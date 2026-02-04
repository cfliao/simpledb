"""
The contents of a disk block in memory.
A page is treated as an array of BLOCK_SIZE bytes.
There are methods to get/set values into this array,
and to read/write the contents of this array to a disk block.

Author: Edward Sciore
"""

from threading import Lock
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_mgr import FileMgr
    from .block import Block


class Page:
    """
    The contents of a disk block in memory.
    Treated as an array of BLOCK_SIZE bytes with methods
    to get/set values and read/write to disk blocks.
    """

    # The number of bytes in a block.
    # Set low for easier testing with many blocks.
    BLOCK_SIZE = 400

    # The size of an integer in bytes.
    INT_SIZE = 4  # Typically 4 bytes for a 32-bit integer

    @staticmethod
    def str_size(n: int) -> int:
        """
        The maximum size, in bytes, of a string of length n.
        A string is represented as the encoding of its characters,
        preceded by an integer denoting the number of bytes in this encoding.

        Args:
            n: the length of the string

        Returns:
            the maximum number of bytes required to store a string of size n
        """
        bytes_per_char = 4  # Assuming UTF-8 encoding worst case
        return Page.INT_SIZE + (n * bytes_per_char)

    def __init__(self, file_mgr: "FileMgr" = None):
        """
        Creates a new page with a byte buffer of BLOCK_SIZE bytes.

        Args:
            file_mgr: the FileMgr instance (optional, can be set later)
        """
        self.contents = bytearray(Page.BLOCK_SIZE)
        self.file_mgr = file_mgr
        self._lock = Lock()

    def read(self, blk: "Block") -> None:
        """
        Populates the page with the contents of the specified disk block.

        Args:
            blk: a reference to a disk block
        """
        with self._lock:
            if self.file_mgr is None:
                raise RuntimeError("FileMgr not initialized")
            self.file_mgr.read(blk, self.contents)

    def write(self, blk: "Block") -> None:
        """
        Writes the contents of the page to the specified disk block.

        Args:
            blk: a reference to a disk block
        """
        with self._lock:
            if self.file_mgr is None:
                raise RuntimeError("FileMgr not initialized")
            self.file_mgr.write(blk, self.contents)

    def append(self, filename: str) -> "Block":
        """
        Appends the contents of the page to the specified file.

        Args:
            filename: the name of the file

        Returns:
            the reference to the newly-created disk block
        """
        with self._lock:
            if self.file_mgr is None:
                raise RuntimeError("FileMgr not initialized")
            return self.file_mgr.append(filename, self.contents)

    def get_int(self, offset: int) -> int:
        """
        Returns the integer value at a specified offset of the page.

        Args:
            offset: the byte offset within the page

        Returns:
            the integer value at that offset
        """
        with self._lock:
            return struct.unpack_from('>I', self.contents, offset)[0]

    def set_int(self, offset: int, val: int) -> None:
        """
        Writes an integer to the specified offset on the page.

        Args:
            offset: the byte offset within the page
            val: the integer to be written to the page
        """
        with self._lock:
            struct.pack_into('>I', self.contents, offset, val & 0xFFFFFFFF)

    def get_string(self, offset: int) -> str:
        """
        Returns the string value at the specified offset of the page.

        Args:
            offset: the byte offset within the page

        Returns:
            the string value at that offset
        """
        with self._lock:
            # Read the length (4 bytes)
            length = struct.unpack_from('>I', self.contents, offset)[0]
            # Read the string bytes
            start = offset + Page.INT_SIZE
            byteval = bytes(self.contents[start:start + length])
            return byteval.decode('utf-8')

    def set_string(self, offset: int, val: str) -> None:
        """
        Writes a string to the specified offset on the page.

        Args:
            offset: the byte offset within the page
            val: the string to be written to the page
        """
        with self._lock:
            byteval = val.encode('utf-8')
            # Write the length
            struct.pack_into('>I', self.contents, offset, len(byteval))
            # Write the string bytes
            start = offset + Page.INT_SIZE
            self.contents[start:start + len(byteval)] = byteval

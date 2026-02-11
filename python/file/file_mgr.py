"""
The SimpleDB file manager.
The database system stores its data as files within a specified directory.
The file manager provides methods for reading the contents of
a file block to a Python bytes object,
writing the contents of bytes to a file block,
and appending the contents of bytes to the end of a file.

Author: Edward Sciore
"""

import os
from pathlib import Path
from threading import Lock
from typing import Dict, Optional
from .page import Page
from .block import Block


class FileMgr:
    """
    The SimpleDB file manager.
    Manages reading, writing, and appending to disk blocks.
    """

    def __init__(self, dbname: str):
        """
        Creates a file manager for the specified database.
        The database will be stored in a folder of that name
        in the user's home directory.
        If the folder does not exist, then a folder containing
        an empty database is created automatically.
        Files for all temporary tables (i.e. tables beginning with "temp") are deleted.

        Args:
            dbname: the name of the directory that holds the database
        """
        home_dir = os.path.expanduser("~")
        self.db_directory = os.path.join(home_dir, dbname)
        self.is_new = not os.path.exists(self.db_directory)

        # create the directory if the database is new
        if self.is_new:
            try:
                os.makedirs(self.db_directory, exist_ok=True)
            except OSError as e:
                raise RuntimeError(f"cannot create {dbname}") from e

        # remove any leftover temporary tables
        if os.path.exists(self.db_directory):
            for filename in os.listdir(self.db_directory):
                if filename.startswith("temp"):
                    temp_file = os.path.join(self.db_directory, filename)
                    try:
                        if os.path.isfile(temp_file):
                            os.remove(temp_file)
                        elif os.path.isdir(temp_file):
                            import shutil
                            shutil.rmtree(temp_file)
                    except OSError:
                        pass

        self.open_files: Dict[str, int] = {}  # filename -> file descriptor
        self._lock = Lock()

    def read(self, blk: Block, contents: bytearray) -> None:
        """
        Reads the contents of a disk block into a bytearray.

        Args:
            blk: a reference to a disk block
            contents: the bytearray to read into
        """
        with self._lock:
            try:
                fc = self._get_file(blk.file_name())
                # Seek to the block position
                offset = blk.id() * Page.BLOCK_SIZE
                os.lseek(fc, offset, os.SEEK_SET)
                # Read the block
                data = os.read(fc, Page.BLOCK_SIZE)
                contents[:len(data)] = data
                # Pad with zeros if necessary
                if len(data) < Page.BLOCK_SIZE:
                    contents[len(data):] = b'\x00' * (Page.BLOCK_SIZE - len(data))
            except OSError as e:
                raise RuntimeError(f"cannot read block {blk}") from e

    def write(self, blk: Block, contents: bytearray) -> None:
        """
        Writes the contents of a bytearray into a disk block.

        Args:
            blk: a reference to a disk block
            contents: the bytearray to write
        """
        with self._lock:
            try:
                fc = self._get_file(blk.file_name())
                # Seek to the block position
                offset = blk.id() * Page.BLOCK_SIZE
                os.lseek(fc, offset, os.SEEK_SET)
                # Write the block
                os.write(fc, bytes(contents))
            except OSError as e:
                raise RuntimeError(f"cannot write block {blk}") from e

    def append(self, filename: str, contents: bytearray) -> Block:
        """
        Appends the contents of a bytearray to the end of the specified file.

        Args:
            filename: the name of the file
            contents: the bytearray to append

        Returns:
            a reference to the newly-created block
        """
        newblknum = self.size(filename)
        blk = Block(filename, newblknum)
        self.write(blk, contents)
        return blk

    def size(self, filename: str) -> int:
        """
        Returns the number of blocks in the specified file.

        Args:
            filename: the name of the file

        Returns:
            the number of blocks in the file
        """
        with self._lock:
            try:
                fc = self._get_file(filename)
                file_size = os.fstat(fc).st_size
                return file_size // Page.BLOCK_SIZE
            except OSError as e:
                raise RuntimeError(f"cannot access {filename}") from e

    def is_new_db(self) -> bool:
        """
        Returns a boolean indicating whether the file manager
        had to create a new database directory.

        Returns:
            True if the database is new
        """
        return self.is_new

    def _get_file(self, filename: str) -> int:
        """
        Returns the file descriptor for the specified filename.
        The file descriptor is stored in a dictionary keyed on the filename.
        If the file is not open, then it is opened and the file descriptor
        is added to the dictionary.

        Args:
            filename: the specified filename

        Returns:
            the file descriptor associated with the open file

        Raises:
            OSError: if the file cannot be opened
        """
        if filename in self.open_files:
            return self.open_files[filename]

        db_table = os.path.join(self.db_directory, filename)
        # Open file with read/write permissions, create if doesn't exist
        fd = os.open(db_table, os.O_RDWR | os.O_CREAT, 0o666)
        self.open_files[filename] = fd
        return fd

    def __del__(self):
        """Close all open files when the FileMgr is destroyed."""
        for fd in self.open_files.values():
            try:
                os.close(fd)
            except OSError:
                pass

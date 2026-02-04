"""
A reference to a disk block.
A Block object consists of a filename and a block number.
It does not hold the contents of the block;
instead, that is the job of a Page object.
"""


class Block:
    """
    A reference to a disk block.
    Consists of a filename and a block number.
    """

    def __init__(self, filename: str, blknum: int):
        """
        Constructs a block reference for the specified filename and block number.

        Args:
            filename: the name of the file
            blknum: the block number
        """
        self.filename = filename
        self.blknum = blknum

    def file_name(self) -> str:
        """
        Returns the name of the file where the block lives.

        Returns:
            the filename
        """
        return self.filename

    def number(self) -> int:
        """
        Returns the location of the block within the file.

        Returns:
            the block number
        """
        return self.blknum

    def __eq__(self, obj) -> bool:
        """
        Compares two Block objects for equality.

        Args:
            obj: the object to compare with

        Returns:
            True if both blocks refer to the same file and block number
        """
        if not isinstance(obj, Block):
            return False
        return self.filename == obj.filename and self.blknum == obj.blknum

    def __str__(self) -> str:
        """
        Returns a string representation of the block.

        Returns:
            a string describing the block
        """
        return f"[file {self.filename}, block {self.blknum}]"

    def __hash__(self) -> int:
        """
        Returns the hash code of the block.

        Returns:
            the hash code based on the string representation
        """
        return hash(str(self))

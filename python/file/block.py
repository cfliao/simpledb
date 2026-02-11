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

    def __init__(self, file_name: str, id: int):
        """
        Constructs a block reference for the specified filename and block number.

        Args:
            filename: the name of the file
            block_number: the block number
        """
        self.file_name = file_name
        self.id = id

    def file_name(self) -> str:
        """
        Returns the name of the file where the block lives.

        Returns:
            the filename
        """
        return self.file_name

    def id(self) -> int:
        """
        Returns the location of the block within the file.

        Returns:
            the block number
        """
        return self.id

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
        return self.file_name == obj.file_name and self.id == obj.id

    def __str__(self) -> str:
        """
        Returns a string representation of the block.

        Returns:
            a string describing the block
        """
        return f"[file {self.file_name}, block {self.id}]"

    def __hash__(self) -> int:
        """
        Returns the hash code of the block.

        Returns:
            the hash code based on the string representation
        """
        return hash(str(self))

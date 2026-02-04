"""
Test file for the SimpleDB file management module.

Author: Edward Sciore
"""

from file_mgr import FileMgr
from page import Page
from block import Block


def main():
    """
    Main test function.
    Demonstrates creating a file manager, page, and block,
    writing data to the page, and persisting it to disk.
    """
    # Initialize the file manager
    file_manager = FileMgr("testdb")

    # Create a block reference
    block = Block("test1", 0)

    # Create a page
    p1 = Page(file_manager)

    # Write data to the page
    p1.set_string(0, "HelloWorld1")
    p1.set_int(15, 20)
    p1.set_string(19, "HelloWorld2")

    # Write the page to disk
    p1.write(block)

    print("File test completed successfully!")
    print(f"Wrote to block: {block}")


if __name__ == "__main__":
    main()

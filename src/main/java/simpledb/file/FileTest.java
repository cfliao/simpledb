package simpledb.file;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import simpledb.server.SimpleDB;

public class FileTest {
    public static void main(String[] args) {
        //FileMgr fileManager = new FileMgr("abcde");
        SimpleDB.initFileMgr("testdb");
        Block block = new Block("test1", 0);
        Page p1 = new Page();
        p1.setString(0, "HelloWorld1");
        p1.setInt(15, 20);
        p1.setString(19, "HelloWorld2");
        
        p1.write(block);

    }

    
}



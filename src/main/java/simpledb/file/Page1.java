package simpledb.file;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;

import simpledb.server.SimpleDB;

public class Page1 {
   /**
    * The number of bytes in a block.
    * This value is set unreasonably low, so that it is easier
    * to create and test databases having a lot of blocks.
    * A more realistic value would be 4K.
    */
   public static final int BLOCK_SIZE = 400;

   /**
    * The size of an integer in bytes.
    * This value is almost certainly 4, but it is
    * a good idea to encode this value as a constant.
    */
   public static final int INT_SIZE = Integer.SIZE / Byte.SIZE;

   /**
    * The maximum size, in bytes, of a string of length n.
    * A string is represented as the encoding of its characters,
    * preceded by an integer denoting the number of bytes in this encoding.
    * If the JVM uses the US-ASCII encoding, then each char
    * is stored in one byte, so a string of n characters
    * has a size of 4+n bytes.
    * 
    * @param n the size of the string
    * @return the maximum number of bytes required to store a string of size n
    */
   public static final int STR_SIZE(int n) {
      float bytesPerChar = Charset.defaultCharset().newEncoder().maxBytesPerChar();

      return INT_SIZE + (n * (int) bytesPerChar);
   }

   private ByteBuffer contents = ByteBuffer.allocateDirect(BLOCK_SIZE);
   private FileMgr filemgr = SimpleDB.fileMgr();

   /**
    * Creates a new page. Although the constructor takes no arguments,
    * it depends on a {@link FileMgr} object that it gets from the
    * method {@link simpledb.server.SimpleDB#fileMgr()}.
    * That object is created during system initialization.
    * Thus this constructor cannot be called until either
    * {@link simpledb.server.SimpleDB#init(String)} or
    * {@link simpledb.server.SimpleDB#initFileMgr(String)} or
    * {@link simpledb.server.SimpleDB#initFileAndLogMgr(String)} or
    * {@link simpledb.server.SimpleDB#initFileLogAndBufferMgr(String)}
    * is called first.
    */
   public Page1() {
   }

   protected ByteBuffer getContents() {
      return contents;
   }

   /**
    * Populates the page with the contents of the specified disk block.
    * 
    * @param blk a reference to a disk block
    */
   public synchronized void loadFrom(Block1 blk) {
      try (RandomAccessFile file = new RandomAccessFile(blk.getFileName(), "rw")) {
         FileChannel fc = file.getChannel();
         fc.read(contents, blk.getId() * BLOCK_SIZE);
      } catch (IOException e) {
         e.printStackTrace();
      }

      // try {
      // contents.clear();
      // FileChannel fc = getFile(blk.getFileName());
      // fc.read(contents, blk.getId() * BLOCK_SIZE);
      // } catch (IOException e) {
      // e.printStackTrace();
      // //throw new RuntimeException("cannot read block " + blk);
      // }
   }

   // private FileChannel getFile(String filename) throws IOException {
   // FileChannel fc = openFiles.get(filename);
   // if (fc == null) {
   // File dbTable = new File(dbDirectory, filename);
   // RandomAccessFile f = new RandomAccessFile(dbTable, "rws");
   // fc = f.getChannel();
   // openFiles.put(filename, fc);
   // // f.close();
   // }
   // return fc;
   // }

   /**
    * Writes the contents of the page to the specified disk block.
    * 
    * @param blk a reference to a disk block
    */
   public synchronized void writeTo(Block1 block) {
      // filemgr.write(blk, contents);
      contents.rewind();
      try (RandomAccessFile file = new RandomAccessFile(block.getFileName(), "rw")) {
         FileChannel fc = file.getChannel();
         fc.write(contents, block.getId() * BLOCK_SIZE);
      } catch (IOException e) {
         e.printStackTrace();
      }
   }

   /**
    * Appends the contents of the page to the specified file.
    * 
    * @param filename the name of the file
    * @return the reference to the newly-created disk block
    */
   public synchronized Block append(String filename) {
      return filemgr.append(filename, contents);
   }

   /**
    * Returns the integer value at a specified offset of the page.
    * If an integer was not stored at that location,
    * the behavior of the method is unpredictable.
    * 
    * @param offset the byte offset within the page
    * @return the integer value at that offset
    */
   public synchronized int getInt(int offset) {
      contents.position(offset);
      return contents.getInt();
   }

   /**
    * Writes an integer to the specified offset on the page.
    * 
    * @param offset the byte offset within the page
    * @param val    the integer to be written to the page
    */
   public synchronized void setInt(int offset, int val) {
      contents.position(offset);
      contents.putInt(val);
   }

   /**
    * Returns the string value at the specified offset of the page.
    * If a string was not stored at that location,
    * the behavior of the method is unpredictable.
    * 
    * @param offset the byte offset within the page
    * @return the string value at that offset
    */
   public synchronized String getString(int offset) {
      contents.position(offset);
      int len = contents.getInt();
      byte[] byteval = new byte[len];
      contents.get(byteval);
      return new String(byteval);
   }

   /**
    * Writes a string to the specified offset on the page.
    * 
    * @param offset the byte offset within the page
    * @param val    the string to be written to the page
    */
   public synchronized void setString(int offset, String val) {
      contents.position(offset);
      byte[] byteval = val.getBytes();
      contents.putInt(byteval.length);
      contents.put(byteval);
   }

}

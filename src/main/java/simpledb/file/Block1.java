package simpledb.file;

/**
 * A reference to a disk block.
 * A Block object consists of a filename and a block number.
 * It does not hold the contents of the block;
 * instead, that is the job of a {@link Page} object.
 * 
 * @author Edward Sciore
 */
public class Block1 {
   private String filename;
   private int id;

   /**
    * Constructs a block reference
    * for the specified filename and block number.
    * 
    * @param filename the name of the file
    * @param id       the block number
    */
   public Block1(String filename, int id) {
      this.filename = filename;
      this.id = id;
   }

   /**
    * Returns the name of the file where the block lives.
    * 
    * @return the filename
    */
   public String getFileName() {
      return filename;
   }

   /**
    * Returns the location of the block within the file.
    * 
    * @return the block number
    */
   public int getId() {
      return id;
   }

   public boolean equals(Object obj) {
      if (!(obj instanceof Block1))
         return false;
      else
         return filename.equals(((Block1) obj).getFileName()) && id == ((Block1) obj).getId();
   }

   public String toString() {
      return "[file " + filename + ", block " + id + "]";
   }

   public int hashCode() {
      return toString().hashCode();
   }
}

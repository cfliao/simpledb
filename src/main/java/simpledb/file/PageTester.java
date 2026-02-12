package simpledb.file;

import java.io.IOException;
import java.util.HexFormat;

public class PageTester {

    public static void main(String[] args) throws IOException {
        testPageRead();
    }

    public static void testPageRead() {
        Page1 page = new Page1();
        page.loadFrom(new Block1("C:/Users/Administrator/testdb/test1", 0));
        page.getContents().rewind();
        // System.out.println(page.getContents().remaining());
        byte[] bytes = new byte[page.getContents().remaining()];
        page.getContents().get(bytes);
        HexFormat format = HexFormat.ofDelimiter(" ").withUpperCase();
        for (int i = 0; i < bytes.length; i += 16) {
            int end = Math.min(i + 16, bytes.length);
            byte[] chunk = new byte[end - i];
            System.arraycopy(bytes, i, chunk, 0, chunk.length);
            System.out.println(format.formatHex(chunk));
        }
        // dump(page.getContents());

        // byte[] fileBytes =
        // Files.readAllBytes(Paths.get("C:/Users/Administrator/testdb/test1"));
        // System.out.println(format.formatHex(fileBytes));
    }

}

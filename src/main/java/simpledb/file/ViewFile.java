package simpledb.file;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ViewFile {
    public static void main(String[] args) {
        printFileAsByteContent("C:/Users/Administrator/testdb/test1");
    }

    public static void printFileAsByteContent(String filePath) {
        Path path = Paths.get(filePath);

        try {
            // 讀取檔案所有位元組 (適合小型教學檔案)
            byte[] fileBytes = Files.readAllBytes(path);

            System.out.println("檔案路徑: " + path.toAbsolutePath());
            System.out.println("------------------------------------------------------------");
            System.out.printf("%-10s | %-4s | %-4s | %-5s%n", "Offset", "Hex", "Dec", "Char");
            System.out.println("------------------------------------------------------------");

            for (int i = 0; i < fileBytes.length; i++) {
                byte b = fileBytes[i];

                // 轉換為無符號整數以便正確顯示十進位
                int unsignedByte = b & 0xFF;

                // 判斷是否為可列印字元 (ASCII 32~126)
                char asciiChar = (unsignedByte >= 32 && unsignedByte <= 126) ? (char) unsignedByte : '.';

                // 格式化輸出
                // %04X: 十六進位, %3d: 十進位
                System.out.printf("0x%08d | 0x%02X | %3d | %c%n", i, unsignedByte, unsignedByte, asciiChar);
            }

            System.out.println("------------------------------------------------------------");
            System.out.println("讀取完成，總計 " + fileBytes.length + " 位元組。");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

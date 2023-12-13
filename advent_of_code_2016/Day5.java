import java.util.Scanner;
import java.security.MessageDigest;

public class Day5 extends AocSolver {

    public Day5(String filename) {
        super(filename);
    }

    private String bytesToHexString(byte[] bytes) {
        String result = "";
        for (byte b : bytes) {
            int i = (b & 0xff) | 0x100;
            result += Integer.toHexString(i).substring(1);
        }
        return result;
    }

    @Override
    public void solve(Scanner scan) {
        String code = scan.nextLine();
        scan.close();
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
        } catch (Exception e) {
            System.err.println(e);
            return;
        }

        String password1 = "";
        char[] password2 = new char[8];
        int i = 0;
        String nextCode;
        int password1Length = 0;
        int password2Length = 0;

        while (password2Length < 8) {
            nextCode = code + i;
            byte[] digest = md.digest(nextCode.getBytes());
            String hash = bytesToHexString(digest);
            if (hash.startsWith("00000")) {
                char position = hash.charAt(5);
                char character = hash.charAt(6);
                if (password1Length < 8) {
                    password1Length++;
                    password1 += position;
                }
                if ('0' <= position && position <= '7') {
                    int index = position - '0';
                    if (password2[index] == 0) {
                        password2[index] = character;
                        password2Length++;
                    }
                }
            }
            i++;
        }
        System.out.println("Part 1: " + password1);
        String password2String = "";
        for (char c : password2) {
            password2String += c;
        }
        System.out.println("Part 2: " + password2String);
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day5("input5.txt");
        solver.run(argv);
    }    
}

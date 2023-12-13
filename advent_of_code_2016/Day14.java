import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import java.util.Scanner;
import java.security.MessageDigest;

public class Day14 extends AocSolver {

    public Day14(String filename) {
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
    private char findConsecutive(String line, int consecutive) {
        for (int i = consecutive - 1; i < line.length(); i++) {
            boolean isConsecutive = true;
            char currentChar = line.charAt(i);
            for (int j = 1; j < consecutive; j++) {
                if (currentChar != line.charAt(i - j)) {
                    isConsecutive = false;
                    break;
                }
            }
            if (isConsecutive) {
                return currentChar;
            }
        }
        return '\0';
    }
    private int getOneTimePad(String salt, int keyStretching) {
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
        } catch (Exception e) {
            System.err.println(e);
            return -1;
        }

        int i = 0;
        String nextCode = salt + i;
        int currKey = 0;
        Map<Character, Queue<Integer>> triplets = new HashMap<>();
        
        while (true) {
            nextCode = salt + i;
            byte[] digest = md.digest(nextCode.getBytes());
            String hash = bytesToHexString(digest);
            for (int k = 0; k < keyStretching; k++) {
                digest = md.digest(hash.getBytes());
                hash = bytesToHexString(digest);
            }
            char quintuplet = findConsecutive(hash, 5);
            char triplet = findConsecutive(hash, 3);
            if (quintuplet != 0) {
                Queue<Integer> q = triplets.get(quintuplet);
                while (!q.isEmpty()) {
                    int index = q.remove();
                    if (i - index <= 1000) {
                        currKey++;
                        if (currKey == 64) {
                            return index;
                        }
                    }
                }
            }
            if (triplet != 0) {
                triplets.putIfAbsent(triplet, new ArrayDeque<>());
                Queue<Integer> q = triplets.get(triplet);
                q.add(i);
            }
            i++;
        }
    }

    @Override
    public void solve(Scanner scan) {
        String code = scan.nextLine();
        scan.close();
        
        System.out.println("Part 1: " + getOneTimePad(code, 0));
        System.out.println("Part 2: " + getOneTimePad(code, 2016));  
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day14("input14.txt");
        solver.run(argv);
    }    
}

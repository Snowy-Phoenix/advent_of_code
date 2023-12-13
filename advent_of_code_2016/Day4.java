import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.Scanner;

public class Day4 extends AocSolver {

    public Day4(String filename) {
        super(filename);
    }

    private class EncryptedRoom {
        public List<String> names;
        public int sectorId;
        public String checksum;

        public EncryptedRoom(List<String> names, int sectorId, String checksum) {
            this.names = names;
            this.sectorId = sectorId;
            this.checksum = checksum;
        }
    }

    private EncryptedRoom parse(String string) {
        String[] tokens = string.split("-");
        List<String> names = new ArrayList<String>(Arrays.asList(tokens));
        String rawChecksum = names.get(names.size() - 1);
        rawChecksum = rawChecksum.substring(0, rawChecksum.length() - 1);
        String[] rawChecksumTokens = rawChecksum.split("\\[");
        int sectorId = Integer.parseInt(rawChecksumTokens[0]);
        String checksum = rawChecksumTokens[1];
        names.remove(names.size() - 1); // Last element is sectorid and checksum.
        return new EncryptedRoom(names, sectorId, checksum);
    }

    private int charCompare(char c1, char c2, Map<Character, Integer> counts) {
        int count1 = counts.get(c1);
        int count2 = counts.get(c2);
        if (count2 > count1) {
            // RHS should be in LHS.
            return 1;
        }  else if (count2 == count1) {
            if (c2 < c1) {
                // Sort alphabetically if sums equal.
                return 1;
            }
        }
        return -1;
    }

    private boolean isRoomReal(EncryptedRoom room) {
        Map<Character, Integer> counts = new HashMap<>();
        for (String n : room.names) {
            for (int i = 0; i < n.length(); i++) {
                char c = n.charAt(i);
                if (counts.containsKey(c)) {
                    counts.put(c, counts.get(c) + 1);
                } else {
                    counts.put(c, 1);
                }
            }
        }
        List<Character> sortedCharsByCounts = new ArrayList<>(counts.keySet());
        sortedCharsByCounts.sort((x, y) -> charCompare(x, y, counts));
        String checksum = "";
        for (int i = 0; i < 5; i++) {
            checksum += sortedCharsByCounts.get(i);
        }
        return checksum.equals(room.checksum);
    }

    private char shift(char c, int shift) {
        return (char)((((c - 'a') + shift) % 26) + 'a');
    }
    private String decrypt(EncryptedRoom room) {
        String decryptedRoomName = "";
        for (int wordi = 0; wordi < room.names.size(); wordi++) {
            String word = room.names.get(wordi);
            if (wordi > 0) {
                decryptedRoomName += " ";
            }
            for (int i = 0; i < word.length(); i++) {
                decryptedRoomName += shift(word.charAt(i), room.sectorId);
            }
        }
        return decryptedRoomName;
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = this.getLines(scan);
        scan.close();
        int idSum = 0;
        int northpoleSectorId = 0;
        for (String line : lines) {
            EncryptedRoom room = parse(line);
            if (isRoomReal(room)) {
                idSum += room.sectorId;
                String decryptedRoom = decrypt(room);
                if (decryptedRoom.equals("northpole object storage")) {
                    northpoleSectorId = room.sectorId;
                }
            }
        }
        System.out.println("Part 1: " + idSum);
        System.out.println("Part 2: " + northpoleSectorId);
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day4("input4.txt");
        solver.run(argv);
    } 
}

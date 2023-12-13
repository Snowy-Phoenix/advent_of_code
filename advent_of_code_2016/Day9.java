import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;


public class Day9 extends AocSolver {

    public Day9(String filename) {
        super(filename);
    }

    private String getMarker(String line, int offset) {
        int endMarker = offset;
        while (endMarker < line.length()) {
            if (line.charAt(endMarker) == ')') {
                return line.substring(offset, endMarker + 1);
            }
            endMarker++;
        }
        return "";
    }

    private int[] parseMarker(String markerString) {
        markerString = markerString.substring(1, markerString.length() - 1);
        String[] params = markerString.split("x");
        int[] output = new int[2];
        output[0] = Integer.parseInt(params[0]);
        output[1] = Integer.parseInt(params[1]);
        return output;
    }
    private String decompressSubstring(int[] marker, String line, int offset) {
        int length = marker[0];
        int repetitions = marker[1];
        String repeatedString = "";
        for (; repetitions > 0; repetitions--) {
            repeatedString += line.substring(offset, offset + length);
        }
        return repeatedString;
    }

    private int solvePart1(String compressedString) {
        String decompressedString = "";
        int cursor = 0;
        while (cursor < compressedString.length()) {
            if (compressedString.charAt(cursor) == '(') {
                String markerString = getMarker(compressedString, cursor);
                cursor += markerString.length();
                int[] marker = parseMarker(markerString);
                decompressedString += decompressSubstring(marker, 
                                        compressedString, cursor);
                cursor += marker[0];
            } else {
                cursor++;
            }
        }
        return decompressedString.length();
    }
    private void multiplyCounts(int key, long mul, Map<Integer, Long> counts) {
        if (counts.containsKey(key)) {
            counts.put(key, counts.get(key) * mul);
        } else {
            counts.put(key, mul);
        }
    }
    private void addCounts(int[] marker, String line, 
                int offset, Map<Integer, Long> counts) {
        int length = marker[0];
        long repetitions = marker[1];
        boolean outOfMarker = true;
        for (int i = 0; i < length; i++) {
            int cursor = offset + i;
            if (line.charAt(cursor) == ')') {
                outOfMarker = true;
            } else if (line.charAt(cursor) == '(') {
                outOfMarker = false;
            } else if (outOfMarker) {
                multiplyCounts(cursor, repetitions, counts);
            }
        }
    }

    private long solvePart2(String compressedString) {
        Map<Integer, Long> counts = new HashMap<>();
        int cursor = 0;
        while (cursor < compressedString.length()) {
            if (compressedString.charAt(cursor) == '(') {
                String markerString = getMarker(compressedString, cursor);
                cursor += markerString.length();

                int[] marker = parseMarker(markerString);
                addCounts(marker, compressedString, cursor, counts);
            } else {
                multiplyCounts(cursor, 1, counts);
                cursor++;
            }
        }
        return counts.values().stream().mapToLong((x) -> x).sum();
    }

    @Override
    public void solve(Scanner scan) {
        String compressedString = scan.nextLine();
        scan.close();
        
        System.out.println("Part 1: " + solvePart1(compressedString));
        System.out.println("Part 2: " + solvePart2(compressedString));
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day9("input9.txt");
        solver.run(argv);
    }    
}

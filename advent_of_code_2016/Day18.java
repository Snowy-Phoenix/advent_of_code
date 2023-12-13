import java.util.Scanner;

public class Day18 extends AocSolver {

    public Day18(String filename) {
        super(filename);
    }

    private int countSafe(String row) {
        int safe = 0;
        for (char c : row.toCharArray()) {
            safe += c == '.' ? 1 : 0;
        }
        return safe;
    }

    private boolean matchesPattern(String row, int offset, String pattern) {
        for (int i = 0; i < 3; i++) {
            int j = offset + i - 1;
            char c = pattern.charAt(i);
            if (j < 0 || row.length() <= j ) {
                if (c == '^') {
                    return false;
                }
                continue;
            }
            if (row.charAt(j) != c) {
                return false;
            }
        }
        return true;
    }

    private String computeNextRow(String row, String[] patterns) {
        String nextRow = "";
        for (int i = 0; i < row.length(); i++) {
            boolean patternMatches = false;
            for (String pattern : patterns) {
                if (matchesPattern(row, i, pattern)) {
                    patternMatches = true;
                    break;
                }
            }
            if (patternMatches) {
                nextRow += "^";
            } else {
                nextRow += ".";
            }
        }
        return nextRow;
    }

    @Override
    public void solve(Scanner scan) {
        String line = scan.nextLine();
        scan.close();

        String[] trapPatterns = {"^^.", ".^^", "^..", "..^"};
        final int NUM_ROWS = 400000;
        int safe = countSafe(line);
        String currRow = line;
        for (int i = 1; i < NUM_ROWS; i++) {
            if (i == 40) {
                System.out.println("Part 1: " + safe);
            }
            currRow = computeNextRow(currRow, trapPatterns);
            safe += countSafe(currRow);
        }
        System.out.println("Part 2: " + safe);
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day18("input18.txt");
        solver.run(argv);
    }        
}

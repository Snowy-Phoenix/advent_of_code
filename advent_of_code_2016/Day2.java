import java.util.List;
import java.util.Scanner;

public class Day2 extends AocSolver {

    public Day2(String filename) {
        super(filename);
    }

    private int moveCol(char c) {
        switch (c) {
            case 'L':
                return -1;
            case 'R':
                return 1;
            default:
                return 0;
        }
    }
    private int moveRow(char c) {
        switch (c) {
            case 'U':
                return -1;
            case 'D':
                return 1;
            default:
                return 0;
        }
    }
    private int fixBounds(int x, int size) {
        if (x < 0) {
            return 0;
        }
        if (x >= size) {
            return size - 1;
        }
        return x;
    }

    private void solvePart1(List<String> lines) {
        String[][] numpad = {{"1", "2", "3"},
                              {"4", "5", "6"},
                              {"7", "8", "9"}};
        String code = "";
        int row = 1;
        int col = 1;
        for (String s : lines) {
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                row += moveRow(c);
                col += moveCol(c);
                row = fixBounds(row, 3);
                col = fixBounds(col, 3);
            }
            code += numpad[row][col];
        }
        System.out.println("Part 1: " + code);
    }

    private void solvePart2(List<String> lines) {
        String[][] numpad = {{" ", " ", "1", " ", " "},
                             {" ", "2", "3", "4", " "},
                             {"5", "6", "7", "8", "9"},
                             {" ", "A", "B", "C", " "},
                             {" ", " ", "D", " ", " "}};
        String code = "";
        int row = 2;
        int col = 0;
        for (String s : lines) {
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                int nextRow = row + moveRow(c);
                int nextCol = col + moveCol(c);
                nextRow = fixBounds(nextRow, 5);
                nextCol = fixBounds(nextCol, 5);
                if (numpad[nextRow][nextCol].equals(" ")) {
                    continue;
                } else {
                    row = nextRow;
                    col = nextCol;
                }
            }
            code += numpad[row][col];
        }
        System.out.println("Part 2: " + code);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = this.getLines(scan);
        scan.close();
        solvePart1(lines);
        solvePart2(lines);
        
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day2("input2.txt");
        solver.run(argv);
    } 
}
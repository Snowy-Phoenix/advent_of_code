import java.util.List;
import java.util.Scanner;

class Instruction {
    public enum InsType {RECT, ROTROW, ROTCOL}
    public InsType type;
    public int paramA;
    public int paramB;

    public Instruction(InsType type, int paramA, int paramB) {
        this.type = type;
        this.paramA = paramA;
        this.paramB = paramB;
    }

    public static Instruction parseInstruction(String line) {
        String[] tokens = line.split(" ");
        int paramA;
        int paramB;
        InsType type;
        if (tokens[0].equals("rect")) {
            String[] params = tokens[1].split("x");
            paramA = Integer.parseInt(params[0]);
            paramB = Integer.parseInt(params[1]);
            type = InsType.RECT;
            return new Instruction(type, paramA, paramB);
        } else if (tokens[1].equals("row")) {
            type = InsType.ROTROW;
        } else {
            type = InsType.ROTCOL;
        }
        String[] params = tokens[2].split("=");
        paramA = Integer.parseInt(params[1]);
        paramB = Integer.parseInt(tokens[4]);
        return new Instruction(type, paramA, paramB);
    }
}

class Screen {
    public int rows;
    public int cols;
    public boolean[][] screen;

    public Screen(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        this.screen = new boolean[rows][cols];
    }

    public void turnOn(int row, int col) {
        if (0 <= row && row < this.rows 
            && 0 <= col && col < this.cols) {
                screen[row][col] = true;
        }
    }

    public void rect(int length, int width) {
        length = Math.min(this.cols, length);
        width = Math.min(this.rows, width);
        for (int r = 0; r < width; r++) {
            for (int c = 0; c < length; c++) {
                turnOn(r, c);
            }
        }
    }
    public void rotRow(int row, int n) {
        if (0 <= row && row < this.rows) {
            boolean[] tmp = screen[row].clone();
            for (int i = 0; i < this.cols; i++) {
                int shiftedi = (i + n) % this.cols;
                screen[row][shiftedi] = tmp[i];
            }
        }
    }
    public void rotCol(int col, int n) {
        if (0 <= col && col < this.cols) {
            boolean[] tmp = new boolean[this.rows];
            for (int i = 0; i < this.rows; i++) {
                tmp[i] = screen[i][col];
            }
            for (int i = 0; i < this.rows; i++) {
                int shiftedi = (i + n) % this.rows;
                screen[shiftedi][col] = tmp[i];
            }
        }
    }
    public int countOn() {
        int numOn = 0;
        for (boolean[] bs : screen) {
            for (boolean b : bs) {
                numOn += b ? 1 : 0;
            }
        }
        return numOn;
    }
    public void execute(Instruction ins) {
        switch(ins.type) {
            case RECT:
                rect(ins.paramA, ins.paramB);
                break;
            case ROTCOL:
                rotCol(ins.paramA, ins.paramB);
                break;
            case ROTROW:
                rotRow(ins.paramA, ins.paramB);
                break;
            default:
                break;
        }
    }
    @Override
    public String toString() {
        String str = "";
        for (boolean[] bs : this.screen) {
            for (boolean b : bs) {
                str += b ? "#" : " ";
            }
            str += "\n";
        }
        return str;
    }
}

public class Day8 extends AocSolver {

    public Day8(String filename) {
        super(filename);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> instructionsStrings = getLines(scan);
        scan.close();
        Screen screen = new Screen(6, 50);
        instructionsStrings.stream().map((x) -> Instruction.parseInstruction(x))
                                    .forEach((x) -> screen.execute(x));
        
        System.out.println("Part 1: " + screen.countOn());
        System.out.println("Part 2:");
        System.out.println(screen);
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day8("input8.txt");
        solver.run(argv);
    }    
}

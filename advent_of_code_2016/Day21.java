import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

abstract class Instruction {

    public abstract void execute(String[] passcode);
    public abstract void antiExecute(String[] passcode);

    public void swap(String[] passcode, int i1, int i2) {
        String c = passcode[i1];
        passcode[i1] = passcode[i2];
        passcode[i2] = c;
    }
    public int find(String letter, String[] passcode) {
        for (int i = 0; i < passcode.length; i++) {
            String s = passcode[i];
            if (s.equals(letter)) {
                return i;
            }
        }
        return -1;
    }
}
class SwapPosition extends Instruction {
    public int param1;
    public int param2;

    public SwapPosition(int param1, int param2) {
        this.param1 = param1;
        this.param2 = param2;
    }

    public void execute(String[] passcode) {
        swap(passcode, param1, param2);
    }
    public void antiExecute(String[] passcode) {
        execute(passcode);
    }
}
class SwapLetters extends Instruction {
    public String param1;
    public String param2;

    public SwapLetters(String param1, String param2) {
        this.param1 = param1;
        this.param2 = param2;
    }

    public void execute(String[] passcode) {
        int i1 = find(param1, passcode);
        int i2 = find(param2, passcode);
        swap(passcode, i1, i2);
    }
    public void antiExecute(String[] passcode) {
        execute(passcode);
    }
}
class RotateRight extends Instruction {
    public int count;

    public RotateRight(int count) {
        this.count = count;
    }
    public void execute(String[] passcode) {
        for (int i = 0; i < count; i++) {
            for (int j = passcode.length - 2; j >= 0; j--) {
                swap(passcode, j, j + 1);
            }
        }
    }
    public void antiExecute(String[] passcode) {
        RotateLeft compliment =  new RotateLeft(count);
        compliment.execute(passcode);
    }
}
class RotateLeft extends Instruction {
    public int count;

    public RotateLeft(int count) {
        this.count = count;
    }
    public void execute(String[] passcode) {
        for (int i = 0; i < count; i++) {
            for (int j = 1; j < passcode.length; j++) {
                swap(passcode, j, j - 1);
            }
        }
    }
    public void antiExecute(String[] passcode) {
        RotateRight compliment =  new RotateRight(count);
        compliment.execute(passcode);
    }
}
class RotateLetter extends Instruction {
    public String letter;

    public RotateLetter(String letter) {
        this.letter = letter;
    }
    private int computeShift(int index) {
        return 1 + index + (index >= 4 ? 1 : 0);
    }
    public void execute(String[] passcode) {
        int index = find(letter, passcode);
        int shift = computeShift(index);
        for (int i = 0; i < shift; i++) {
            for (int j = passcode.length - 2; j >= 0; j--) {
                swap(passcode, j, j + 1);
            }
        }
    }
    public void antiExecute(String[] passcode) {
        int index = find(letter, passcode);
        // Try to find the prev index that moved the letter into the
        // current index.
        int prevIndex = 0;
        for (; prevIndex < passcode.length; prevIndex++) {
            if (((prevIndex + computeShift(prevIndex)) % passcode.length) == index) {
                break;
            }
        }
        while (index != prevIndex) {
            for (int j = passcode.length - 2; j >= 0; j--) {
                swap(passcode, j, j + 1);
            }
            index = (index + 1) % passcode.length;
        }
    }
}
class ReversePositions extends Instruction {
    public int param1;
    public int param2;

    public ReversePositions(int param1, int param2) {
        this.param1 = param1;
        this.param2 = param2;
    }
    public void execute(String[] passcode) {
        int low = param1;
        int high = param2;
        while (low < high) {
            swap(passcode, low, high);
            low++;
            high--;
        }
    }
    public void antiExecute(String[] passcode) {
        execute(passcode);
    }
}
class MovePosition extends Instruction {
    public int param1;
    public int param2;

    public MovePosition(int param1, int param2) {
        this.param1 = param1;
        this.param2 = param2;
    }
    public void execute(String[] passcode) {
        if (param1 < param2) {
            // Moving right
            int i = param1;
            while (i < param2) {
                swap(passcode, i, i + 1);
                i++;
            }
        } else {
            // Moving left
            int i = param1;
            while (i > param2) {
                swap(passcode, i, i - 1);
                i--;
            }
        }
    }
    public void antiExecute(String[] passcode) {
        int p = param1;
        param1 = param2;
        param2 = p;
        execute(passcode);
        param2 = param1;
        param1 = p;
    }
}

public class Day21 extends AocSolver {

    public Day21(String filename) {
        super(filename);
    }

    private Instruction parseSwap(String line) {
        String[] words = line.split(" ");
        if (words[1].equals("position")) {
            int pos1 = Integer.parseInt(words[2]);
            int pos2 = Integer.parseInt(words[5]);
            return new SwapPosition(pos1, pos2);
        }
        String letter1 = words[2];
        String letter2 = words[5];
        return new SwapLetters(letter1, letter2);
    }
    private Instruction parseRotate(String line) {
        String[] words = line.split(" ");
        if (words[1].equals("right")) {
            int count = Integer.parseInt(words[2]);
            return new RotateRight(count);
        } else if (words[1].equals("left")) {
            int count = Integer.parseInt(words[2]);
            return new RotateLeft(count);
        }
        String letter = words[6];
        return new RotateLetter(letter);
    }
    private Instruction parseReverse(String line) {
        String[] words = line.split(" ");
        int pos1 = Integer.parseInt(words[2]);
        int pos2 = Integer.parseInt(words[4]);
        return new ReversePositions(Math.min(pos1, pos2), Math.max(pos1, pos2));
    }
    private Instruction parseMove(String line) {
        String[] words = line.split(" ");
        int pos1 = Integer.parseInt(words[2]);
        int pos2 = Integer.parseInt(words[5]);
        return new MovePosition(pos1, pos2);
    }

    private List<Instruction> parseInstructions(List<String> lines) {
        List<Instruction> ls = new ArrayList<>();
        for (String line : lines) {
            if (line.startsWith("swap")) {
                ls.add(parseSwap(line));
            } else if (line.startsWith("rotate")) {
                ls.add(parseRotate(line));
            } else if (line.startsWith("reverse")) {
                ls.add(parseReverse(line));
            } else if (line.startsWith("move")) {
                ls.add(parseMove(line));
            }
        }
        return ls;
    }

    private void fillArray(String line, String[] arr) {
        for (int i = 0; i < line.length(); i++) {
            arr[i] = "" + line.charAt(i);
        } 
    }

    public static String arrToString(String[] arr) {
        String str = "";
        for (String c : arr) {
            str += c;
        }
        return str;
    }

    private String solvePart1(String passcode, List<Instruction> instructions) {
        String[] passcodeArr = new String[passcode.length()];
        fillArray(passcode, passcodeArr);
        for (Instruction ins : instructions) {
            ins.execute(passcodeArr);
        }
        return arrToString(passcodeArr);
    }
    private String solvePart2(String passcode, List<Instruction> instructions) {
        String[] passcodeArr = new String[passcode.length()];
        fillArray(passcode, passcodeArr);
        for (int i = instructions.size() - 1; i >= 0; i--) {
            Instruction ins = instructions.get(i);
            ins.antiExecute(passcodeArr);
        }
        return arrToString(passcodeArr);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = getLines(scan);
        scan.close();
        List<Instruction> instructions = parseInstructions(lines);
        String passcode = "abcdefgh";
        System.out.println("Part 1: " + solvePart1(passcode, instructions));
        String scrambledPasscode = "fbgdceah";
        System.out.println("Part 2: " + solvePart2(scrambledPasscode, instructions));
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day21("input21.txt");
        solver.run(argv);
    }        
}

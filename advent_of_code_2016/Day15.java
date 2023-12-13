import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Day15 extends AocSolver {

    private class Disc {
        public int discNumber;
        public int positions;
        public int initPosition;

        public Disc(int num, int pos, int initPos) {
            discNumber = num;
            positions = pos;
            initPosition = initPos;
        }
        public int alignDisc(int offset, int multiple) {
            for (int i = 0; i < positions; i++) {
                int newPosition = (initPosition + offset + i*multiple + discNumber) % positions;
                if (newPosition == 0) {
                    return i;
                }

            }
            return -1;
        }
    }

    public Day15(String filename) {
        super(filename);
    }

    private List<Disc> parseDiscs(List<String> lines) {
        List<Disc> discs = new ArrayList<>();
        for (String line : lines) {
            String[] words = line.split(" ");
            int discNum = Integer.parseInt(words[1].substring(1));
            int pos = Integer.parseInt(words[3]);
            int initPos = Integer.parseInt((words[11].split("\\."))[0]);
            discs.add(new Disc(discNum, pos, initPos));
        }
        return discs;
    }

    private int calculateEarliestCapsule(List<Disc> discs) {
        int offset = 0;
        int multiple = 1;
        for (Disc d : discs) {
            int cycles = d.alignDisc(offset, multiple);
            if (cycles == -1) {
                return -1;
            }
            offset += cycles * multiple;
            multiple *= d.positions; 
        }
        return offset;
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = getLines(scan);
        scan.close();

        List<Disc> discs = parseDiscs(lines);
        
        System.out.println("Part 1: " + calculateEarliestCapsule(discs));
        discs.add(new Disc(discs.size() + 1, 11, 0));
        System.out.println("Part 2: " + calculateEarliestCapsule(discs));
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day15("input15.txt");
        solver.run(argv);
    }    
}

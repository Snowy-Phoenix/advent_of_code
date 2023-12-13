import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class BitArray {
    public List<Character> bytes;
    public int size; // Number of bits.

    public BitArray() {
        bytes = new ArrayList<>();
        size = 0;
    }

    public void appendbit(int bit) {
        int biti = size % 8;
        if (biti == 0) {
            bytes.add((char)bit);
        } else {
            char b = bytes.get(bytes.size() - 1);
            b |= bit << biti;
            bytes.set(bytes.size() - 1, b);
        }
        size++;
    }
    public int getBit(int index) {
        if (0 <= index && index < size) {
            char b = bytes.get(index / 8);
            return ((b >> (index % 8)) & 1);
        }
        return -1;
    }

    public static BitArray parseBits(String bits) {
        BitArray byteArr = new BitArray();
        for (char c : bits.toCharArray()) {
            byteArr.appendbit(c == '1' ? 1 : 0);
        }
        return byteArr;
    }

    public void lengthen() {
        appendbit(0);
        for (int i = size - 2; i >= 0; i--) {
            int b = getBit(i);
            appendbit(b ^ 1);
        }
    }

    public void trimBits(int desiredBits) {
        while (size - 8 >= desiredBits) {
            // Trim bytes.
            bytes.remove(bytes.size() - 1);
            size -= 8;
        }
        if (size - (size % 8) >= desiredBits) {
            // Trim the partial byte if we can
            bytes.remove(bytes.size() - 1);
            size -= size % 8;
        }
        char b = bytes.get(bytes.size() - 1);
        while (size > desiredBits) {
            // Trim bits one by one.
            int shift = size % 8;
            if (shift == 0) {
                shift = 7;
            } else {
                shift--;
            }
            b &= ~(1 << shift);
            size--;
        }
        bytes.set(bytes.size() - 1, b);
    }
    
    public String bitsToString() {
        String str = "";
        for (int i = 0; i < size; i++) {
            str += getBit(i) == 1? "1" : "0";
        }
        return str;
    }

    public String computeCheckSum() {
        if (size % 2 != 0) {
            return this.bitsToString();
        }
        BitArray checksum = new BitArray();
        for (int i = 1; i < size; i += 2) {
            int bit1 = getBit(i);
            int bit2 = getBit(i - 1);
            if (bit1 == bit2) {
                checksum.appendbit(1);
            } else {
                checksum.appendbit(0);
            }
        }
        return checksum.computeCheckSum();
    }
}

public class Day16 extends AocSolver {

    public Day16(String filename) {
        super(filename);
    }

    private String fillDisk(String bits, int size) {
        BitArray bytes = BitArray.parseBits(bits);
        while (bytes.size < size) {
            bytes.lengthen();
        }
        bytes.trimBits(size);
        return bytes.computeCheckSum();
    }

    @Override
    public void solve(Scanner scan) {
        String bits = scan.nextLine();
        scan.close();
        final int SIZE_PART1 = 272;
        final int SIZE_PART2 = 35651584;
        System.out.println("Part 1: " + fillDisk(bits, SIZE_PART1));
        System.out.println("Part 2: " + fillDisk(bits, SIZE_PART2));        
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day16("input16.txt");
        solver.run(argv);
    }    
}

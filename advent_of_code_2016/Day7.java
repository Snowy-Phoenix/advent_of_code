import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Day7 extends AocSolver {

    public Day7(String filename) {
        super(filename);
    }

    private boolean isABBA(String s, int i) {
        return s.charAt(i) == s.charAt(i + 3)
            && s.charAt(i + 1) == s.charAt(i + 2)
            && s.charAt(i) != s.charAt(i + 1);
    }
    private boolean supportsTls(String address) {
        boolean outerTrue = false;
        boolean isInner = false;
        for (int i = 0; i < address.length() - 3; i++) {
            if (address.charAt(i) == '[') {
                isInner = true;
                continue;
            } else if (address.charAt(i) == ']') {
                // Assumes no nesting
                isInner = false;
                continue;
            }
            boolean substringIsABBA = isABBA(address, i);
            if (substringIsABBA && isInner) {
                return false;
            }
            outerTrue |= substringIsABBA && !isInner;
        }
        return outerTrue;
    }

    private boolean isABA(String s, int i) {
        return s.charAt(i) == s.charAt(i + 2)
            && s.charAt(i) != s.charAt(i + 1);
    }
    private List<String> getABAs(String address) {
        List<String> pairs = new ArrayList<>();
        boolean isInner = false;
        for (int i = 0; i < address.length() - 2; i++) {
            if (address.charAt(i) == '[') {
                isInner = true;
                continue;
            }
            if (address.charAt(i) == ']') {
                isInner = false;
                continue;
            }
            if (isInner) {
                continue;
            }
            if (isABA(address, i)) {
                pairs.add("" + address.charAt(i) + address.charAt(i + 1));
            }
        }
        return pairs;
    }
    private boolean hasBAB(List<String> pairs, String address) {
        boolean isInner = false;
        for (int i = 0; i < address.length() - 2; i++) {
            if (address.charAt(i) == '[') {
                isInner = true;
                continue;
            }
            if (address.charAt(i) == ']') {
                isInner = false;
                continue;
            }
            if (!isInner) {
                continue;
            }
            if (isABA(address, i)) {
                for (String pair : pairs) {
                    if (pair.charAt(1) == address.charAt(i)
                        && pair.charAt(0) == address.charAt(i + 1)) {
                            return true;
                        }
                }
            }
        }
        return false;
    }

    private boolean supportsSsl(String address) {
        List<String> pairs = getABAs(address);
        return hasBAB(pairs, address);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> addresses = getLines(scan);
        scan.close();
        int numTlsSupported = 0;
        int numSslSupported = 0;
        for (String address : addresses) {
            numTlsSupported += supportsTls(address) ? 1 : 0;
            numSslSupported += supportsSsl(address) ? 1 : 0;
        }
        System.out.println("Part 1: " + numTlsSupported);
        System.out.println("Part 2: " + numSslSupported);
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day7("input7.txt");
        solver.run(argv);
    }    
}

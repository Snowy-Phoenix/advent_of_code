import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Scanner;

public class Day20 extends AocSolver {

    private class RangeComparator implements Comparator<Range> {
    @Override
    public int compare(Range r1, Range r2) {
        if (r1.min < r2.min) {
            return -1;
        } else if (r1.min > r2.min) {
            return 1;
        }
        return 0;
        }
    }

    private class Range {
        public long min;
        public long max;

        public Range(long min, long max) {
            this.min = min;
            this.max = max;
        }

        public boolean overlaps(Range other) {
            return (min <= other.min && other.min <= max)
                    || (min <= other.max && other.max <= max);
        }
        public boolean overlaps(long n) {
            return (min <= n && n <= max);
        }
        public void add(Range other) {
            this.min = Math.min(other.min, this.min);
            this.max = Math.max(other.max, this.max);
        }
        public Range getNonOverlappingRange(Range other) {
            if (this.max + 1 > other.min - 1) {
                return null;
            }
            return new Range(this.max + 1, other.min - 1);
        }
        public long getLength() {
            return this.max - this.min + 1;
        }

        @Override
        public String toString() {
            return min + "-" + max;
        }
    }

    public Day20(String filename) {
        super(filename);
    }
    public Range parseRange(String str) {
        String[] minmax = str.split("-");
        return new Range(Long.parseLong(minmax[0]),
                         Long.parseLong(minmax[1]));
    }
    public List<Range> parseRanges(List<String> ls) {
        return ls.stream()
                 .map((x) -> parseRange(x))
                 .collect(() -> new ArrayList<>(),
                          (c, e) -> c.add(e),
                          (c1, c2) -> c1.addAll(c2));
    }

    private long getNumUnblockedAddresses(Range blocked, Range other) {
        Range unblockedRange = blocked.getNonOverlappingRange(other);
        if (unblockedRange != null) {
            return unblockedRange.getLength();
        }
        return 0;
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = getLines(scan);
        scan.close();

        List<Range> blockedRanges = parseRanges(lines);
        blockedRanges.sort(new RangeComparator());

        final long MAX_IP = 4294967295L;
        Range blockedRange = new Range(0, 0);
        long unblockedAddresses = 0;
        long minUnblockedAddress = -1;

        for (Range r : blockedRanges) {
            if (!blockedRange.overlaps(r)) {
                long newUnblocked = getNumUnblockedAddresses(blockedRange, r);
                if (newUnblocked > 0 && minUnblockedAddress == -1) {
                    minUnblockedAddress = blockedRange.max + 1;
                }
                unblockedAddresses += newUnblocked;
            }
            blockedRange.add(r);
        }
            
        if (!blockedRange.overlaps(MAX_IP)) {
            unblockedAddresses += MAX_IP - blockedRange.max;
        }
        System.out.println("Part 1: " + minUnblockedAddress);
        System.out.println("Part 2: " + unblockedAddresses);
        
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day20("input20.txt");
        solver.run(argv);
    }        
}

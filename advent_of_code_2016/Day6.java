import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class Day6 extends AocSolver {

    public Day6(String filename) {
        super(filename);
    }

    private void countCharacters(String message, 
                                 List<HashMap<Character, Integer>> counts) {
        for (int i = 0; i < message.length(); i++) {
            HashMap<Character, Integer> iCounts = counts.get(i);
            char c = message.charAt(i);
            if (iCounts.containsKey(c)) {
                iCounts.put(c, iCounts.get(c) + 1);
            } else {
                iCounts.put(c, 1);
            }
        }
    }

    private String getErrorCorrectedMessagePart1(List<HashMap<Character, Integer>> counts) {
        String message = "";
        for (HashMap<Character, Integer> countMap : counts) {
            int max = 0;
            char maxc = 0;
            for (char c : countMap.keySet()) {
                if (countMap.get(c) > max) {
                    max = countMap.get(c);
                    maxc = c;
                }
            }
            message += maxc;
        }
        return message;
    }
    private String getErrorCorrectedMessagePart2(List<HashMap<Character, Integer>> counts) {
        String message = "";
        for (HashMap<Character, Integer> countMap : counts) {
            int min = Integer.MAX_VALUE;
            char minc = 0;
            for (char c : countMap.keySet()) {
                if (countMap.get(c) < min) {
                    min = countMap.get(c);
                    minc = c;
                }
            }
            message += minc;
        }
        return message;
    }
    

    @Override
    public void solve(Scanner scan) {
        List<String> messages = getLines(scan);
        scan.close();
        List<HashMap<Character, Integer>> counts = new ArrayList<>();
        for (int i = 0; i < messages.get(0).length(); i++) {
            counts.add(new HashMap<>());
        }
        for (String message : messages) {
            countCharacters(message, counts);
        }
        System.out.println("Part 1: " + getErrorCorrectedMessagePart1(counts));
        System.out.println("Part 2: " + getErrorCorrectedMessagePart2(counts));
    } 
    public static void main(String[] argv) {
        AocSolver solver = new Day6("input6.txt");
        solver.run(argv);
    }    
}

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Day3 extends AocSolver {

    public Day3(String filename) {
        super(filename);
    }

    private List<Integer> getNumbersList(List<String> lines) {
        final List<Integer> numbers = new ArrayList<>();
        for (String line : lines) {
            List<String> numberStrings = Arrays.asList(line.split(" "));
            numberStrings.stream()
                         .filter((x) -> !x.equals(""))
                         .mapToInt((x) -> Integer.parseInt(x))
                         .collect(() -> numbers,
                                  (c, e) -> c.add(e),
                                  (c1, c2) -> c1.addAll(c2));
        }
        return numbers;
    }

    private void solvePart1(List<Integer> numbers) {
        int totalPossibleTriangles = 0;
        
        int[] triangle = new int[3];

        for (int i = 0; i < numbers.size(); i += 3) {
            triangle[0] = numbers.get(i);
            triangle[1] = numbers.get(i + 1);
            triangle[2] = numbers.get(i + 2);
            Arrays.sort(triangle);
            if (triangle[0] + triangle[1] > triangle[2]) {
                totalPossibleTriangles++;
            }
        }
        System.out.printf("Part 1: %d\n", totalPossibleTriangles);
    }

    private void solvePart2(List<Integer> numbers) {
        int totalPossibleTriangles = 0;
        int[] triangle = new int[3];
        for (int i = 0; i < numbers.size(); i += 9) {
            for (int j = 0; j < 3; j++) {
                triangle[0] = numbers.get(i + j);
                triangle[1] = numbers.get(i + j + 3);
                triangle[2] = numbers.get(i + j + 6);
                Arrays.sort(triangle);
                if (triangle[0] + triangle[1] > triangle[2]) {
                    totalPossibleTriangles++;
                }
            }
        }
        System.out.printf("Part 2: %d\n", totalPossibleTriangles);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> lines = this.getLines(scan);
        scan.close();
        List<Integer> numbers = getNumbersList(lines);
        solvePart1(numbers);
        solvePart2(numbers);
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day3("input3.txt");
        solver.run(argv);
    } 
}

import java.util.HashSet;
import java.util.Set;
import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

public class Day1 extends AocSolver {

    public Day1(String filename) {
        super(filename);
    }

    @Override
    public void solve(Scanner scan) {
        int[][] directions = {{0,1},{1,0},{0,-1},{-1,0}}; // N, E, S, W, using x,y
        int currentDirection = 0;
        int x = 0;
        int y = 0;
        String line = scan.nextLine();
        scan.close();
        String[] steps = line.split(", ");
        Map<Integer, Set<Integer>> visited = new HashMap<>();
        boolean foundDuplicate = false;
        int dupX = 0;
        int dupY = 0;
        
        for (String step : steps) {
            if (step.charAt(0) == 'L') {
                currentDirection = currentDirection - 1 < 0 ? 3 : currentDirection - 1;
            } else if (step.charAt(0) == 'R') {
                currentDirection = (currentDirection + 1) % 4;
            } else {
                System.out.printf("Bad instruction %s\n", step);
                continue;
            }
            
            int count = Integer.parseInt(step.substring(1));
            int[] movement = directions[currentDirection];
            for (; count > 0; count--) {
                x += movement[0];
                y += movement[1];
                if (!foundDuplicate && visited.containsKey(x)) {
                    Set<Integer> y_values = visited.get(x);
                    if (y_values.contains(y)) {
                        foundDuplicate = true;
                        dupX = x;
                        dupY = y;
                    } else {
                        y_values.add(y);
                    }
                } else {
                    HashSet<Integer> y_values = new HashSet<>();
                    y_values.add(y);
                    visited.put(x, y_values);
                }
            }
        }
        System.out.printf("Part 1: %d\n", Math.abs(x) + Math.abs(y));
        System.out.printf("Part 2: %d\n", Math.abs(dupX) + Math.abs(dupY));
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day1("input1.txt");
        solver.run(argv);
    } 
}
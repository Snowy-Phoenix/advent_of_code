import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import java.util.Map;
import java.util.Queue;
import java.util.Scanner;

class Node {
    public final int x;
    public final int y;
    public int steps;
    public Node prev;

    public Node(int x, int y, int steps, Node prev) {
        this.x = x;
        this.y = y;
        this.steps = steps;
        this.prev = prev;
    }

    @Override
    public boolean equals(Object obj1) {
        if (obj1 instanceof Node) {
            return ((Node)obj1).x == this.x && ((Node)obj1).y == this.y;
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = 17;
        hash = hash * 23 + ((Integer)x).hashCode();
        hash = hash * 23 + ((Integer)y).hashCode();
        return hash;
    }
}

public class Day13 extends AocSolver {

    public Day13(String filename) {
        super(filename);
    }

    public boolean isWall(int x, int y, int constant) {
        int a = x*x + 3*x + 2*x*y + y + y*y + constant;
        int parity = 0;
        while (a > 0) {
            parity = parity ^ (a & 1);
            a >>= 1;
        }
        return parity == 1;
    }

    public void traceSteps(Node lastNode, int favouriteNumber) {
        int maxX = 0;
        int maxY = 0;
        Map<Integer, Set<Integer>> nodes = new HashMap<>();
        while (lastNode != null) {
            if (!nodes.containsKey(lastNode.x)) {
                nodes.put(lastNode.x, new HashSet<>());
            }
            nodes.get(lastNode.x).add(lastNode.y);
            maxX = Math.max(lastNode.x, maxX);
            maxY = Math.max(lastNode.y, maxY);
            lastNode = lastNode.prev;
        }
        String grid = "";
        for (int y = 0; y <= maxY; y++) {
            for (int x = 0; x <= maxX; x++) {
                if (nodes.containsKey(x)) {
                    if (nodes.get(x).contains(y)) {
                        grid += "O";
                        continue;
                    }
                } if (isWall(x, y, favouriteNumber)) {
                    grid += "#";
                    continue;
                }
                grid += " ";
            }
            grid += "\n";
        }
        System.out.println(grid);
    }

    @Override
    public void solve(Scanner scan) {
        int favouriteNumber = Integer.parseInt(scan.nextLine());
        scan.close();

        int[][] vectors = {{1,0}, {0,1}, {-1,0}, {0,-1}};
        Node goal = new Node(31, 39, 0, null);
        Queue<Node> queue = new ArrayDeque<>();
        Set<Node> visited = new HashSet<>();

        Node start = new Node(1, 1, 0, null);
        visited.add(start);
        queue.add(start);
        
        int reachable = 0;
        while (!queue.isEmpty()) {
            Node currentNode = queue.remove();
            if (currentNode.steps <= 50) {
                reachable++;
            }
            if (currentNode.equals(goal)) {
                System.out.println("Part 1: " + currentNode.steps);
                break;
            }
            for (int[] v : vectors) {
                int newX = currentNode.x + v[0];
                int newY = currentNode.y + v[1];
                if (newX < 0 || newY < 0) {
                    continue;
                }
                if (isWall(newX, newY, favouriteNumber)) {
                    continue;
                }
                Node newNode = new Node(newX, newY, currentNode.steps + 1, currentNode);
                if (visited.contains(newNode)) {
                    continue;
                }
                visited.add(newNode);
                queue.add(newNode);
            }
        }
        System.out.println("Part 2: " + reachable);
        
    } 

    public static void main(String[] argv) {
        AocSolver solver = new Day13("input13.txt");
        solver.run(argv);
    }    
}

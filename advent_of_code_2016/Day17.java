import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;
import java.security.MessageDigest;


class Node {
    public final int x;
    public final int y;
    public int steps;
    public String path;

    public Node(int x, int y, int steps, String path) {
        this.x = x;
        this.y = y;
        this.steps = steps;
        this.path = path;
    }

    public int heuristic(Node goal) {
        return Math.abs(goal.x - this.x) + Math.abs(goal.y - this.y) + steps;
    }

    public boolean isCoordsEqual(Node other) {
        return other.x == this.x && other.y == this.y;
    }
}

public class Day17 extends AocSolver {

    private String bytesToHexString(byte[] bytes) {
        String result = "";
        for (byte b : bytes) {
            int i = (b & 0xff) | 0x100;
            result += Integer.toHexString(i).substring(1);
        }
        return result;
    }
    private boolean isLocked(char c) {
        return !('b' <= c && c <= 'f');
    }

    public Day17(String filename) {
        super(filename);
    }

    @Override
    public void solve(Scanner scan) {
        String passcode = scan.nextLine();
        scan.close();
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
        } catch (Exception e) {
            System.err.println(e);
            return;
        }

        int[][] vectors = {{-1,0}, {1,0}, {0,-1}, {0,1}};
        String[] directions = {"U", "D", "L", "R"};
        Node goal = new Node(3, 3, 0, "");
        Queue<Node> queue = new ArrayDeque<>();
        
        Node start = new Node(0, 0, 0, passcode);
        queue.add(start);

        String shortestPath = "";
        int longestPathLength = 0;
        while (!queue.isEmpty()) {
            Node currentNode = queue.remove();
            if (currentNode.isCoordsEqual(goal)) {
                String path = currentNode.path.substring(passcode.length());
                if (shortestPath.length() == 0) {
                    shortestPath = path;
                }
                longestPathLength = Math.max(longestPathLength, path.length());
                continue;
            }
            String hash = currentNode.path;
            byte[] digest = md.digest(hash.getBytes());
            String doors = bytesToHexString(digest).substring(0, vectors.length);

            for (int i = 0; i < vectors.length; i++) {
                if (isLocked(doors.charAt(i))) {
                    continue;
                }
                int[] v = vectors[i];
                int newX = currentNode.x + v[0];
                int newY = currentNode.y + v[1];
                if (newX < 0 || newY < 0 || newX > 3 || newY > 3) {
                    continue;
                }
                String direction = directions[i];
                Node newNode = new Node(newX, newY, currentNode.steps + 1, hash + direction);
                queue.add(newNode);
            }
        }
        System.out.println("Part 1: " + shortestPath);
        System.out.println("Part 2: " + longestPathLength);
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day17("input17.txt");
        solver.run(argv);
    }        
}

import java.util.Scanner;

class LinkedNode {

    public LinkedNode next;
    public LinkedNode prev;
    public int id;

    public LinkedNode(int id) {
        this.id = id;
        this.next = this;
        this.prev = this;
    }

    public static void remove(LinkedNode node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
        node.next = null;
        node.prev = null;
    }
    public static void add(LinkedNode to, LinkedNode newNode) {
        newNode.next = to.next;
        newNode.prev = to;
        to.next.prev = newNode;
        to.next = newNode;
    }
}

public class Day19 extends AocSolver {

    public Day19(String filename) {
        super(filename);
    }

    private int solvePart1(int elves) {
        LinkedNode currNode = new LinkedNode(1);
        for (int id = 2; id <= elves; id++) {
            LinkedNode.add(currNode, new LinkedNode(id));
            currNode = currNode.next;
        }
        currNode = currNode.next;
        while (true) {
            LinkedNode.remove(currNode.next);
            if (currNode.next == null) {
                break;
            }
            currNode = currNode.next;
        }
        return currNode.id;
    }

    private int solvePart2(int elves) {
        LinkedNode currNode = new LinkedNode(1);
        for (int id = 2; id <= elves; id++) {
            LinkedNode.add(currNode, new LinkedNode(id));
            currNode = currNode.next;
        }
        currNode = currNode.next;

        LinkedNode oppositeNode = currNode;
        int distance = 0;
        while (distance < elves / 2) {
            oppositeNode = oppositeNode.next;
            distance++;
        }

        while (elves > 0) {
            LinkedNode nextNode = oppositeNode.next;
            LinkedNode.remove(oppositeNode);
            oppositeNode = nextNode;
            if (currNode.next == null) {
                break;
            }
            currNode = currNode.next;
            distance--;
            elves--;
            while (distance < elves / 2) {
                oppositeNode = oppositeNode.next;
                distance++;
            }
        }
        return currNode.id;
    }

    @Override
    public void solve(Scanner scan) {
        int elves = Integer.parseInt(scan.nextLine());
        scan.close();
        // for (int i = 1; i <= 100; i++) {
        //     System.out.printf("%d: %d\n",i,  solvePart2(i));
        // }
        System.out.println("Part 1: " + solvePart1(elves));
        System.out.println("Part 2: " + solvePart2(elves));
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day19("input19.txt");
        solver.run(argv);
    }        
}

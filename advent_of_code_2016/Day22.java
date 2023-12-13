import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.List;
import java.util.Scanner;

class Node {
    String file;
    int x;
    int y;
    int size;
    int used;
    int available;
    
    public Node(String file, int size, int used, int available) {
        this.file = file;
        this.size = size;
        this.used = used;
        this.available = available;
        parseFile();
    }
    private void parseFile() {
        String[] words = file.split("-");
        x = Integer.parseInt(words[1].substring(1));
        y = Integer.parseInt(words[2].substring(1));
    }

    private static List<String> getWords(String line) {
        List<String> words = Arrays.asList(line.split(" "));
        words = words.stream()
                     .filter((x) -> x.length() > 0)
                     .collect(() -> new ArrayList<>(),
                              (c, e) -> c.add(e),
                              (c1, c2) -> c1.addAll(c2));
        return words;
    }

    public static Node parseNode(String line) {
        List<String> words = getWords(line);
        String file = words.get(0);
        int size = Integer.parseInt(words.get(1).substring(0, words.get(1).length() - 1));
        int used = Integer.parseInt(words.get(2).substring(0, words.get(2).length() - 1));
        int available = Integer.parseInt(words.get(3).substring(0, words.get(3).length() - 1));
        return new Node(file, size, used, available);
    }

    public boolean isViable(Node other) {
        // self is A. Other is B.
        if (this.used > 0) {
            if (!this.file.equals(other.file)) {
                if (this.used <= other.available) {
                    return true;
                }
            }
        }
        return false;
    }

    @Override
    public String toString() {
        return "x" + x + "y" + y + " " + size + " " + used + " " + available;
    }
}

class Coords {
    public int x;
    public int y;
    public Coords(int x, int y) {
        this.x = x;
        this.y = y;
    }
    @Override
    public boolean equals(Object obj1) {
        if (obj1 instanceof Coords) {
            return ((Coords)obj1).x == this.x && ((Coords)obj1).y == this.y;
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
    @Override
    public String toString() {
        return "(" + this.x + ", " + this.y + ")";
    }
}

class Grid {

    private class SearchNode {
        public Coords coordsBox;
        public Coords coordsPlayer;
        public int steps;
        public SearchNode prev;

        public SearchNode(Coords coordsBox, Coords coordsPlayer, int steps, SearchNode prev) {
            this.coordsBox = coordsBox;
            this.coordsPlayer = coordsPlayer;
            this.steps = steps;
            this.prev = prev;
        }
    }
    
    public char[][] nodes;
    public Coords player;
    public Coords box;
    public Coords goal;

    public static Grid generateGrid(Set<Node> movable, Set<Node> carrying, int lenx, int leny) {
        lenx++; // 0 to lenx inclusive
        leny++; // 0 to leny inclusive.
        Grid g = new Grid();
        Set<Coords> movableCoords = movable.stream()
                                           .map((c) -> new Coords(c.x, c.y))
                                           .collect(() -> new HashSet<>(),
                                                    (c, e) -> c.add(e),
                                                    (c1, c2) -> c1.addAll(c2));
        Set<Coords> carryingCoords = carrying.stream()
                                           .map((c) -> new Coords(c.x, c.y))
                                           .collect(() -> new HashSet<>(),
                                                    (c, e) -> c.add(e),
                                                    (c1, c2) -> c1.addAll(c2));
        g.nodes = new char[leny][lenx];
        for (int x = 0; x < lenx; x++) {
            for (int y = 0; y < leny; y++) {
                Coords c = new Coords(x, y);
                if (movableCoords.contains(c)) {
                    g.nodes[y][x] = '.';
                } else if (carryingCoords.contains(c)) {
                    g.nodes[y][x] = '.';
                    g.player = new Coords(x, y);
                } else {
                    g.nodes[y][x] = '#';
                }
            }
        }
        return g;
    }

    @Override
    public String toString() {
        String str = "";
        for (int y = 0; y < nodes.length; y++) {
            char[] row = nodes[y];
            for (int x = 0; x < row.length; x++) {
                char c = row[x];
                if (player.x == x && player.y == y) {
                    str += "_";
                } else if (box != null && box.x == x && box.y == y) {
                    str += "O";
                } else if (goal != null && x == goal.x && y == goal.x) {
                    str += "G";
                } else {
                    str += c;
                }
            }
            str += "\n";
        }
        return str;
    }

    public boolean collidingWall(int x, int y) {
        if (0 <= y && y < nodes.length) {
            if (0 <= x && x < nodes[y].length) {
                return nodes[y][x] == '#';
            }
        }
        return true;
    }
    public boolean collidingWall(Coords c) {
        return collidingWall(c.x, c.y);
    }
    
    public List<Coords> getMoves(Coords box) {
        int[][] vectors = {{1,0}, {-1,0}, {0,1}, {0,-1}};
        List<Coords> moves = new ArrayList<>();
        for (int[] v : vectors) {
            Coords c = new Coords(box.x + v[0], box.y + v[1]);
            if (!collidingWall(c)) {
                moves.add(c);
            }
        }
        return moves;
    }
    public int getDistance(Coords to, Coords from, Coords box) {
        Queue<Coords> nextQueue = new ArrayDeque<>();
        Queue<Coords> currQueue = new ArrayDeque<>();
        Set<Coords> visited = new HashSet<>();
        nextQueue.add(from);
        visited.add(from);
        int steps = 0;
        while (!nextQueue.isEmpty()) {
            currQueue.addAll(nextQueue);
            nextQueue.clear();
            while (!currQueue.isEmpty()) {
                Coords currCoords = currQueue.remove();
                if (currCoords.equals(to)) {
                    return steps;
                } else if (currCoords.equals(box)) {
                    continue;
                }
                List<Coords> nextMoves = getMoves(currCoords);
                for (Coords m : nextMoves) {
                    if (!visited.contains(m)) {
                        nextQueue.add(m);
                        visited.add(m);
                    }
                }
            }
            steps++;
        }
        return -1;
    }

    public int findOptimalSolution(Coords box, Coords goal) {
        this.goal = goal;
        this.box = box;

        // Uniform cost search
        Queue<SearchNode> queue = new PriorityQueue<>((x, y) -> x.steps - y.steps);
        Set<Coords> boxVisited = new HashSet<>();

        queue.add(new SearchNode(box, player, 0, null));
        while (!queue.isEmpty()) {
            SearchNode n = queue.remove();
            if (n.coordsBox.equals(goal)) {
                return n.steps;
            }
            if (boxVisited.contains(n.coordsBox)) {
                continue;
            } else {
                boxVisited.add(n.coordsBox);
            }
            List<Coords> boxMoves = getMoves(n.coordsBox);
            for (Coords move : boxMoves) {
                int steps = getDistance(move, n.coordsPlayer, n.coordsBox);
                if (steps == -1) {
                    continue;
                }
                SearchNode newNode = new SearchNode(move, n.coordsBox, n.steps + steps + 1, n);
                queue.add(newNode);
            }
        }
        return -1;
    }

    public void play() {
        Scanner input = new Scanner(System.in);
        int moves = 0;
        Coords playerBeginning = player;
        player = new Coords(player.x, player.y);
        box = new Coords(nodes[0].length - 1, 0);
        goal = new Coords(0, 0);
        
        while (true) {
            System.out.println(this);
            if (box.x == 0 && box.y == 0) {
                System.out.println("Part 2: " + moves);
                break;
            }
            String move = input.nextLine();

            if ("w".equals(move)) {
                if (!collidingWall(player.x, player.y - 1)) {
                    player.y -= 1;
                    moves++;
                    if (player.equals(box)) {
                        box.y += 1;
                    }
                }
            } else if ("s".equals(move)) {
                if (!collidingWall(player.x, player.y + 1)) {
                    player.y += 1;
                    moves++;
                    if (player.equals(box)) {
                        box.y -= 1;
                    }
                }
            } else if ("d".equals(move)) {
                if (!collidingWall(player.x + 1, player.y)) {
                    player.x += 1;
                    moves++;
                    if (player.equals(box)) {
                        box.x -= 1;
                    }
                }
            } else if ("a".equals(move)) {
                if (!collidingWall(player.x - 1, player.y)) {
                    player.x -= 1;
                    moves++;
                    if (player.equals(box)) {
                        box.x += 1;
                    }
                }
            }
        }
        input.close();
        player = playerBeginning;
    }
}

public class Day22 extends AocSolver {

    public Day22(String filename) {
        super(filename);
    }
    private List<Node> parseNodes(List<String> lines) {
        List<Node> ls = new ArrayList<>();
        for (int i = 2; i < lines.size(); i++) {
            ls.add(Node.parseNode(lines.get(i)));
        }
        return ls;
    }
    
    @Override
    public void solve(Scanner scan) {
        List<String> lines = getLines(scan);
        scan.close();
        List<Node> nodes = parseNodes(lines);
        int viableNodes = 0;
        Set<Node> movableNode = new HashSet<>();
        Set<Node> carryingNode = new HashSet<>();
        int maxX = 0;
        int maxY = 0;
        for (Node n1 : nodes) {
            for (Node n2 : nodes) {
                if (n1.isViable(n2)) {
                    viableNodes++;
                    movableNode.add(n1);
                    carryingNode.add(n2);
                }
            }
            maxX = Math.max(maxX, n1.x);
            maxY = Math.max(maxY, n1.y);
        }
        System.out.println("Part 1: " + viableNodes);
        Grid g = Grid.generateGrid(movableNode, carryingNode, maxX, maxY);
        int solution = g.findOptimalSolution(new Coords(maxX, 0), new Coords(0,0));
        System.out.println("Part 2: " + solution);
    }

    public static void main(String[] argv) {
        AocSolver solver = new Day22("input22.txt");
        solver.run(argv);
    }        
}

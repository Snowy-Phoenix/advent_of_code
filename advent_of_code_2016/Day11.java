import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import java.util.Map;
import java.util.Queue;
import java.util.List;
import java.util.Scanner;



class Building {
    private List<Item> items;
    private List<List<Item>> building;
    public int floors;
    public int elevator;

    public Building(int floors) {
        this.items = new ArrayList<>();
        this.building = new ArrayList<>();
        this.floors = floors;
        this.elevator = 0;
        for (int i = 0; i < floors; i++) {
            this.building.add(new ArrayList<>());
        }
    }
    public List<Item> getFloor(int floorNum) {
        if (0 <= floorNum && floorNum < floors) {
            return building.get(floorNum);
        }
        return null;
    }
    public boolean isComplete() {
        return this.items.size() == building.get(floors - 1).size();
    }
    public void addItem(Item it, int floor) {
        building.get(floor).add(it);
        items.add(it);
    }

    @Override
    public String toString() {
        String str = "";
        for (int i = building.size() - 1; i >= 0; i--) {
            str += "F" + (i + 1);
            if (i + 1 == elevator + 1) {
                str += "\tE";
            } else {
                str += "\t.";
            }
            List<Item> floor = building.get(i);
            for (int j = 0; j < items.size(); j++) {
                Item it = items.get(j);
                if (floor.contains(it)) {
                    str += "\t" + it;
                } else {
                    str += "\t.";
                }
            }
            str += "\n";
        }
        return str;
    }

    @Override
    public Building clone() {
        Building newBuilding = new Building(floors);
        newBuilding.elevator = this.elevator;
        for (Item it : this.items) {
            newBuilding.items.add(it);
        }
        for (int floorNum = 0; floorNum < floors; floorNum++) {
            List<Item> newFloor = newBuilding.building.get(floorNum);
            List<Item> oldFloor = this.building.get(floorNum);
            for (Item it : oldFloor) {
                newFloor.add(it);
            }
        }
        return newBuilding;
    }

    public long getFloorBitmap() {
        // Could optimise so that objects use log2(floor) bits.
        if (floors * items.size() + floors > 64) {
            System.out.println("Bitmap will exceed 64 bits.");
            return 0;
        }
        long bitmap = 0;
        int totalItems = items.size() + 1;
        for (int fl = 0; fl < floors; fl++) {
            List<Item> currFloor = building.get(fl);
            for (int i = 0; i < totalItems; i++) {
                if (i == totalItems - 1) {
                    if (elevator == fl) {
                        bitmap |= (long)1 << (fl*totalItems + i);
                    }
                }
                else if (currFloor.contains(items.get(i))) {
                    bitmap |= (long)1 << (fl*totalItems + i);
                }
            }
        }
        return bitmap;
    }
}
class Move {
    public List<Item> items;
    public Building floorPlan;
    public int movement; // 1 for up, -1 for down.
    public Move prev;

    public Move(List<Item> items, Building floorPlan, int movement, Move prev) {
        this.floorPlan = floorPlan;
        this.movement = movement;
        this.prev = prev;
        this.items = new ArrayList<>();
        for (Item it : items) {
            this.items.add(it);
        }
    }

    public boolean contains(Item it) {
        return items.contains(it);
    }
    public Building executeMove() {
        Building newBuilding = floorPlan.clone();
        List<Item> currFloor = newBuilding.getFloor(newBuilding.elevator);
        newBuilding.elevator += movement;
        List<Item> nextFloor = newBuilding.getFloor(newBuilding.elevator);
        for (Item it : items) {
            currFloor.remove(it);
            nextFloor.add(it);
        }
        return newBuilding;
    }
    public static boolean isLegal(Building b, int movement, List<Item> items) {
        int nextFloorNum = b.elevator + movement;
        List<Item> currFloor = b.getFloor(b.elevator);
        List<Item> nextFloor = b.getFloor(nextFloorNum);
        if (nextFloor == null || currFloor == null) {
            return false;
        }
        for (Item it : items) {
            if (!it.canMove(currFloor, items) || !it.isLegal(nextFloor, items)) {
                return false;
            }
        }
        return true;
    }
    public static List<Move> generateMoves(Building b, Move prev) {
        List<Move> possibleMoves = new ArrayList<>();
        List<Item> floorItems = b.getFloor(b.elevator);
        List<Item> elevatorItems = new ArrayList<>();
        int[] upOrDownPossibilities = {1, -1};
        for (int firstMove = 0; firstMove < floorItems.size(); firstMove++) {
            Item item1 = floorItems.get(firstMove);
            for (int upOrDown : upOrDownPossibilities) {
                elevatorItems.add(item1);
                if (Move.isLegal(b, upOrDown, elevatorItems)) {
                    possibleMoves.add(new Move(elevatorItems, b, upOrDown, prev));
                }
                for (int secMove = firstMove + 1; secMove < floorItems.size(); secMove++) {
                    Item item2 = floorItems.get(secMove);
                    elevatorItems.add(item2);
                    if (Move.isLegal(b, upOrDown, elevatorItems)) {
                        possibleMoves.add(new Move(elevatorItems, b, upOrDown, prev));
                    }
                    elevatorItems.remove(item2);
                }
                elevatorItems.remove(item1);
            }
        }
        return possibleMoves;
    }
}
abstract class Item {
    String displayName;

    abstract boolean isLegal(List<Item> floor, List<Item> items);
    abstract boolean canMove(List<Item> floor, List<Item> items);

    @Override
    public String toString() {
        return displayName;
    }
}
class Microchip extends Item {
    Generator pair;

    @Override
    boolean isLegal(List<Item> floor, List<Item> items) {
        if (floor.contains(pair) || items.contains(pair)) {
            // Shielded microchip
            return true;
        }
        for (Item it : floor) {
            if (it instanceof Generator) {
                // Floor contains another generator.
                return false;
            }
        }
        for (Item it : items) {
            if (it instanceof Generator) {
                // Elevator contains another generator.
                return false;
            }
        }
        return true;
    }

    @Override
    boolean canMove(List<Item> floor, List<Item> items) {
        return true;
    }
}
class Generator extends Item {
    Microchip pair;

    @Override
    boolean isLegal(List<Item> floor, List<Item> items) {
        // Assumes floor is in a legal state.
        for (Item it : floor) {
            if (it instanceof Microchip) {
                Microchip chip = (Microchip)it;
                if (chip.pair == this) {
                    // Correct pair.
                    continue;
                }
                if (!floor.contains(chip.pair) && !items.contains(chip.pair)) {
                    // Do not move the generator in a floor with a chip that has no
                    // partner
                    return false;
                }
            }
        }
        return true;
    }

    @Override
    boolean canMove(List<Item> floor, List<Item> items) {
        if (items.contains(pair)) {
            // Moving with the pair
            return true;
        } else if (floor.contains(pair)) {
            for (Item it : floor) {
                if (it instanceof Generator) {
                    if (it != this && !items.contains(it)) {
                        // Leaving the microchip without protection.
                        return false;
                    }
                }
            }
        }
        // floor contains no other generators or pair is not present.
        return true;
    }
}

public class Day11 extends AocSolver {

    public Day11(String filename) {
        super(filename);
    }

    private void parseLine(String line, int floorNum, Building b, 
            Map<String, Generator> generators, Map<String, Microchip> microchips) {
        String[] words = line.split(" ");
        int offset = 1;
        while (offset < words.length) {
            String name = words[offset - 1];
            if (words[offset].startsWith("generator")) {
                Generator g = new Generator();
                g.displayName = (name.substring(0, 1) + "g").toUpperCase();
                generators.put(name, g);
                b.addItem(g, floorNum);
            } else if (words[offset].startsWith("microchip")) {
                Microchip m = new Microchip();
                m.displayName = (name.substring(0, 1) + "m").toUpperCase();
                String[] n = name.split("-");
                microchips.put(n[0], m);
                b.addItem(m, floorNum);
            }
            offset += 1;
        }
    }

    private void linkPairs(Map<String, Generator> generators, 
                           Map<String, Microchip> microchips) {
        for (String name : generators.keySet()) {
            generators.get(name).pair = microchips.get(name);
            microchips.get(name).pair = generators.get(name);
        }
    }
    private Building parseBuilding(List<String> floors) {
        Building b = new Building(floors.size());
        Map<String, Generator> generators = new HashMap<>();
        Map<String, Microchip> microchips = new HashMap<>();
        for (int i = 0; i < floors.size(); i++) {
            parseLine(floors.get(i), i, b, generators, microchips);
        }
        linkPairs(generators, microchips);
        return b;
    }

    private int getMinMoves(Building b) {
        Queue<Move> fringe = new ArrayDeque<>();
        Set<Long> visited = new HashSet<>();
        List<Move> moves = Move.generateMoves(b, null);
        visited.add(b.getFloorBitmap());
        fringe.addAll(moves);
        Move nextMove = null;
        boolean solutionFound = false;
        while (!fringe.isEmpty()) {
            nextMove = fringe.remove();
            Building currBuilding = nextMove.executeMove();
            if (currBuilding.isComplete()) {
                // Solution found!
                solutionFound = true;
                break;
            }
            moves = Move.generateMoves(currBuilding, nextMove);
            for (Move m : moves) {
                Building nextBuilding = m.executeMove();
                if (visited.contains(nextBuilding.getFloorBitmap())) {
                    continue;
                } else {
                    fringe.add(m);
                    visited.add(nextBuilding.getFloorBitmap());
                }
            }
        }
        if (solutionFound) {
            int steps = 0;
            while (nextMove != null) {
                steps++;
                nextMove = nextMove.prev;
            }
            return steps;
        }
        return 0;
    }

    public void addItemsFromPart2(Building b) {
        Generator g1 = new Generator();
        Generator g2 = new Generator();
        g1.displayName = "EG";
        g2.displayName = "DG";
        Microchip m1 = new Microchip();
        Microchip m2 = new Microchip();
        m1.displayName = "EM";
        m2.displayName = "DM";
        g1.pair = m1;
        g2.pair = m2;
        m1.pair = g1;
        m2.pair = g2;
        b.addItem(g1, 0);
        b.addItem(m1, 0);
        b.addItem(g2, 0);
        b.addItem(g2, 0);
    }

    @Override
    public void solve(Scanner scan) {
        List<String> floors = getLines(scan);
        scan.close();
        Building building = parseBuilding(floors);
        int minMoves = getMinMoves(building);
        System.out.println("Part 1: " + minMoves);

        addItemsFromPart2(building);

        minMoves = getMinMoves(building);
        System.out.println("Part 2: " + minMoves);
    } 

    public static void main(String[] argv) {
        AocSolver solver = new Day11("input11.txt");
        solver.run(argv);
    }    
}

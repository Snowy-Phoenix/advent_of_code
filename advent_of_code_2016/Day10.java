import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;

import java.util.Map;
import java.util.Queue;
import java.util.List;
import java.util.Scanner;


public class Day10 extends AocSolver {

    private abstract class Worker {
        public int id;
        public Worker low;
        public Worker high;
        public List<Integer> hand = new ArrayList<>();
        
        public abstract void receive(int microchip);
        public abstract void give();
        
    }

    private class Robot extends Worker {

        public Robot(int id) {
            this.id = id;
        }

        public void setLow(Worker w) {
            low = w;
        }
        public void setHigh(Worker w) {
            high = w;
        }

        @Override
        public void receive(int microchip) {
            hand.add(microchip);
            if (hand.size() == 2) {
                if ((hand.get(0) == 17 && hand.get(1) == 61)
                    || (hand.get(1) == 17 && hand.get(0) == 61)) {
                    alertSolution(this);
                }
                taskQueue.add(this);
            }
        }

        @Override
        public void give() {
            if (low != null && high != null && hand.size() == 2) {
                low.receive(Math.min(hand.get(0), hand.get(1)));
                high.receive(Math.max(hand.get(0), hand.get(1)));
                hand.clear();
            }
        }

    }

    private class Output extends Worker {

        public Output(int id) {
            this.id = id;
        }

        @Override
        public void receive(int microchip) {
            hand.add(microchip);
        }

        @Override
        public void give() {
            return;
        }
    }

    public Queue<Worker> taskQueue = new ArrayDeque<>();

    public Day10(String filename) {
        super(filename);
    }

    private void alertSolution(Worker w) {
        System.out.println("Part 1: " + w.id);
    }

    private Robot getBot(int id, Map<Integer, Robot> robots) {
        if (!robots.containsKey(id)) {
            robots.put(id, new Robot(id));
        }
        return robots.get(id);
    }
    private Output getOutput(int id, Map<Integer, Output> outputs) {
        if (!outputs.containsKey(id)) {
            outputs.put(id, new Output(id));
        }
        return outputs.get(id);
    }
    private Worker createWorkerFromString(String type, String id, 
            Map<Integer, Robot> robots, Map<Integer, Output> outputs) {
        if (type.equals("bot")) {
            return getBot(Integer.parseInt(id), robots);
        } else {
            return getOutput(Integer.parseInt(id), outputs);
        }
    }

    private void parseLine(String line, Map<Integer, Robot> robots, 
                          Map<Integer, Output> outputs) {
        String[] words = line.split(" ");
        if (words[0].equals("value")) {
            int literal = Integer.parseInt(words[1]);
            Worker w = createWorkerFromString(words[4], words[5], robots, outputs);
            w.receive(literal);
        } else if (words[0].equals("bot")) {
            Robot giver = getBot(Integer.parseInt(words[1]), robots);
            Worker low = createWorkerFromString(words[5], words[6], robots, outputs);
            Worker high = createWorkerFromString(words[10], words[11], robots, outputs);
            giver.setLow(low);
            giver.setHigh(high);;
        } else {
            System.err.println("Unable to parse line " + line);
        }
    }

    @Override
    public void solve(Scanner scan) {
        List<String> instructions = getLines(scan);
        scan.close();
        Map<Integer, Robot> robots = new HashMap<>();
        Map<Integer, Output> outputs = new HashMap<>();
        for (String line : instructions) {
            parseLine(line, robots, outputs);
        }
        while (!taskQueue.isEmpty()) {
            Worker w = taskQueue.remove();
            w.give();
        }
        int outputMultiplied = 1;
        for (int i = 0; i < 3; i++) {
            List<Integer> outputBin = outputs.get(i).hand;
            for (int j : outputBin) {
                outputMultiplied *= j;
            }
        }
        System.out.println("Part 2: " + outputMultiplied);
    } 

    public static void main(String[] argv) {
        AocSolver solver = new Day10("input10.txt");
        solver.run(argv);
    }    
}

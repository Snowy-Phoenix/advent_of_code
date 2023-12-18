import {readFileSync} from "fs";

type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT";

const DIRECTIONS: Direction[] = ["UP", "DOWN", "LEFT", "RIGHT"];
const DIRECTION_VECTORS: {[D in Direction]: Vector;} 
        = {"UP": {row: -1, col: 0}, "DOWN": {row: 1, col: 0}, 
           "LEFT": {row: 0, col: -1}, "RIGHT": {row: 0, col: 1}}

interface PQNode {
    index: number;

    getPriority(): number
    updatePriority(priority: number): void
}

interface Vector {
    row: number;
    col: number;
}

class Coordinates implements Vector {
    row: number;
    col: number;

    constructor(row: number, col: number) {
        this.row = row;
        this.col = col;
    }

    add(other: Vector): Coordinates {
        return new Coordinates(this.row + other.row, this.col + other.col);
    }
    subtract(other: Vector): Coordinates {
        return new Coordinates(this.row - other.row, this.col - other.col);
    }
}

class SearchNode implements PQNode {

    distance: number;
    index: number;

    coordinates: Coordinates;
    lastDirection: Direction;
    lastDirectionCount: number;
    heuristic: (v: Vector) => number;
    prev: SearchNode | undefined;

    constructor(distance: number, coords: Vector, lastDirection: Direction,
                lastDirectionCount: number, 
                heuristic?: (v: Vector) => number, prev?: SearchNode) {
        this.distance = distance;
        this.lastDirection = lastDirection;
        this.lastDirectionCount = lastDirectionCount;
        this.prev = prev;
        if (heuristic === undefined) {
            this.heuristic = (v) => 0;
        } else {
            this.heuristic = heuristic;
        }
        if (coords instanceof Coordinates) {
            this.coordinates = coords;
        } else {
            this.coordinates = new Coordinates(coords.row, coords.col);
        }
    }

    getPriority(): number {
        return this.distance + this.heuristic(this.coordinates);
    }
    updatePriority(distance: number): void {
        this.distance = distance;
    }

    generateNextMoves(getCost: (v: Vector) => number | undefined): SearchNode[] {
        let nextMoves: SearchNode[] = [];
        let currVector = DIRECTION_VECTORS[this.lastDirection];
        
        for (let direction of DIRECTIONS) {
            let nextDirectionCount = 1;
            if (direction === this.lastDirection) {
                if (this.lastDirectionCount == 3) {
                    continue;
                }
                nextDirectionCount = this.lastDirectionCount + 1;
            }
            let vector = DIRECTION_VECTORS[direction];
            if (vector.row === -currVector.row && vector.col === -currVector.col) {
                // Cannot go backwards.
                continue;
            }

            let nextCoords = this.coordinates.add(vector);
            let cost = getCost(nextCoords);
            if (cost === undefined) {
                continue;
            }
            nextMoves.push(new SearchNode(this.distance + cost, 
                                          nextCoords, direction, 
                                          nextDirectionCount, this.heuristic, this));
        }
        return nextMoves;
    }
    hash(): string {
        return this.lastDirection + this.lastDirectionCount + 
               "(" + this.coordinates.row + "," + this.coordinates.col + ")"
    }
    visitedHashes(): string[] {
        // Optimisation: If we expand the tile at currStepCount < maxStepCount using dijkstra's, 
        // then this must also be the optimal for currStepCount <= steps <= maxStepCount.
        // This is because for all those steps, the tiles they could visit is a subset of
        // the current step count.
        
        let hashes: string[] = [];
        let coordString = "(" + this.coordinates.row + "," + this.coordinates.col + ")";
        for (let i = this.lastDirectionCount; i <= 3; i++) {
            hashes.push(this.lastDirection + i + coordString);
        }
        return hashes;
    }
}

class PriorityQueue<T extends PQNode> {
    queue: T[]
    length: number;

    constructor() {
        this.queue = [];
        this.length = 0;
    }

    private swap(i1: number, i2: number): void {
        let c = this.queue[i1];
        this.queue[i1] = this.queue[i2];
        this.queue[i2] = c;
        this.queue[i1].index = i1;
        this.queue[i2].index = i2;
    }
    private siftUp(nodeIndex: number): void {
        if (nodeIndex < 0 || nodeIndex >= this.length) {
            return;
        }
        let node = this.queue[nodeIndex];
        while (nodeIndex > 0) {
            let nextIndex = Math.ceil(nodeIndex / 2) - 1;
            if (node.getPriority() < this.queue[nextIndex].getPriority()) {
                this.swap(nextIndex, nodeIndex);
                nodeIndex = nextIndex;
            } else {
                break;
            }
        }
    }
    private siftDown(nodeIndex: number): void {
        if (nodeIndex < 0 || nodeIndex >= this.length) {
            return;
        }
        let currPriority = this.queue[nodeIndex].getPriority();
        while (true) {
            let nextIndex = this.minPriority(currPriority, nodeIndex*2 + 1, nodeIndex*2 + 2);
            if (nextIndex == -1) {
                break;
            }
            this.swap(nodeIndex, nextIndex);
            nodeIndex = nextIndex;
        }
    }
    push(node: T): void {
        this.queue.push(node);
        let nodeIndex = this.length;
        node.index = nodeIndex;
        this.length++;
        this.siftUp(nodeIndex);
        
    }
    private minPriority(currPriority: number, i1: number, i2: number): number {
        let n1 = this.queue[i1];
        let n2 = this.queue[i2];
        let min = currPriority;
        let minIndex = -1;
        if (n1 !== undefined) {
            if (min > n1.getPriority()) {
                minIndex = i1;
                min = n1.getPriority()
            }
        }
        if (n2 !== undefined) {
            if (min > n2.getPriority()) {
                minIndex = i2;
                min = n2.getPriority();
            }
        }
        return minIndex;
    }
    pop(): T | undefined {
        if (this.length === 0) {
            return undefined;
        }
        this.swap(0, this.length - 1);
        let output = this.queue.pop();
        this.length--;
        this.siftDown(0);
        return output;
    }
    update(node: T, priority: number): void {
        let current = node.getPriority();
        node.updatePriority(priority);
        if (priority < current) {
            this.siftUp(node.index);
        } else {
            this.siftDown(node.index);
        }
    }
    updateIfLower(node: T, priority: number): void {
        if (node.getPriority() > priority) {
            node.updatePriority(priority);
            this.siftUp(node.index);
        }
    }

    isEmpty(): boolean {
        return this.length == 0;
    }
}

class Grid {
    grid: readonly number[][];
    rows: number;
    cols: number;

    constructor(gridString: String[]) {
        this.parseGrid(gridString);
    }

    private parseGrid(string: String[]): void {
        let grid: number[][] = [];
        this.rows = 0;
        this.cols = 0;
        for (let line of string) {
            let n: number[] = [];
            for (let i = 0; i < line.length; i++) {
                let char = line.charAt(i);
                n.push(parseInt(char));
            }
            grid.push(n);
            this.cols = Math.max(n.length, this.cols);
        }
        this.rows = grid.length;
        this.grid = grid;
    }

    getNumber(coords: Vector): number | undefined {
        let r = coords.row;
        let c = coords.col;
        if (0 <= r && r < this.rows && 0 <= c && c < this.cols) {
            return this.grid[coords.row][coords.col];
        }
        return undefined;
    }
    isEnd(coords: Vector): boolean {
        return coords.row === (this.rows - 1) && coords.col === (this.cols - 1);
    }
    distanceToEnd(coords: Vector): number {
        return Math.abs(coords.row - (this.rows - 1)) 
               + Math.abs(coords.col - (this.cols - 1));
    }
}

function solve(lines: string[]): void {
    let grid = new Grid(lines);
    let pq = new PriorityQueue<SearchNode>();
    let inPq = new Map<string, SearchNode>();
    let visited = new Set<string>();

    let start = new SearchNode(0, {row:0, col:0}, "RIGHT", 0, (v) => grid.distanceToEnd(v));
    pq.push(start);
    inPq.set(start.hash(), start);
    
    let minHeatLoss = 0;
    let searches = 0;
    while (true) {
        let node = pq.pop();
        searches++;

        if (node === undefined) {
            break;
        }

        let currHash = node.hash();
        inPq.delete(currHash);
        if (grid.isEnd(node.coordinates)) {
            minHeatLoss = node.distance;
            break;
        }
        
        if (visited.has(currHash)) {
            continue;
        }
        let hashes = node.visitedHashes()
        for (let hash of hashes) {
            visited.add(hash);
        }

        let nextMoves = node.generateNextMoves((v) => grid.getNumber(v));
        for (let n of nextMoves) {
            let nextHash = n.hash();
            if (visited.has(nextHash)) {
                continue;
            }
            let pqNode = inPq.get(nextHash)
            if (pqNode !== undefined) {
                pq.updateIfLower(pqNode, n.getPriority());
            } else {
                pq.push(n);
                inPq.set(nextHash, n);
            }
        }
    }
    console.log("Part 1:", minHeatLoss);
    console.log("Searched:", searches);
    
}

function main() {
    let lines: string[] = readFileSync("input17.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import { Dir, readFileSync } from "fs";

type Direction = "U" | "D" | "L" | "R";

const DIRECTIONS: Direction[] = ["U", "D", "L", "R"];
const DIRECTION_VECTORS: {[D in Direction]: Coordinates;} 
        = {"U": {row: -1, col: 0}, "D": {row: 1, col: 0}, 
           "L": {row: 0, col: -1}, "R": {row: 0, col: 1}}
const SLOPE_LEGAL_DIRECTION: {[key: string]: Direction;}
        = {"^": "U", "v": "D", "<": "L", ">": "R"};

class Coordinates {
    row: number;
    col: number;
}

interface Edge {
    to: Node;
    cost: number;
}
interface Node {
    edges: Edge[];
    coords: Coordinates;
}
function hashCoords(coords: Coordinates): string {
    return coords.row.toString() + ',' + coords.col.toString();
}

class Graph {
    nodes: Map<string, Node>; 

    constructor() {
        this.nodes = new Map();
    }

    addNode(coords: Coordinates): boolean {
        let hash = hashCoords(coords);
        if (this.nodes.has(hash)) {
            return false;
        }
        let newNode: Node = {edges: [], coords: coords};
        this.nodes.set(hash, newNode);
        return true;
    }
    addEdge(from: Coordinates, to: Coordinates, distance: number): boolean {
        let fromNode = this.nodes.get(hashCoords(from));
        if (fromNode === undefined) {
            return false;
        }
        for (let edge of fromNode.edges) {
            if (edge.to.coords.row == to.row && edge.to.coords.col == to.col) {
                if (edge.cost != distance) {
                    edge.cost = distance;
                    return true;
                } else {
                    return false;
                }
            }
        }
        let toNode = this.nodes.get(hashCoords(to));
        if (toNode === undefined) {
            return false;
        }
        let edge: Edge = { to: toNode, cost: distance };
        fromNode.edges.push(edge);
        return true;
    }
    getNode(coords: Coordinates): Node {
        let hash = hashCoords(coords);
        let node = this.nodes.get(hash);
        if (node === undefined) {
            throw new Error("Key Error: " + hash);
        }
        return node;
    }
    findLongestPath(start: Node, end: Node, visited?: Set<string>): number {
        if (visited === undefined) {
            visited = new Set();
        }
        let maximum = -1;
        for (let edge of start.edges) {
            let next = edge.to;
            if (visited.has(hashCoords(next.coords))) {
                continue;
            } else if (next.coords.row === end.coords.row && next.coords.col === end.coords.col) {
                maximum = Math.max(edge.cost, maximum);
            } else {
                let hash = hashCoords(start.coords);
                visited.add(hash);
                let nextMaximum = this.findLongestPath(next, end, visited);
                visited.delete(hash);
                if (nextMaximum < 0) {
                    continue;
                }
                maximum = Math.max(edge.cost + nextMaximum, maximum);
            }            
        }
        return maximum;
    }
}

class Maze {
    maze: readonly string[][]
    mazeGraph: Graph;
    start: Coordinates;
    end: Coordinates;
    rows = 0;
    cols = 0;

    constructor(lines: string[]) {
        this.rows = 0;
        this.cols = 0
        this.parseMaze(lines);
    }

    private parseMaze(lines: string[]) {
        let maze: string[][] = [];
        for (let r = 0; r < lines.length; r++) {
            let row = lines[r];
            let nextRow: string[] = [];
            for (let c = 0; c < row.length; c++) {
                let char = row[c];
                nextRow.push(char);
                if (r === 0 && char === '.') {
                    this.start = {row: r, col: c};
                } else if (r === lines.length - 1 && char === '.') {
                    this.end = {row: r, col: c};
                }
            }
            maze.push(nextRow);
            this.cols = Math.max(this.cols, nextRow.length);
        }
        this.maze = maze;
        this.rows = maze.length;
    }
    isLegal(coords: Coordinates, direction: Direction, obeyArrows: boolean): boolean {
        let r = coords.row;
        let c = coords.col;
        if (0 <= r && r < this.rows && 0 <= c && c < this.cols) {
            let tile = this.maze[r][c];
            if (tile === '#') {
                return false;
            } else if (tile === '.') {
                return true;
            } else {
                return !obeyArrows || (direction === SLOPE_LEGAL_DIRECTION[tile]);
            }
        }
        return false;
    }
    move(coords: Coordinates, direction: Direction, obeyArrows: boolean): Coordinates | undefined {
        let vector = DIRECTION_VECTORS[direction];
        let next: Coordinates = {row: coords.row + vector.row, col: coords.col + vector.col};
        return this.isLegal(next, direction, obeyArrows) ? next : undefined;
    }
    isEnd(coords: Coordinates): boolean {
        return coords.row === this.end.row && coords.col === this.end.col;
    }
    getNextIntersections(start: Coordinates, obeyArrows: boolean): [Coordinates, number][] {
        let intersections: [Coordinates, number][] = [];
        for (let startDirection of DIRECTIONS) {
            let nextStart = this.move(start, startDirection, obeyArrows);
            if (nextStart === undefined) {
                continue;
            }
            let distance = 1;
            let visited = new Set<string>();
            let queue = [nextStart];
            visited.add(hashCoords(start));
            visited.add(hashCoords(nextStart));
            while (queue.length > 0) {
                let nextQueue: Coordinates[] = [];
                for (let curr of queue) {
                    if (this.isEnd(curr)) {
                        intersections.push([curr, distance]);
                        continue;
                    }
                    for (let direction of DIRECTIONS) {
                        let nextCoords = this.move(curr, direction, obeyArrows);
                        if (nextCoords === undefined) {
                            continue;
                        }
                        let hash = hashCoords(nextCoords);
                        if (visited.has(hash)) {
                            continue;
                        } else {
                            nextQueue.push(nextCoords);
                            visited.add(hash);
                        }
                        
                    }
                }
                if (nextQueue.length > 1) {
                    intersections.push([queue[0], distance]);
                    break;
                }
                queue = nextQueue;
                distance++;
            }
        }
        return intersections;

    }

    buildGraph(obeyArrows: boolean): void {
        let graph = new Graph();
        let visited = new Set<string>();
        graph.addNode(this.start);
        graph.addNode(this.end);
        let queue = [this.start];
        visited.add(hashCoords(this.start));
        visited.add(hashCoords(this.end));
        while (true) {
            let currCoords = queue.shift();
            if (currCoords === undefined) {
                break;
            }
            let nextIntersections = this.getNextIntersections(currCoords, obeyArrows);
            for (let [coords, distance] of nextIntersections) {
                graph.addNode(coords);
                graph.addEdge(currCoords, coords, distance);
                if (visited.has(hashCoords(coords))) {
                    continue;
                } else {
                    queue.push(coords);
                    visited.add(hashCoords(coords));
                }
            }
        }
        this.mazeGraph = graph;
    }

    findLongestPath(): number {

        let start = this.mazeGraph.getNode(this.start);
        let end = this.mazeGraph.getNode(this.end);
        return this.mazeGraph.findLongestPath(start, end);
    }
}

function solve(lines: string[]): void {
    let maze = new Maze(lines);
    // maze.buildGraph(true);
    // console.log("Part 1:", maze.findLongestPath());
    maze.buildGraph(false);
    // console.log(maze.mazeGraph.nodes);
    console.log("Part 2:", maze.findLongestPath());
}

function main() {
    let lines: string[] = readFileSync("input23.txt", "utf-8")
        .split(/\n/)
        .map(x => x.trim())
        .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import {readFileSync} from "fs";

type Tile = '#' | '.';

const DIRECTION_VECTORS: Coordinates[] = [{row: -1, col: 0}, {row: 1, col: 0}, 
                                          {row: 0, col: -1}, {row: 0, col: 1}]

interface Coordinates {
    row: number;
    col: number;
}

class Plot {
    map: readonly Tile[][];
    start: Coordinates;
    rows: number;
    cols: number;

    constructor() {
        this.start = {row: 0, col: 0};
        this.rows = 0;
        this.cols = 0;
        this.map = [];
    }

    parseMap(lines: string[]) {
        let map: Tile[][] = [];
        for (let r = 0; r < lines.length; r++) {
            let line = lines[r];
            let row: Tile[] = [];
            for (let c = 0; c < line.length; c++) {
                let char = line.charAt(c);
                if (char === '#') {
                    row.push('#');
                } else if (char === '.') {
                    row.push('.');
                } else if (char === 'S') {
                    this.start = {row: r, col: c};
                    row.push('.');
                } else {
                    throw new Error("Parse Error: Unable to parse char " + char + " at line " + (r + 1));
                }
            }
            map.push(row);
            this.cols = Math.max(this.cols, row.length);
        }
        this.map = map;
        this.rows = this.map.length;
    }
    inBounds(coords: Coordinates): boolean {
        return (0 <= coords.row && coords.row < this.map.length)
               && (0 <= coords.col && coords.col < this.map[0].length);
    }
    convertCoordsInBounds(coords: Coordinates): Coordinates {
        let row = coords.row % this.rows;
        if (row < 0) {
            row = this.rows + row;
        }
        let col = coords.col % this.cols;
        if (col < 0) {
            col = this.cols + col;
        }
        return {row: row, col: col};
    }
    getTile(coords: Coordinates, inBounds=true): Tile | undefined {
        if (inBounds) {
            if (this.inBounds(coords)) {
                return this.map[coords.row][coords.col];
            }
            return undefined;
        }
        let inBoundsCoords = this.convertCoordsInBounds(coords);
        return this.map[inBoundsCoords.row][inBoundsCoords.col];
    }
    nextMoves(coords: Coordinates, inBounds=true): Coordinates[] {
        let output: Coordinates[] = [];
        for (let vector of DIRECTION_VECTORS) {
            let next = {row: coords.row + vector.row, col: coords.col + vector.col};
            let tile = this.getTile(next, inBounds);
            if (tile === '.') {
                output.push(next);
            }
        }
        return output;
    }
    generateMoves(coords: Coordinates[], inBounds=true): Coordinates[] {
        let hashmap = new Map<string, Coordinates>();
        for (let c of coords) {
            for (let next of this.nextMoves(c, inBounds)) {
                hashmap.set(next.row.toString() + ',' + next.col.toString(), next);
            }
        }
        let output: Coordinates[] = [];
        for (let c of hashmap.values()) {
            output.push(c);
        }
        return output;
    }

    getNumReachablePlots(steps: number, inBounds=true): number {
        let on = 0;
        let off = 0;
        let prev = new Set<string>();
        let newBlocks = new Set<string>();
        let curr = [this.start]
        for (let i = 0; i < steps; i++) {
            let a = on;
            on = off + curr.length;
            off = a;
            let next = this.generateMoves(curr, false);
            let nextSet = new Set<string>();
            let nextcurr: Coordinates[] = [];
            for (let c of next) {
                let newBlock = Math.floor(c.row / this.rows).toString() + ',' 
                               + Math.floor(c.col / this.cols).toString()
                if (!newBlocks.has(newBlock)) {
                    let inBoundsCoords = this.convertCoordsInBounds(c)
                    // console.log("New block: " + newBlock + " at i = " + (i + 1) + " with coords:", inBoundsCoords);
                    newBlocks.add(newBlock);
                }
                let hash = c.row.toString() + ',' + c.col.toString();
                if (prev.has(hash)) {
                    continue;
                } else {
                    nextcurr.push(c);
                }
            }
            for (let c of curr) {
                nextSet.add(c.row.toString() + ',' + c.col.toString());
            }
            prev = nextSet;
            curr = nextcurr;
        }
        return off + curr.length;
    }
}

interface OddsEvens {
    odds: number;
    evens: number;
}

class InfinitePlotSolver {

    map: readonly Tile[][];
    beginning: Coordinates;
    rows: number;
    cols: number;

    solutions: Map<string, OddsEvens>;
    counts: Map<string, number>;


    constructor(start: Plot) {
        this.map = start.map;
        this.beginning = start.start;
        this.rows = start.rows;
        this.cols = start.cols;
        this.solutions = new Map();
        this.counts = new Map();
    }

    inBounds(coords: Coordinates): boolean {
        return (0 <= coords.row && coords.row < this.map.length)
               && (0 <= coords.col && coords.col < this.map[0].length);
    }
    mapNSteps(beginning: Coordinates, steps: number): OddsEvens {
        if (steps == 0) {
            return {odds: 0, evens: 1}; // Beginning
        }
        let i = 0;
        let odds = 0;
        let evens = 0;
        let isEven = true;
        let visited = new Set<string>();
        let queue: Coordinates[] = [beginning];
        visited.add(beginning.row.toString() + ',' + beginning.col.toString());
        while (queue.length > 0 && i <= steps) {
            if (isEven) {
                evens += queue.length;
            } else {
                odds += queue.length;
            }
            let nextQueue: Coordinates[] = [];
            for (let c of queue) {
                for (let v of DIRECTION_VECTORS) {
                    let next: Coordinates = {row: c.row + v.row, col: c.col + v.col};
                    let hash = next.row.toString() + ',' + next.col.toString();
                    if (visited.has(hash)) {
                        continue;
                    } else if (!this.inBounds(next)) {
                        continue;
                    } else if (this.map[next.row][next.col] === '#') {
                        continue;
                    }
                    nextQueue.push(next);
                    visited.add(hash);
                }
            }
            queue = nextQueue;
            isEven = !isEven;
            i++;
        }
        return {odds: odds, evens: evens};
    }

    mapPlot(beginning: Coordinates): OddsEvens {
        
        return this.mapNSteps(beginning, this.rows * this.cols);
    }

    calculatePlotBlockLength(steps: number): number {
        let remainingSteps = steps - this.beginning.row;
        return 1 + 2 * (Math.ceil(remainingSteps / this.rows));
    }

    solve(steps: number): number {
        let stepsEven = steps % 2 === 0;

        if (steps <= this.beginning.row) {
            let oddEvens = this.mapNSteps(this.beginning, steps);
            return steps % 2 == 0 ? oddEvens.evens : oddEvens.odds;
        }

        let blockData = this.mapPlot(this.beginning);
        if (!stepsEven) {
            let c = blockData.evens; // Must swap, as the block is calculated with beginning 
            blockData.evens = blockData.odds;  // starting as even.
            blockData.odds = c;
        }

        let reachable = 0;

        let evens = 0;
        let odds = 0;
        let isEven = true;
        let iteration = 0;
        while (true) {
            if (steps < this.rows) {
                break;
            } else {
                steps -= this.rows;
                let newBlocks = iteration == 0 ? 1 : iteration * 4;
                if (isEven) {
                    evens += newBlocks;
                } else {
                    odds += newBlocks;
                }
                iteration++;
                isEven = !isEven;

            }
        }
        reachable += evens * blockData.evens;
        reachable += odds * blockData.odds;

        // console.log("Steps:", steps);
        let innerEdgeSteps = steps + this.beginning.row;
        // console.log(innerEdgeSteps);
        // console.log("Reachable ", reachable, blockData, 'odds:', odds, 'evens:', evens);
        let edges: Coordinates[] = [{row: this.beginning.row, col: 0},
                                    {row: this.beginning.row, col: this.cols - 1},
                                    {row: 0, col: this.beginning.col},
                                    {row: this.rows - 1, col: this.beginning.col}];
        for (let c of edges) {
            let result = this.mapNSteps(c, innerEdgeSteps);
            // console.log("edge: ", c, result, "even?", isEven);
            if ((innerEdgeSteps % 2) == 0) {
                reachable += result.evens;
            } else {
                reachable += result.odds;
            }
        }
        let outerEdgeSteps = steps - this.beginning.row - 1;
        if (outerEdgeSteps >= 0) {
            for (let c of edges) {
                let result = this.mapNSteps(c, outerEdgeSteps);
                // console.log("outeredge: ", c, result, "even?", isEven);
                if ((outerEdgeSteps % 2) == 0) {
                    reachable += result.evens;
                } else {
                    reachable += result.odds;
                }
            }
        }

        let cornerStepsBig = steps + this.beginning.row + this.beginning.col;
        let corners: Coordinates[] = [{row: 0, col: 0},
                                      {row: 0, col: this.cols - 1},
                                      {row: this.rows - 1, col: this.cols - 1},
                                      {row: this.rows - 1, col: 0}];
        if (iteration > 0) {
            for (let c of corners) {
                let result = this.mapNSteps(c, cornerStepsBig);
                // console.log("bigcorner: ", c, result, "even?", isEven);
                if ((cornerStepsBig % 2) == 0) {
                    reachable += result.evens * (iteration - 1);
                } else {
                    reachable += result.odds * (iteration - 1);
                }
            }
        }
        // console.log("Reachable: ", reachable);
        let cornerStepsSmall = steps - 1;
        // console.log("Small step:", cornerStepsSmall, "iteration: ", iteration);
        if (iteration > 0) {
            for (let c of corners) {
                let result = this.mapNSteps(c, cornerStepsSmall);
                // console.log("smallcorner: ", c, result, "even?", isEven);
                if ((cornerStepsSmall % 2) == 0) {
                    reachable += result.evens * (iteration);
                } else {
                    reachable += result.odds * (iteration);
                }
            }
        }
        
        return reachable;
    }
}

function solve(lines: string[]): void {
    let plot = new Plot();
    plot.parseMap(lines);
    
    let solver = new InfinitePlotSolver(plot);
    console.log("Part 1:", solver.mapNSteps(plot.start, 64).evens);
    // console.log("answer: ", plot.getNumReachablePlots(500));
    console.log("Part 2:", solver.solve(26501365));
    

}

function main() {
    let lines: string[] = readFileSync("input21.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import {readFileSync} from "fs";

type Tile = '#' | '.';

const DIRECTION_VECTORS: Coordinates[] = [{row: -1, col: 0}, {row: 1, col: 0}, 
                                          {row: 0, col: -1}, {row: 0, col: 1}]

interface Coordinates {
    row: number;
    col: number;
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

    bruteForcedValues: number[];

    constructor(map: string[]) {
        this.solutions = new Map();
        this.counts = new Map();
        this.rows = 0;
        this.cols = 0;
        this.beginning = {row:0, col:0};
        this.map = [];
        this.bruteForcedValues = []
        this.parseMap(map);
        
    }
    parseMap(lines: string[]): void {
        
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
                    this.beginning = {row: r, col: c};
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
    getTile(coords: Coordinates): Tile {
        // Converting negative modulo.
        let row = coords.row % this.rows;
        if (row < 0) {
            row = this.rows + row;
        }
        let col = coords.col % this.cols;
        if (col < 0) {
            col = this.cols + col;
        }
        return this.map[row][col];
        
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

    solveBruteForce(steps: number): number {
        if (steps == 0) {
            this.bruteForcedValues.push(1);
            return 1; // Beginning
        }
        let i = 0;
        let odds = 0;
        let evens = 0;
        let isEven = true;
        let visited = new Set<string>();
        let queue: Coordinates[] = [this.beginning];
        visited.add(this.beginning.row.toString() + ',' + this.beginning.col.toString());
        while (queue.length > 0 && i <= steps) {
            if (isEven) {
                evens += queue.length;
            } else {
                odds += queue.length;
            }
            this.bruteForcedValues.push(i % 2 == 0 ? evens : odds);
            let nextQueue: Coordinates[] = [];
            for (let c of queue) {
                for (let v of DIRECTION_VECTORS) {
                    let next: Coordinates = {row: c.row + v.row, col: c.col + v.col};
                    let hash = next.row.toString() + ',' + next.col.toString();
                    let nextTile = this.getTile(next);
                    if (visited.has(hash)) {
                        continue;
                    } else if (nextTile === '#') {
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
        return steps % 2 == 0 ? evens : odds;
    }

    solve(steps: number): number {
        // Solution only works by observing these properties in our puzzle
        // input:
        // > The dimensions of the map is odd and a square
        // > S starts in the middle of the map.
        // > You can infinitely travel up, down, left, or right starting from the middle 
        //   without hitting any rocks.
        // > The outer ring has no rocks
        // > It takes a maximum of 2*length to map out all the reachable plots from any location.
        
        // This means we can travel to any block with the least steps (unlike the puzzle input).
        let stepsEven = steps % 2 === 0;

        // The middle block is partially filled. Just solve it using brute
        // force in order to not deal with edge cases.
        if (steps < this.beginning.row + this.rows) {
            return this.solveBruteForce(steps);
        }

        let blockData = this.mapPlot(this.beginning);
        if (!stepsEven) {
            // So the steps we wish to calculate is an odd number.
            // Since the start is consisidered even, we must swap the answers.
            let c = blockData.evens;
            blockData.evens = blockData.odds;
            blockData.odds = c;
        }

        let reachable = 0; // Our output

        // Calculate the total number of blocks that are fully traversed.
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
                // When we step over to an adjacent block, the parity changes.
                isEven = !isEven; 
            }
        }
        reachable += evens * blockData.evens;
        reachable += odds * blockData.odds;

/*
             ....O....
             ...O.O...
             ,,O,,,O,, <- Calculating this part
             ,O,,,,,O,
*/
        let innerEdgeSteps = steps + this.beginning.row;
        let edges: Coordinates[] = [{row: this.beginning.row, col: 0},
                                    {row: this.beginning.row, col: this.cols - 1},
                                    {row: 0, col: this.beginning.col},
                                    {row: this.rows - 1, col: this.beginning.col}];
        for (let c of edges) {
            let result = this.mapNSteps(c, innerEdgeSteps);
            if ((innerEdgeSteps % 2) == 0) {
                reachable += result.evens;
            } else {
                reachable += result.odds;
            }
        }
/*
               ....O....
               ...O.O... <- Calculating this part, if it exists
               ,,O,,,O,, 
               ,O,,,,,O,
*/
        let outerEdgeSteps = steps - this.beginning.row - 1;
        if (outerEdgeSteps >= 0) {
            for (let c of edges) {
                let result = this.mapNSteps(c, outerEdgeSteps);
                if ((outerEdgeSteps % 2) == 0) {
                    reachable += result.evens;
                } else {
                    reachable += result.odds;
                }
            }
        }

/*
        ...........,,,,,O,,,,,
        ...........,,,,O,,,,,,
        ...........,,,O,,,,,,,
        ,,,,,,,,,,,..O........
        ,,,,,,,,,,,.O.........
        ,,,,,,,,,,,O.......... <- Calculating this part, the corners that
        ,,,,,,,,,,O...........    contain the centre.
        ,,,,,,,,,O,........... 
*/
        let cornerStepsBig = steps + this.beginning.row + this.beginning.col;
        let corners: Coordinates[] = [{row: 0, col: 0},
                                      {row: 0, col: this.cols - 1},
                                      {row: this.rows - 1, col: this.cols - 1},
                                      {row: this.rows - 1, col: 0}];
        if (iteration > 0) {
            for (let c of corners) {
                let result = this.mapNSteps(c, cornerStepsBig);
                if ((cornerStepsBig % 2) == 0) {
                    reachable += result.evens * (iteration - 1);
                } else {
                    reachable += result.odds * (iteration - 1);
                }
            }
        }

/*
        ...........,,,,,O,,,,,
        ...........,,,,O,,,,,, <- Calculating this part, the corners that
        ...........,,,O,,,,,,,    do not contain the centre.
        ,,,,,,,,,,,..O........
        ,,,,,,,,,,,.O.........
        ,,,,,,,,,,,O.......... 
        ,,,,,,,,,,O...........    
        ,,,,,,,,,O,........... 
            ^                    
        This is also the same corner
*/
        let cornerStepsSmall = steps - 1;
        if (iteration > 0) {
            for (let c of corners) {
                let result = this.mapNSteps(c, cornerStepsSmall);
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

function testBruteForce() {
    let lines: string[] = readFileSync("test.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    let solver = new InfinitePlotSolver(lines);
    let testSteps = [6, 10, 50, 100, 500];
    let expected = [16, 50, 1594, 6536, 167004];
    for (let i = 0; i < testSteps.length; i++) {
        let got = solver.solveBruteForce(testSteps[i])
        console.assert(got === expected[i], "Expected %d. Got %d", expected[i], got);
    }
}

function testSolver(solver: InfinitePlotSolver) {
    solver.solveBruteForce(500);
    for (let i = 200; i <= 500; i++) {
        let got = solver.solve(i);
        let expected = solver.bruteForcedValues[i];
        console.assert(got === expected, "Iteration %d: Expected %d. Got %d", i, expected, got);
    }
}

function solve(lines: string[]): void {
    let solver = new InfinitePlotSolver(lines);
    // testBruteForce();
    // testSolver(solver);
    console.log("Part 1:", solver.solve(64));
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
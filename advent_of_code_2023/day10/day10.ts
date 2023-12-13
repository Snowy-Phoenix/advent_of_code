import {readFileSync} from "fs";

interface Coordinates {
    row: number;
    col: number;
}

class CoordinatesSet {
    [key: number]: Set<number>;

    has(coords: Coordinates): boolean {
        if (coords.row in this) {
            let set = this[coords.row];
            if (set.has(coords.col)) {
                return true;
            }
        }
        return false;
    }
    add(coords: Coordinates): void {
        if (!(coords.row in this)) {
            this[coords.row] = new Set();
        } 
        let set = this[coords.row]
        set.add(coords.col);
    }
}

class Pipe {
    char: string;
    directions: Coordinates[]

    constructor(char: string, directions: Coordinates[]) {
        this.char = char;
        this.directions = directions;
    }

    getNeighbours(coords: Coordinates): Coordinates[] {
        let output: Coordinates[] = [];
        for (let v of this.directions) {
            output.push({
                row: coords.row + v["row"],
                col: coords.col + v["col"]
            })
        }
        return output;
    }
}

class PipeGrid {
    rows: number;
    cols: number;
    grid: Pipe[][];
    start: Coordinates;

    constructor() {
        this.rows = 0;
        this.cols = 0
        this.grid = [];
    }

    isInGrid(coords: Coordinates): boolean {
        if (0 <= coords.row && coords.row < this.rows) {
            return 0 <= coords.col && coords.col < this.grid[coords.row].length;
        }
        return false;
    }
    addPipe(p: Pipe): void {
        let row = this.grid[this.rows - 1];
        row.push(p);
        this.cols = Math.max(this.cols, row.length)
        if (p.char == "S") {
            this.start = {row: this.rows - 1, col: row.length - 1};
        }
    }
    setPipe(p: Pipe, coords: Coordinates): void {
        if (this.isInGrid(coords)) {
            this.grid[coords.row][coords.col] = p;
        }
    }
    newLine(): void {
        this.grid.push([]);
        this.rows++;
    }
    canMove(from: Coordinates, to: Coordinates): boolean {
        if (this.isInGrid(from) && this.isInGrid(to)) {
            let potentialMoves = this.grid[from.row][from.col].getNeighbours(from);
            for (let move of potentialMoves) {
                if (move.row === to.row && move.col === to.col) {
                    return true;
                }
            }
        }
        return false;
    }
    getMoves(coords: Coordinates): Coordinates[] {
        let validMoves: Coordinates[] = [];
        if (this.isInGrid(coords)) {
            let potentialMoves = this.grid[coords.row][coords.col].getNeighbours(coords);
            for (let move of potentialMoves) {
                if (this.canMove(move, coords)) {
                    validMoves.push(move);
                }
            }
        }
        return validMoves;
    }
    getStartPipeType(): string {
        const map = {'1100': 'L',
                     '1010': '|',
                     '1001': 'J',
                     '0110': 'F',
                     '0101': '-',
                     '0011': '7'}
        let mapString = ""
        mapString += this.canMove({row: this.start.row - 1,
                                   col: this.start.col}, 
                                   this.start) ? '1' : '0';
        mapString += this.canMove({row: this.start.row,
                                   col: this.start.col + 1}, 
                                   this.start) ? '1' : '0';
        mapString += this.canMove({row: this.start.row + 1,
                                   col: this.start.col}, 
                                   this.start) ? '1' : '0';
        mapString += this.canMove({row: this.start.row,
                                   col: this.start.col - 1}, 
                                   this.start) ? '1' : '0';
        return map[mapString];
    }

}

function parseGrid(lines: string[]): PipeGrid {
    const PIPE_VECTORS = {
        '|': [{row: 1,  col: 0}, {row: -1, col: 0}],
        '-': [{row: 0,  col: 1}, {row: 0,  col: -1}],
        'L': [{row: -1, col: 0}, {row: 0,  col: 1}],
        'J': [{row: -1, col: 0}, {row: 0,  col: -1}],
        '7': [{row: 1,  col: 0}, {row: 0,  col: -1}],
        'F': [{row: 1,  col: 0}, {row: 0,  col: 1}],
        '.': [],
        'S': [{row: 1, col: 0}, {row: -1, col: 0},{row: 0, col: 1}, {row: 0, col: -1}],
    }
    let pipeGrid = new PipeGrid();
    for (let line of lines) {
        pipeGrid.newLine();
        for (let char of line) {
            let pipe = new Pipe(char, PIPE_VECTORS[char]);
            pipeGrid.addPipe(pipe);
        }
    }
    let pipe = pipeGrid.getStartPipeType();
    pipeGrid.setPipe(new Pipe(pipe, PIPE_VECTORS[pipe]), pipeGrid.start);
    return pipeGrid;
}

function mapPipes(pipeGrid: PipeGrid): [CoordinatesSet, number] {
    let queue = [pipeGrid.start];
    let visited = new CoordinatesSet();
    visited.add(pipeGrid.start);
    let nextQueue: Coordinates[] = [];
    let steps = 0;
    while (true) {
        for (let move of queue) {
            let nextMoves = pipeGrid.getMoves(move).filter((x) => !visited.has(x));
            nextQueue = nextQueue.concat(nextMoves);
            visited.add(move);
        }
        if (nextQueue.length == 0) {
            break;
        } else {
            steps++;
            queue = nextQueue;
            nextQueue = [];
        }
    }
    return [visited, steps];
}

function findEnclosed(pipeGrid: PipeGrid, loopPipes: CoordinatesSet): number {

    const UP_PIPES = ['L', 'J', '|'];
    const DOWN_PIPES = ['7', 'F', '|'];

    let numInsideLoop = 0;
    let up = false;
    let down = false;
    for (let r = 0; r < pipeGrid.rows; r++) {
        let row = pipeGrid.grid[r];
        for (let c = 0; c < row.length; c++) {
            let char = row[c].char;

            if (!loopPipes.has({row: r, col: c})) {
                numInsideLoop += up && down ? 1 : 0;
                continue;
            }
            if (UP_PIPES.includes(char)) {
                up = !up;
            }
            if (DOWN_PIPES.includes(char)) {
                down = !down;
            }
        }
    }
    return numInsideLoop;
}

function solve(lines: string[]): void {
    let pipeGrid = parseGrid(lines);
    let [loopPipes, steps] = mapPipes(pipeGrid);
    
    console.log("Part 1:", steps);
    
    let numInsideLoop = findEnclosed(pipeGrid, loopPipes);
    console.log("Part 2:", numInsideLoop);
}

function main() {
    let lines: string[] = readFileSync("input10.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
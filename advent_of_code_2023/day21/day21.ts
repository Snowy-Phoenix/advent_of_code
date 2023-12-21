import {readFileSync} from "fs";

type Tile = '#' | '.';

const DIRECTION_VECTORS: Coordinates[] = [{row: -1, col: 0}, {row: 1, col: 0}, 
                                          {row: 0, col: -1}, {row: 0, col: 1}]

interface Coordinates {
    row: number;
    col: number;
}

class Plot {
    map: Tile[][];
    start: Coordinates;
    rows: number;
    cols: number;

    constructor(lines: string[]) {
        this.start = {row: 0, col: 0};
        this.rows = 0;
        this.cols = 0;
        this.map = [];
        this.parseMap(lines);
    }

    private parseMap(lines: string[]) {
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
            this.map.push(row);
            this.cols = Math.max(this.cols, row.length);
        }
        this.rows = this.map.length;
    }
    inBounds(coords: Coordinates): boolean {
        return (0 <= coords.row && coords.row < this.map.length)
               && (0 <= coords.col && coords.col < this.map[0].length);
    }
    getTile(coords: Coordinates): Tile | undefined {
        if (this.inBounds(coords)) {
            return this.map[coords.row][coords.col];
        }
        return undefined;
    }
    nextMoves(coords: Coordinates): Coordinates[] {
        let output: Coordinates[] = [];
        for (let vector of DIRECTION_VECTORS) {
            let next = {row: coords.row + vector.row, col: coords.col + vector.col};
            let tile = this.getTile(next);
            if (tile === '.') {
                output.push(next);
            }
        }
        return output;
    }
    generateMoves(coords: Coordinates[]): Coordinates[] {
        let hashmap = new Map<string, Coordinates>();
        for (let c of coords) {
            for (let next of this.nextMoves(c)) {
                hashmap.set(next.row.toString() + ',' + next.col.toString(), next);
            }
        }
        let output: Coordinates[] = [];
        for (let c of hashmap.values()) {
            output.push(c);
        }
        return output;
    }
}

function solve(lines: string[]): void {
    let plot = new Plot(lines);
    let nextMoves = [plot.start];
    for (let i = 0; i < 64; i++) {
        nextMoves = plot.generateMoves(nextMoves);
    }
    console.log("Part 1:", nextMoves.length);
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
import {readFileSync} from "fs";

enum Tilt {NORTH, WEST, SOUTH, EAST};

interface Coordinates {
    row: number;
    col: number;
}

class Dish {

    grid: string[][];
    boulders: Set<number>; // (r * maxCols) + c
    walls: Set<number>;    // (r * maxCols) + c
    tiltTable: number[][]; // 4 * (rows * cols)
    rows: number;
    cols: number;
    vectors: number[];

    constructor(grid: string[]) {
        this.boulders = new Set();
        this.walls = new Set()
        this.parseDish(grid);
        this.vectors = [-this.cols, -1, this.cols, 1];
        this.generateTiltTable();
    }

    flattenCoords(coords: Coordinates): number {
        return (coords.row * this.cols) + coords.col;
    }
    unflattenCoords(n: number): Coordinates {
        return {row: Math.floor(n / this.cols), col: n % this.cols}
    }

    private generateTiltTable(): void {
        this.tiltTable = [];
        for (let v of this.vectors) {
            let table: number[] = [];
            for (let i = 0; i < this.rows * this.cols; i++) {
                if (this.walls.has(i)) {
                    table.push(i);
                    continue;
                }
                let curr = i;
                while (true) {
                    let next = curr + v;
                    if (next < 0 // Boundary Up
                    || next >= this.rows * this.cols // Boundary Down
                    || (next % this.cols) - (curr % this.cols) != v % this.cols // Wrap-around checking
                    || this.walls.has(next)) {
                        table.push(curr);
                        break;
                    }
                    curr = next;
                }
            }
            this.tiltTable.push(table);
        }
    }

    private parseDish(grid: string[]): void {
        this.rows = grid.length;
        this.cols = grid[0].length;
        this.grid = [];
        for (let r = 0; r < grid.length; r++) {
            let line = grid[r];
            this.grid.push([]);

            for (let c = 0; c < line.length; c++) {
                let char = line[c];
                this.grid[this.grid.length - 1].push(char);
                if (char == 'O') {
                    this.boulders.add(this.flattenCoords({row: r, col: c}));
                } else if (char == '#') {
                    this.walls.add(this.flattenCoords({row: r, col: c}));
                }
            }
        }
    }

    swap(from: Coordinates, to: Coordinates): void {
        let n1 = this.flattenCoords(from);
        let n2 = this.flattenCoords(to);
        let s1 = this.grid[from.row][from.col];
        let s2 = this.grid[to.row][to.col];
        if (s1 != undefined && s2 != undefined) {
            this.grid[from.row][from.col] = s2;
            this.grid[to.row][to.col] = s1;
            let n1Boulder = false;
            let n2Boulder = false;
            if (this.boulders.has(n1)) {
                n1Boulder = true;
            }
            if (this.boulders.has(n2)) {
                n2Boulder = true;
            }
            if (n1Boulder !== n2Boulder) {
                if (n1Boulder) {
                    this.boulders.delete(n1);
                    this.boulders.add(n2);
                } else {
                    this.boulders.delete(n2);
                    this.boulders.add(n1);
                }
            }
        }
    }

    getTile(coords: Coordinates): string {
        return this.grid[coords.row][coords.col];
    }

    lookupTilt(direction: Tilt, n: number): number {
        return this.tiltTable[direction][n];
    }

    tilt(direction: Tilt): void {
        let v = this.vectors[direction];
        for (let n of this.boulders.values()) {
            let curr = this.lookupTilt(direction, n);
            while (curr != n && 0 <= curr && curr < this.rows * this.cols) {
                if (!this.boulders.has(curr)) {
                    break;
                }
                curr -= v;
            }
            this.swap(this.unflattenCoords(n), this.unflattenCoords(curr));
        }
    }

    getGridAsString(): string {
        let str = this.grid[0].reduce((s, char) => s + char);
        for (let i = 1; i < this.grid.length; i++) {
            let line = this.grid[i];
            str += "\n";
            str += line.reduce((s, char) => s + char);
        }
        return str;
    }

    computeLoad(): number {
        let sum = 0;
        for (let n of this.boulders) {
            let row = Math.floor(n / this.cols);
            sum += (this.rows - row);
        }
        return sum;
    }

    hashBoulders(): string {
        let byteArray = new Uint8Array(Math.ceil(this.rows * this.cols / 8));
        for (let b of this.boulders.values()) {
            let block = Math.floor(b / 8);
            let offset = b % 8;
            byteArray[block] = byteArray[block] | (1 << offset);
        }
        let str = ''
        for (let b of byteArray) {
            str += String.fromCharCode(b);
        }
        return str;
    }
}

function decodeLoad(str: string, rows: number, cols: number): number {
    let load = 0;
    for (let block = 0; block < str.length; block++) {
        let byte = str.charCodeAt(block);
        let i = 0;
        while (byte != 0) {
            if ((byte & 1) == 1) {
                let n = block*8 + i;
                load += rows - Math.floor(n / cols);
            }
            byte >>= 1;
            i += 1;
        }
    }
    return load
}

function cycle(dish: Dish) {
    dish.tilt(Tilt.NORTH);
    dish.tilt(Tilt.WEST);
    dish.tilt(Tilt.SOUTH);
    dish.tilt(Tilt.EAST);
}

function solve(lines: string[]): void {
    let dish = new Dish(lines);
    dish.tilt(Tilt.NORTH);
    console.log("Part 1:", dish.computeLoad());
    dish.tilt(Tilt.WEST);
    dish.tilt(Tilt.SOUTH);
    dish.tilt(Tilt.EAST);

    let visited = new Map<string, number>();
    let dishes: string[] = [];

    let str = dish.hashBoulders()
    visited.set(str, 0);
    dishes.push(str);

    let finalDishStr = ""
    let totalCycles = 1000000000;
    for (let i = 1; i < totalCycles; i++) {
        cycle(dish);
        let key = dish.hashBoulders();
        let val = visited.get(key)
        if (val !== undefined) {
            let cycleLength = i - val;
            let cyclesLeft = totalCycles - 1 - i;
            let cycleIndex = cyclesLeft % cycleLength;
            finalDishStr = dishes[val + cycleIndex]; 
            break;
        }
        visited.set(key, i);
        dishes.push(key);
        finalDishStr = key;
    }
    console.log("Part 2:", decodeLoad(finalDishStr, dish.rows, dish.cols));
}

function main() {
    let lines: string[] = readFileSync("input14.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
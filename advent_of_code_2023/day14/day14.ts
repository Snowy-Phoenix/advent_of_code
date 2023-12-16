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

    let str = dish.getGridAsString()
    visited.set(str, 0);
    dishes.push(str);

    let finalDishStr = ""
    let totalCycles = 1000000000;
    for (let i = 1; i < totalCycles; i++) {
        cycle(dish);
        let key = dish.getGridAsString();
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
    
    let finalDish = new Dish(finalDishStr.split('\n'));
    console.log("Part 2:", finalDish.computeLoad());
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
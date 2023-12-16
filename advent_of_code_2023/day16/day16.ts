import {readFileSync} from "fs";


const Direction = {
    up: [-1,0],
    down: [1,0],
    left: [0,-1],
    right: [0,1]
} as const;

interface Ray {
    row: number;
    col: number;
    direction: readonly [number, number];
}

interface Tile {
    shine(ray: Ray): Ray[];
}

class Empty implements Tile {
    shine(ray: Ray): Ray[] {
        let row = ray.row + ray.direction[0];
        let col = ray.col + ray.direction[1];
        return [{row: row, col: col, direction: ray.direction}];
    }
}
class ForwardSlashMirror implements Tile {
    shine(ray: Ray): Ray[] {
        let reflection: readonly [number, number];
        if (ray.direction === Direction.up) {
            reflection = Direction.right;
        } else if (ray.direction === Direction.left) {
            reflection = Direction.down;
        } else if (ray.direction === Direction.down) {
            reflection = Direction.left;
        } else {
            reflection = Direction.up;
        }
        let row = ray.row + reflection[0];
        let col = ray.col + reflection[1];
        return [{row: row, col: col, direction: reflection}];
    }
}
class BackSlashMirror implements Tile {
    shine(ray: Ray): Ray[] {
        let reflection: readonly [number, number];
        if (ray.direction === Direction.up) {
            reflection = Direction.left;
        } else if (ray.direction === Direction.left) {
            reflection = Direction.up;
        } else if (ray.direction === Direction.down) {
            reflection = Direction.right;
        } else {
            reflection = Direction.down;
        }
        let row = ray.row + reflection[0];
        let col = ray.col + reflection[1];
        return [{row: row, col: col, direction: reflection}];
    }
}
class VerticalSplitter implements Tile {
    shine(ray: Ray): Ray[] {
        if (ray.direction === Direction.down
            || ray.direction === Direction.up) {
                let row = ray.row + ray.direction[0];
                let col = ray.col + ray.direction[1];
                return [{row: row, col: col, direction: ray.direction}];
            }
        else {
            let dir1 = Direction.up;
            let row1 = ray.row + dir1[0];
            let col1 = ray.col + dir1[1];
            let ray1: Ray = {
                row: row1,
                col: col1,
                direction: dir1
            };

            let dir2 = Direction.down;
            let row2 = ray.row + dir2[0];
            let col2 = ray.col + dir2[1];
            let ray2: Ray = {
                row: row2,
                col: col2,
                direction: dir2
            };
            return [ray1, ray2];
        }
    }
}
class HorizontalSplitter implements Tile {
    shine(ray: Ray): Ray[] {
        if (ray.direction === Direction.left
            || ray.direction === Direction.right) {
                let row = ray.row + ray.direction[0];
                let col = ray.col + ray.direction[1];
                return [{row: row, col: col, direction: ray.direction}];
            }
        else {
            let dir1 = Direction.left;
            let row1 = ray.row + dir1[0];
            let col1 = ray.col + dir1[1];
            let ray1: Ray = {
                row: row1,
                col: col1,
                direction: dir1
            };

            let dir2 = Direction.right;
            let row2 = ray.row + dir2[0];
            let col2 = ray.col + dir2[1];
            let ray2: Ray = {
                row: row2,
                col: col2,
                direction: dir2
            };
            return [ray1, ray2];
        }
    }
}

class Grid {
    grid: Tile[][];
    rows: number;
    cols: number;
    visited: [boolean[], boolean[], boolean[], boolean[]];

    constructor(grid: string[]) {
        this.rows = 0;
        this.cols = 0;
        this.parseGrid(grid);
    }

    private parseGrid(grid: string[]) {
        this.grid = [];
        this.visited = [[], [], [], []];
        for (let line of grid) {
            let row: Tile[] = [];
            for (let char of line) {
                row.push(this.createTile(char));
                this.visited[0].push(false);
                this.visited[1].push(false);
                this.visited[2].push(false);
                this.visited[3].push(false);
            }
            this.grid.push(row);
            this.cols = Math.max(this.cols, row.length);
        }
        this.rows = this.grid.length;
    }

    getRayDirectionIndex(ray: Ray): number {
        if (ray.direction === Direction.up) {
            return 0;
        } else if (ray.direction === Direction.down) {
            return 1;
        } else if (ray.direction === Direction.left) {
            return 2;
        } else {
            return 3;
        }
    }
    setVisited(ray: Ray): boolean {
        if (this.isInBounds(ray)) {
            let directionIndex = this.getRayDirectionIndex(ray);
            let index = ray.row * this.cols + ray.col;
            if (this.visited[directionIndex][index]) {
                return false;
            }
            this.visited[directionIndex][index] = true;
            return true;
        }
        return false;
        
    }

    createTile(tile: string): Tile {
        switch (tile) {
            case '.':
                return new Empty();
            case '/':
                return new ForwardSlashMirror();
            case '\\':
                return new BackSlashMirror();
            case '|':
                return new VerticalSplitter();
            case '-':
                return new HorizontalSplitter();
            default:
                throw new Error('Unknown tile:' + tile);
        }
    }
    isInBounds(ray: Ray): boolean {
        return 0 <= ray.row && ray.row < this.rows
               && 0 <= ray.col && ray.col < this.cols;
    }

    shine(ray: Ray): Ray[] {
        return this.grid[ray.row][ray.col].shine(ray);
    }

    propagateRay(ray: Ray): void {
        let queue = [ray];
        while (true) {
            let r = queue.shift();
            if (r == undefined) {
                break;
            }
            if (this.setVisited(r)) {
                queue = queue.concat(this.shine(r));
            }
        }
    }

    calculateEnergised(ray: Ray): number {
        this.propagateRay(ray);
        let energised = 0;
        for (let i = 0; i < this.visited[0].length; i++) {
            energised += this.visited[0][i]
                         || this.visited[1][i]
                         || this.visited[2][i]
                         || this.visited[3][i] ? 1 : 0;
                         
        }
        return energised
    }

    getEnergisedString(): string {
        let energised = ''
        for (let i = 0; i < this.visited[0].length; i++) {
            energised += this.visited[0][i]
                         || this.visited[1][i]
                         || this.visited[2][i]
                         || this.visited[3][i] ? '#' : '.';
            if (i % this.cols == this.cols - 1) {
                energised += '\n';
            }
        }
        return energised;
    }

    clearVisited(): void {
        for (let i = 0; i < this.visited[0].length; i++) {
            this.visited[0][i] = false;
            this.visited[1][i] = false;
            this.visited[2][i] = false;
            this.visited[3][i] = false;
        }
    }
}

function solve(lines: string[]): void {
    let grid = new Grid(lines);
    let initRay: Ray = {
        row: 0,
        col: 0,
        direction: Direction.right
    }
    let maxEnergised = grid.calculateEnergised(initRay);
    console.log("Part 1:", maxEnergised);
    grid.clearVisited();
    
    let rightRay: Ray = {row: 1, col: 0, direction: Direction.right};
    while (rightRay.row < grid.rows) {
        maxEnergised = Math.max(maxEnergised, grid.calculateEnergised(rightRay));
        grid.clearVisited();
        rightRay.row++;
    }

    let downRay: Ray = {row: 0, col: 0, direction: Direction.down};
    while (downRay.col < grid.cols) {
        maxEnergised = Math.max(maxEnergised, grid.calculateEnergised(downRay));
        grid.clearVisited();
        downRay.col++;
    }

    let leftRay: Ray = {row: 0, col: grid.cols - 1, direction: Direction.down};
    while (leftRay.row < grid.rows) {
        maxEnergised = Math.max(maxEnergised, grid.calculateEnergised(leftRay));
        grid.clearVisited();
        leftRay.row++;
    }

    let upRay: Ray = {row: grid.rows - 1, col: 0, direction: Direction.down};
    while (upRay.col < grid.cols) {
        maxEnergised = Math.max(maxEnergised, grid.calculateEnergised(upRay));
        grid.clearVisited();
        upRay.col++;
    }

    console.log("Part 2:", maxEnergised);
}

function main() {
    let lines: string[] = readFileSync("input16.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
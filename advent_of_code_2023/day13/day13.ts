import {readFileSync} from "fs";

class Surface {
    pattern: string[];
    rows: number;
    cols: number;

    constructor(pattern: string[]) {
        this.pattern = pattern;
        this.rows = pattern.length;
        this.cols = pattern[0].length;
    }

    getReflectionDifference(mode: 'r' | 'c', n: number): number {
        let i1 = n - 1;
        let i2 = n;
        let difference = 0;
        if (mode == 'r') {
            while (i1 >= 0 && i2 < this.rows) {
                for (let i = 0; i < this.cols; i++) {
                    if (this.pattern[i1][i] != this.pattern[i2][i]) {
                        difference++;
                    }
                }
                i1--;
                i2++;
            }
        } else {
            while (i1 >= 0 && i2 < this.cols) {
                for (let i = 0; i < this.rows; i++) {
                    if (this.pattern[i][i1] != this.pattern[i][i2]) {
                        difference++;
                    }
                }
                i1--;
                i2++;
            }
        }

        return difference;
    }
    getScore(mode: 'r' | 'c', n: number): number {
        let multiplier = mode == 'r' ? 100 : 1;
        return n * multiplier;
    } 

    findReflectionScore(threshold=0): number {
        for (let r = 1; r < this.rows; r++) {
            if (this.getReflectionDifference('r', r) == threshold) {
                return this.getScore('r', r);
            }
        }
        for (let c = 1; c < this.cols; c++) {
            if (this.getReflectionDifference('c', c) == threshold) {
                return this.getScore('c', c);
            }
        }
        return 0;
    }
}

function separateSurfaces(patterns: string[]): string[][] {
    let surfaces: string[][] = [[]];
    for (let line of patterns) {
        if (line.length == 0) {
            surfaces.push([]);
        } else {
            surfaces[surfaces.length - 1].push(line);
        }
    }
    return surfaces.filter((x) => x.length > 0);
}
function parseSurfaces(patterns: string[][]): Surface[] {
    let surfaces: Surface[] = [];
    for (let p of patterns) {
        surfaces.push(new Surface(p));
    }
    return surfaces;
}

function solve(lines: string[]): void {
    let patterns = separateSurfaces(lines);
    let surfaces = parseSurfaces(patterns);
    let sumPart1 = 0;
    let sumPart2 = 0;
    for (let s of surfaces) {
        sumPart1 += s.findReflectionScore(0);
        sumPart2 += s.findReflectionScore(1);
    }
    console.log("Part 1:", sumPart1);
    console.log("Part 2:", sumPart2);
}

function main() {
    let lines: string[] = readFileSync("input13.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
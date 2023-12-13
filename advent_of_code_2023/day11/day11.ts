import {readFileSync} from "fs";

interface Star {
    row: number;
    col: number;
}

function getDistance(s1: Star, s2: Star, 
                     emptyRows: number[], emptyCols: number[], 
                     expansion: number): number {
    
    let minR = Math.min(s1.row, s2.row);
    let maxR = Math.max(s1.row, s2.row);
    let minC = Math.min(s1.col, s2.col);
    let maxC = Math.max(s1.col, s2.col);
    let expansions = emptyRows.filter((v) => minR <= v && v < maxR).length + 
                     emptyCols.filter((v) => minC <= v && v < maxC).length;
    return expansions * (expansion - 1) + (maxR - minR) + (maxC - minC);
}

function solve(lines: string[]): void {
    let emptyRows: number[] = [];
    let emptyCols: number[] = [];
    let isEmptyCols: boolean[] = [];
    let stars: Star[] = [];
    for (let r = 0; r < lines.length; r++) {
        let line = lines[r];
        let isEmptyRow = true;
        for (let c = 0; c < line.length; c++) {
            let char = line[c];
            if (c >= isEmptyCols.length) {
                isEmptyCols.push(true);
            }
            if (char === '#') {
                isEmptyRow = false;
                isEmptyCols[c] = false;
                stars.push({row: r, col: c});
            }
        }
        if (isEmptyRow) {
            emptyRows.push(r);
        }
    }
    emptyCols = isEmptyCols.map((v, i) => v ? i : -1)
                           .filter((x) => x != -1)
    
    let distances1 = 0;
    let distances2 = 0;
    for (let i = 0; i < stars.length; i++) {
        for (let j = i + 1; j < stars.length; j++) {
            let star1 = stars[i];
            let star2 = stars[j];
            distances1 += getDistance(star1, star2, emptyRows, emptyCols, 2);
            distances2 += getDistance(star1, star2, emptyRows, emptyCols, 1000000);
        }
    }
    console.log("Part 1:", distances1);
    console.log("Part 2:", distances2);
}

function main() {
    let lines: string[] = readFileSync("input11.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import {readFileSync} from "fs";

type Direction = "U" | "D" | "L" | "R";

interface Step {
    direction: Direction;
    count: number;
    hexDirection: Direction;
    hexCount: number;
}
interface VerticalWall {
    beginRow: number;
    endRow: number;
    col: number;
}
interface Range {
    min: number;
    max: number;
}

function parseDirection(str: string): Direction {
    switch (str) {
        case "U":
            return "U";
        case "D":
            return "D";
        case "L":
            return "L";
        case "R":
            return "R";
        default:
            throw new Error("Unknown direction: " + str);
    }
}

function parseHex(hex: string): [Direction, number] {
    let countStr = hex.slice(0, 5);
    let hexCount = parseInt(countStr, 16);
    let dirStr = hex.charAt(5);
    switch (dirStr) {
        case '0':
            return ["R", hexCount];
        case '1':
            return ["D", hexCount];
        case '2':
            return ["L", hexCount];
        case '3':
            return ["U", hexCount];
        default:
            throw new Error("Unable to parse hex: " + hex);
    }
}

function parseStep(str: string): Step {
    let tokens = str.split(' ');
    let direction = parseDirection(tokens[0]);
    let count = parseInt(tokens[1]);
    let colour = tokens[2].slice(2, tokens[2].length - 1);
    let [hexDirection, hexCount] = parseHex(colour);
    return {direction: direction, count: count, 
            hexCount: hexCount, hexDirection: hexDirection};

}
function parseSteps(lines: string[]): Step[] {
    let steps: Step[] = [];
    for (let line of lines) {
        steps.push(parseStep(line));
    }
    return steps;
}

function getVerticalWalls(steps: Step[], useHex=false) {
    let walls: VerticalWall[] = []
    let col = 0;
    let row = 0;
    for (let s of steps) {
        let direction = s.direction
        let key = 'count';
        if (useHex) {
            direction = s.hexDirection;
            key = 'hexCount'
        }
        let count = s[key];
        switch (direction) {
            case "U":
                walls.push({
                    beginRow: row - count,
                    endRow: row,
                    col: col
                })
                row -= count;
                break;
            case "D":
                walls.push({
                    beginRow: row,
                    endRow: row + count,
                    col: col
                })
                row += count;
                break;
            case "L":
                col -= count;
                break;
            case "R":
                col += count;
                break;
        }
    }
    return walls;
}

class EndPointRow {

    row: number;
    cols: number[];
    isBeginning: boolean[];

    constructor(row: number) {
        this.row = row;
        this.cols = [];
        this.isBeginning = [];
    }
    private insert(c: number, isBeginning: boolean): void {
        let min = 0;
        let max = this.cols.length;
        while (min <= max) {
            let middle = Math.floor((max + min) / 2);
            let middleCol = this.cols[middle];
            if (c < middleCol) {
                max = middle - 1;
            } else {
                min = middle + 1;
            }
        }
        this.cols.splice(min, 0, c);
        this.isBeginning.splice(min, 0, isBeginning);
    }

    addEndPoint(w: VerticalWall): void {
        if (w.beginRow === this.row) {
            this.insert(w.col, true);
        } else if (w.endRow === this.row) {
            this.insert(w.col, false);
        }
    }
}

function addEndPointRow(wall: VerticalWall, endpoints: Map<number, EndPointRow>) {
    let beginning = endpoints.get(wall.beginRow);
    if (beginning === undefined) {
        beginning = new EndPointRow(wall.beginRow);
        endpoints.set(wall.beginRow, beginning);
    }
    beginning.addEndPoint(wall);
    
    let ending = endpoints.get(wall.endRow);
    if (ending === undefined) {
        ending = new EndPointRow(wall.endRow);
        endpoints.set(wall.endRow, ending);
    }
    ending.addEndPoint(wall);
}

function getEndPoints(walls: VerticalWall[]): EndPointRow[] {
    let endPointMap = new Map<number, EndPointRow>();
    for (let w of walls) {
        addEndPointRow(w, endPointMap);
    }
    let endPointRows: EndPointRow[] = [];
    for (let p of endPointMap.values()) {
        endPointRows.push(p);
    }
    return endPointRows;
}

function calculateLineVolume(cols: number[]): number {
    let volume = 0;
    for (let i = 1; i < cols.length; i += 2) {
        volume += cols[i] - cols[i - 1] + 1;
    }
    return volume;
}

function isInRange(n: number, range: Range): boolean {
    return range.min <= n && n <= range.max;
}
function isOverlap(r1: Range, r2: Range): boolean {
    return isInRange(r1.min, r2) || isInRange(r2.min, r1);
}
function getOverlapRange(r1: Range, r2: Range): number {
    if (isOverlap(r1, r2)) {
        let start = r1.min;
        if (isInRange(r2.min, r1)) {
            start = r2.min;
        }
        let end = r1.max;
        if (isInRange(r2.max, r1)) {
            end = r2.max;
        }
        return end - start + 1;
    }
    return 0;
}
function addNewRowVolume(prevCols: number[], nextCols: number[]): number {
    // Adds the area given by the subtraction of previous area and next area.

    let overlap = 0;
    for (let prevIndex = 1; prevIndex < prevCols.length; prevIndex += 2) {
        for (let nextIndex = 1; nextIndex < nextCols.length; nextIndex += 2) {
            let prevRange: Range = {min: prevCols[prevIndex - 1], max: prevCols[prevIndex]};
            let nextRange: Range = {min: nextCols[nextIndex - 1], max: nextCols[nextIndex]};
            overlap += getOverlapRange(prevRange, nextRange);
        }
    }
    let nextVolume = calculateLineVolume(nextCols);
    return nextVolume - overlap
}

function calculateInteriorVolume(endpoints: EndPointRow[]): number {
    endpoints.sort((a, b) => a.row - b.row);
    let totalVolume = 0;
    let lineVolume = 0;
    let prevRow = 0;
    let cols: number[] = [];

    for (let p of endpoints) {
        
        // At an endpoint now. Add up the total area between this and the 
        // previous endpoint. This also adds the area given by the current line.
        totalVolume += lineVolume * (p.row - prevRow);

        let nextCols = cols.filter(() => true);
        for (let i = 0; i < p.cols.length; i++) {
            if (p.isBeginning[i]) {
                nextCols.push(p.cols[i]);
            } else {
                nextCols.splice(nextCols.indexOf(p.cols[i]), 1);
            }
        }
        nextCols.sort((a, b) => a - b);

        // We are at a boundary. We have already added the previous row area.
        // Add the new row area, while making sure we do not overlap.
        totalVolume += addNewRowVolume(cols, nextCols);
        lineVolume = calculateLineVolume(nextCols);
        cols = nextCols;
        prevRow = p.row;
    }
    return totalVolume;
}


function solve(lines: string[]): void {
    let steps = parseSteps(lines);
    
    let walls: VerticalWall[] = getVerticalWalls(steps);
    let endPoints = getEndPoints(walls);
    let numInteriorPart1 = calculateInteriorVolume(endPoints);
    console.log("Part 1:", numInteriorPart1);

    let walls2: VerticalWall[] = getVerticalWalls(steps, true);
    let endPoints2 = getEndPoints(walls2);
    let numInteriorPart2 = calculateInteriorVolume(endPoints2);
    console.log("Part 2:", numInteriorPart2);
}

function main() {
    let lines: string[] = readFileSync("input18.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
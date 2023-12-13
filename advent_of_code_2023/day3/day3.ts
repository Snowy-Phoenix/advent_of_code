import {readFileSync} from "fs";

interface PartMatch {
    part: String;
    row: number;
    col: number;
}
interface Tile {
    id: number;
    value: number;
    char: string;
}

function checkBounds(row: number, col: number, 
                        schematic: string[]): boolean {
    if (0 <= row && row < schematic.length) {
        return 0 <= col && col < schematic[row].length;
    }
    return false;
}
function checkBoundsGrid<T>(row: number, col: number, 
    schematic: T[][]): boolean {
    if (0 <= row && row < schematic.length) {
        return 0 <= col && col < schematic[row].length;
    }
        return false;
}

function getPartsAdjacent(row: number, col: number, schematic: string[]): PartMatch[] {
    var parts: PartMatch[] = [];
    var offsets = [-1, 0, 1];
    for (var rowOffset of offsets) {
        for (var colOffset of offsets) {
            var nextRow = row + rowOffset;
            var nextCol = col + colOffset;
            if (checkBounds(nextRow, nextCol, schematic)) {
                var char = schematic[nextRow][nextCol];
                if (char.match(/[0-9\.]/)) {
                    continue;
                }
                parts.push({part: char, 
                    row: nextRow, 
                    col: nextCol})
                }
            }
        }
    return parts;
}
function parseNumber(row: number, col: number, schematic: string[]): number {
    var rowSchematic = schematic[row];
    var n = 0;
    while (col < rowSchematic.length) {
        var char = rowSchematic[col]
        if (char.match(/[0-9]/)) {
            n *= 10;
            n += parseInt(char);
        } else {
            return n;
        }
        col++;
    }
    return n;
}

function computeGearRatio(row: number, col: number, grid: Tile[][]): number {
    const offsets = [-1, 0, 1];
    var seenIds: number[] = [];
    var ratio = 1;
    for (var rowOffset of offsets) {
        for (var colOffset of offsets) {
            const nextRow = row + rowOffset;
            const nextCol = col + colOffset;
            if (checkBoundsGrid(nextRow, nextCol, grid)) {
                const currTile = grid[nextRow][nextCol];
                if (currTile.value > 0 && !(seenIds.includes(currTile.id))) {
                    seenIds.push(currTile.id)
                    ratio *= currTile.value;
                }
            }
        }
    }
    if (seenIds.length === 2) {
        return ratio;
    }
    return 0;
}

function computeGearRatioSum(grid: Tile[][]): number {
    var ratioSums = 0
    for (var row = 0; row < grid.length; row++) {
        const gridRow = grid[row];
        for (var col = 0; col < gridRow.length; col++) {
            const t = gridRow[col];
            if (t.char === '*') {
                ratioSums += computeGearRatio(row, col, grid);
            }
        }
    }
    return ratioSums;
}

function addTile(gridRow: Tile[], id: number, currNumber: number, char:string, row: number) {
    gridRow.push({
        id: id,
        value: currNumber,
        char: char
    });
}

function solve(schematic: string[]): void {
    enum State {Digits, Parts};

    var grid: Tile[][] = [];
    var id = 0;
    var state: State = State.Parts;
    var sum = 0;
    var adjacentParts: PartMatch[] = [];
    
    for (var row = 0; row < schematic.length; row++) {
        grid.push([]);
        var gridRow = grid[row];
        var currNumber = 0;
        var rowString = schematic[row];
        for (var col = 0; col < rowString.length; col++) {
            var char = schematic[row][col];
            switch (state) {
                case State.Digits:
                    if (!char.match(/[0-9]/) || col === rowString.length - 1) {
                        // Not a digit or the last charactr of the line.
                        state = State.Parts;
                        if (adjacentParts.length > 0) {
                            sum += currNumber;
                        }
                        adjacentParts = [];
                        if (col === rowString.length - 1 && char.match(/[0-9]/)) {
                            addTile(gridRow, id, currNumber, char, row);
                        }
                        currNumber = 0;
                        id++;
                    } else {
                        adjacentParts = adjacentParts.concat(getPartsAdjacent(row, col, schematic))
                    }
                    break;
                case State.Parts:
                    if (char.match(/[0-9]/)) {
                        state = State.Digits;
                        currNumber = parseNumber(row, col, schematic);
                        adjacentParts = adjacentParts.concat(getPartsAdjacent(row, col, schematic))
                    }
                    break;
            }
            if (!(col === rowString.length - 1 && char.match(/[0-9]/))) {
                addTile(gridRow, id, currNumber, char, row);
            }
        }
    }
    console.log("Part 1:", sum);
    console.log("Part 2:", computeGearRatioSum(grid));
}

function main() {
    let lines: string[] = readFileSync("input3.txt", "utf-8").split('\n').map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
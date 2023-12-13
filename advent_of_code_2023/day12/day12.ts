import {readFileSync} from "fs";

interface Nonogram {
    line: string;
    numbers: number[];
}

function create2dArray<T>(rows: number, cols: number, val: () => T): T[][] {
    let arr: T[][] = [];
    for (let r = 0; r < rows; r++) {
        arr.push([]);
        for (let c = 0; c < cols; c++) {
            arr[r].push(val());
        }
    }
    return arr;
}

function parseNonogram(row: string): Nonogram {
    let tokens = row.split(/ |,/);
    let numbers = tokens.slice(1).map((x) => parseInt(x));
    return {line: tokens[0], numbers: numbers};
}

function parseNonograms(lines: string[]): Nonogram[] {
    let nonograms: Nonogram[] = [];
    for (let line of lines) {
        nonograms.push(parseNonogram(line));
    }
    return nonograms;
}

function canFit(line: string, n: number, index: number): boolean {

    if (index - n < -1) {
        return false;
    }
    for (let i = index; i > index - n; i--) {
        let char = line[i];
        if (char == '.') {
            return false;
        }
    }
    if (index - n >= 0) {
        return line[index - n] != '#'
    }
    return true

}

function countPossibleArrangements(nonogram: Nonogram): number {
    // Bottom-up approach.

    // The table is constructed as follows:
    // All values are initialised to 0.
    // row indicates the subset 0:n of numbers. 
    // col indicates the string length.
    // table[r][c] represents the total arrangements of 0:r numbers of the substring 0:c
    let table: number[][] = create2dArray<number>(nonogram.numbers.length + 1,
                                                  nonogram.line.length + 1,
                                                  () => 0);
    let line = nonogram.line;
    let numbers = nonogram.numbers;

    // Base cases when there are no numbers.
    table[0][0] = 1; // empty case
    for (let c = 1; c < table[0].length; c++) {
        table[0][c] = line[c - 1] == '#'? 0 : table[0][c - 1];
    }

    // Iteratively solve for n numbers.
    let nSum = 0;
    for (let n = 0; n < numbers.length; n++) {
        let currN = numbers[n];
        let tableN = n + 1;

        let broken = 0;
        nSum += currN
        for (let c = 0; c < line.length; c++) {
            let char = line[c];
            let tableStrLen = c + 1;
            
            // Not actually required, but does this does save a little time.
            if (char == '#') {
                broken++;
            }
            if (broken > nSum) {
                // Don't need to iterate over the next substring lengths, as they
                // all have 0 possible arrangements because we have more broken springs
                // than the sum of all the numbers.
                break;
            }

            // Count perms where we don't place the block. 
            // If the spring is broken, we must place the block.
            if (char != '#') {
                table[tableN][tableStrLen] = table[tableN][tableStrLen - 1];
            }

            // Count perms where we place the block, if we can.
            if (canFit(line, currN, c)) {
                let prevStrLen = Math.max(0, tableStrLen - currN - 1)
                table[tableN][tableStrLen] += table[tableN - 1][prevStrLen];
            }
        }
    }
    return table[table.length - 1][table[table.length - 1].length - 1];
}

function transformNonograms(nonograms: Nonogram[]): void {
    for (let n of nonograms) {
        let str = n.line;
        let numbers = n.numbers;
        let newStr = str;
        let newNumbers = numbers;
        for (let i = 0; i < 4; i++) {
            newStr += "?" + str;
            newNumbers = newNumbers.concat(numbers);
        }
        n.line = newStr;
        n.numbers = newNumbers;
    }
}

function solve(lines: string[]): void {
    let nonograms = parseNonograms(lines);
    let arrangements = 0;
    for (let n of nonograms) {
        arrangements += countPossibleArrangements(n);
    }
    console.log("Part 1:", arrangements);

    transformNonograms(nonograms);

    arrangements = 0;
    for (let n of nonograms) {
        arrangements += countPossibleArrangements(n);
    }
    console.log("Part 2:", arrangements);

}

function main() {
    let lines: string[] = readFileSync("input12.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
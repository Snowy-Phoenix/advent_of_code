import {readFileSync} from "fs";

function convertWords(line: string) {
    return line.replace(/one/g, "one1one")
    .replace(/two/g, "two2two")
    .replace(/three/g, "three3three")
    .replace(/four/g, "four4four")
    .replace(/five/g, "five5five")
    .replace(/six/g, "six6six")
    .replace(/seven/g, "seven7seven")
    .replace(/eight/g, "eight8eight")
    .replace(/nine/g, "nine9nine");
}

function getDigits(line: string, part2=false): number {
    if (part2) {
        line = convertWords(line);
    }
    let digits = [-1,-1];
    for (let c of line) {
        if (c.match("[0-9]")) {
            if (digits[0] === -1) {
                digits[0] = parseInt(c);
            }
            digits[1] = parseInt(c);
        }
    }
    if (digits[0] === -1) {
        return 0;
    }
    return 10 * digits[0] + digits[1];
}

function solve(lines: string[]): void {
    let sum1 = 0;
    let sum2 = 0;
    for (let line of lines) {
        sum1 += getDigits(line);
        sum2 += getDigits(line, true);
    }
    console.log("Part 1:", sum1);
    console.log("Part 2:", sum2);
}

function main() {
    let lines: string[] = readFileSync("input1.txt", "utf-8").split('\n').map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
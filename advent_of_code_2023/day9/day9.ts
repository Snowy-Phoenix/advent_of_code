import {readFileSync} from "fs";

function extendSequence(numbers: number[]): [number, number] {
    let next: number[] = [];
    if (numbers.length <= 1) {
        return [numbers[0], numbers[0]];
    } else {
        for (let i = 1; i < numbers.length; i++) {
            next.push(numbers[i] - numbers[i - 1]);
        }
    }
    let nextSequence = extendSequence(next);
    return [numbers[0] - nextSequence[0], numbers[numbers.length - 1] + nextSequence[1]];
}

function solve(lines: string[]): void {
    let sumNext = 0;
    let sumPrev = 0;
    for (let line of lines) {
        if (line.length == 0) {
            continue;
        }
        let numbers = line.split(" ").map((x) => parseInt(x));
        let [prev, next] = extendSequence(numbers);
        sumNext += next;
        sumPrev += prev;
    }
    console.log("Part 1:", sumNext);
    console.log("Part 2:", sumPrev);
}

function main() {
    let lines: string[] = readFileSync("input9.txt", "utf-8").split(/\n/).map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
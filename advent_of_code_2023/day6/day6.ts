import {readFileSync} from "fs";

function parseData(data: string): number[] {
    return data.split(/ +/)
               .map((x) => parseInt(x))
               .filter((x) => !Number.isNaN(x));
}

function getRange(time: number, record: number) {
    // d(b) = b * (t - b) - r
    // where,
    //   d(b) = difference between distance travelled and record with respect to b.
    //      b = button held down time
    //      t = maximum time
    //      r = record time
    // We want d(b) > 0, meaning we have beaten the record. 
    // We solve for b using the quadratic equation.

    let min = Math.ceil((time - Math.sqrt(time**2 - 4*record))/2 + 1);
    let max = Math.floor((time + Math.sqrt(time**2 - 4*record))/2 + 1);
    return max - min + 1;
}

function concatNumbers(numbers: number[]): number {
    let str = "";
    for (let n of numbers) {
        str += n;
    }
    return parseInt(str);
}

function solvePart1(times: number[], record: number[]): number {
    let prod = 1;
    for (let i = 0; i < times.length; i++) {
        prod *= getRange(times[i], record[i]);
    }
    return prod;
}

function solve(data: string[]): void {
    let times = parseData(data[0]);
    let record = parseData(data[1]);
    let prod = solvePart1(times, record);
    console.log("Part 1:", prod);
    let concatTime = concatNumbers(times);
    let concatRecord = concatNumbers(record);
    console.log("Part 2:", getRange(concatTime, concatRecord));
}

function main() {
    let lines: string[] = readFileSync("input6.txt", "utf-8").split(/\n/).map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
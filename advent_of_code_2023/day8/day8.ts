import {readFileSync} from "fs";

interface NodeMap {
    [key: string]: [string, string];
}
interface Cycle {
    [key: number]: string;
    offset: number;
    length: number;
    cycleLength: number;
}

function gcd(a: number, b: number): number {
    return b === 0 ? a : gcd(b, a % b);
}
function lcm(a: number, b: number): number {
  return (a * b) / gcd(a, b);
}

function parseNode(line: string): [string, string, string] {
    let words = line.split(/ = \(/);
    let key = words[0]
    let leftRight = words[1].split(/, /)
    let left = leftRight[0];
    let right = leftRight[1].replace("\)", "");
    return [key, left, right];
}
function parseMap(lines: string[]): [NodeMap, string] {
    let directions = lines[0];
    let map: NodeMap = {};
    for (let i = 2; i < lines.length; i++) {
        let currentLine = lines[i];
        if (currentLine.length == 0) {
            continue;
        }
        let [key, left, right] = parseNode(currentLine);
        map[key] = [left, right];
    }
    return [map, directions];
}
function solvePart1(map: NodeMap, directions: string): number {
    let currentNode = "AAA";
    let steps = 0
    while (currentNode != "ZZZ") {
        let d = directions[steps % directions.length];
        if (d == 'L') {
            currentNode = map[currentNode][0];
        } else {
            currentNode = map[currentNode][1];
        }
        steps++;
    }
    return steps;
}
function mapCycle(map: NodeMap, directions: string, node: string, ): Cycle {
    
    let steps = 0
    let cycle: Cycle = {offset: 0, length:0, cycleLength:0};
    let visited = {};
    let currentNode = node;
    while (true) {
        let key = currentNode + (steps % directions.length).toString();
        if (key in visited) {
            cycle["offset"] = visited[key];
            cycle["length"] = steps;
            cycle["cycleLength"] = steps - visited[key];
            break;
        } else {
            visited[key] = steps;
            cycle[steps] = currentNode;
        }
        let d = directions[steps % directions.length];
        if (d == 'L') {
            currentNode = map[currentNode][0];
        } else {
            currentNode = map[currentNode][1];
        }
        steps++;
    }
    return cycle;
}

function findZ(c: Cycle, offset: number, multiplier: number): [number, number] {
    let steps = 0;
    let currentIndex = offset;
    if (offset > c.offset) {
        currentIndex = ((currentIndex - c.offset) % c.cycleLength) + c.offset;
    }
    while (steps < c.length) {
        if (c[currentIndex][2] == "Z") {
            return [steps*multiplier + offset, lcm(c.cycleLength, multiplier)];
        }
        steps += 1;
        currentIndex += multiplier;
        if (currentIndex >= c.length) {
            currentIndex = ((currentIndex - c.offset) % c.cycleLength) + c.offset;
        }
    }
    return [0, 0];
}
function solvePart2(map: NodeMap, directions: string): number {

    let aNodes: string[] = [];
    for (let key in map) {
        if (key[2] == 'A') {
            aNodes.push(key);
        }
    }

    let cycles: Cycle[] = [];
    for (let n of aNodes) {
        cycles.push(mapCycle(map, directions, n));
    }
    
    let offset = 0;
    let multiplier = 1;
    for (let c of cycles) {
        [offset, multiplier] = findZ(c, offset, multiplier);
    }
    return offset;
}


function solve(lines: string[]): void {
    let [map, directions] = parseMap(lines);
    
    let stepsPart1 = solvePart1(map, directions);
    console.log("Part 1:", stepsPart1);

    let stepsPart2 = solvePart2(map, directions);
    console.log("Part 2:", stepsPart2);
}

function main() {
    let lines: string[] = readFileSync("input8.txt", "utf-8").split(/\n/).map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
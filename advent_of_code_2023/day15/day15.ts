import {readFileSync} from "fs";

interface Hashable {
    isEqual(other: Hashable): boolean;
    hash(): number;
}

class Step implements Hashable {
    rawString: string
    name: string
    instruction: string
    param: number

    constructor(str: string) {
        this.rawString = str;
        this.parseStep(str);
    }
    
    parseStep(str: string) {
        let tokens = str.split(/-|=/);
        this.name = tokens[0];
        if (tokens[1].length == 0) {
            this.instruction = '-';
            this.param = 0;
        } else {
            this.instruction = '=';
            this.param = parseInt(tokens[1]);
        }
    }
    isEqual(other: Hashable): boolean {
        if (other instanceof Step) {
            return other.name == this.name;
        }
        return false;
    }

    hash(): number {
        let currValue = 0;
        for (let i = 0; i < this.name.length; i++) {
            currValue += this.name.charCodeAt(i);
            currValue *= 17;
        }
        return currValue;
    }

    hashRaw(): number {
        let currValue = 0;
        for (let i = 0; i < this.rawString.length; i++) {
            currValue += this.rawString.charCodeAt(i);
            currValue *= 17;
        }
        return currValue;
    }
}

class HashMapBucket<E extends Hashable, V> {
    elements: E[];
    values: V[];

    constructor() {
        this.elements = [];
        this.values = [];
    }

    update(elem: E, val: V): void {
        for (let i = 0; i < this.elements.length; i++) {
            let e = this.elements[i];
            if (e.isEqual(elem)) {
                this.values[i] = val;
                return;
            }
        }
        this.elements.push(elem);
        this.values.push(val);
    }
    remove(elem: E): void {
        let i = this.elements.findIndex((v) => v.isEqual(elem));
        if (i != -1) {
            this.elements.splice(i, 1);
            this.values.splice(i, 1);
        }
    }
}
class HashMap<E extends Hashable, V> {
    boxes: HashMapBucket<E, V>[];
    numBoxes: number;

    constructor(boxes=256) {
        this.numBoxes = boxes;
        this.boxes = [];
        for (let i = 0; i < boxes; i++) {
            this.boxes.push(new HashMapBucket());
        }
    }

    update(elem: E, val: V): void {
        let i = elem.hash() % this.numBoxes;
        this.boxes[i].update(elem, val);
    }
    remove(elem: E): void {
        let i = elem.hash() % this.numBoxes;
        this.boxes[i].remove(elem);
    }
}

function parseSteps(lines: string): Step[] {
    let stepStrings = lines.split(',');
    let steps: Step[] = []
    for (let word of stepStrings) {
        steps.push(new Step(word));
    }
    return steps;
}
function solvePart1(steps: Step[]): number {
    let sum = 0;
    for (let s of steps) {
        sum += s.hashRaw() % 256;
    }
    return sum;
}

function computePower(hashMap: HashMap<Step, number>): number {
    let power = 0;
    for (let b = 0; b < hashMap.numBoxes; b++) {
        let box = hashMap.boxes[b];
        for (let i = 0; i < box.values.length; i++) {
            power += (b + 1) * box.values[i] * (i + 1);
        }
    }
    return power
}

function solvePart2(steps: Step[]): number {
    let hashMap = new HashMap<Step, number>();
    for (let s of steps) {
        if (s.instruction == '=') {
            hashMap.update(s, s.param);
        } else {
            hashMap.remove(s);
        }
    }
    return computePower(hashMap);
}

function solve(lines: string[]): void {
    let steps = parseSteps(lines[0])
    console.log("Part 1:", solvePart1(steps));
    console.log("Part 2:", solvePart2(steps));
}

function main() {
    let lines: string[] = readFileSync("input15.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
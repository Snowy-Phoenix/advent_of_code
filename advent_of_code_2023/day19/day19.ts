import {readFileSync} from "fs";

type Category = "x" | "m" | "a" | "s";

const MINIMUM: Part = {
    x: 1,
    m: 1,
    a: 1,
    s: 1
}
const MAXIMUM: Part = {
    x: 4001,
    m: 4001,
    a: 4001,
    s: 4001
}

interface Rule {
    accept: string;

    eval(part: Part): boolean;
    split(range: PartRange): [PartRange | null, PartRange | null];
}

class GreaterThan implements Rule {
    param: Category
    value: number
    accept: string;

    constructor(param: Category, value: number, accept: string) {
        this.param = param;
        this.value = value;
        this.accept = accept;
    }
    split(range: PartRange): [PartRange | null, PartRange | null] {
        if (this.eval(range.minPart)) {
            // The whole range true.
            return [range, null];
        } else if (this.eval(range.maxPart)) {
            // Partially true.
            let trueRange = range.copy();
            let falseRange = range.copy();
            trueRange.setMin(this.param, this.value + 1);
            falseRange.setMax(this.param, this.value + 1);
            
            return [trueRange, falseRange];
        } else {
            return [null, range];
        }
    }

    eval(part: Part): boolean {
        switch (this.param) {
            case "x":
                return part.x > this.value;
            case "m":
                return part.m > this.value;
            case "a":
                return part.a > this.value;
            case "s":
                return part.s > this.value;
        }
    }
}
class LessThan implements Rule {
    param: Category;
    value: number;
    accept: string;

    constructor(param: Category, value: number, accept: string) {
        this.param = param;
        this.value = value;
        this.accept = accept;
    }

    eval(part: Part): boolean {
        switch (this.param) {
            case "x":
                return part.x < this.value;
            case "m":
                return part.m < this.value;
            case "a":
                return part.a < this.value;
            case "s":
                return part.s < this.value;
        }
    }
    split(range: PartRange): [PartRange | null, PartRange | null] {
        if (this.eval(range.maxPart)) {
            // The whole range true.
            return [range, null];
        } else if (this.eval(range.minPart)) {
            // Partially true.
            let trueRange = range.copy();
            let falseRange = range.copy();
            trueRange.setMax(this.param, this.value);
            falseRange.setMin(this.param, this.value);
            return [trueRange, falseRange];
        } else {
            return [null, range];
        }
    }
}

class Workflow {

    rules: Rule[];
    else: string;

    constructor(rules: Rule[], _else: string) {
        this.rules = rules;
        this.else = _else;
    }
    eval(p: Part): string {
        for (let r of this.rules) {
            if (r.eval(p)) {
                return r.accept;
            }
        }
        return this.else;
    }
    getRangesAccepted(range: PartRange, workflowMap: Map<string, Workflow>, depth=0): number {
        if (depth > workflowMap.size) {
            return 0;
        }
        let currentRange = range;
        let accepted = 0;
        for (let r of this.rules) {
            let [t, f] = r.split(currentRange);
            if (t !== null) {
                let name = r.accept;
                if (name === 'A') {
                    accepted += t.getCombinations();
                } else if (name !== 'R') {
                    let next = workflowMap.get(name);
                    if (next) {
                        accepted += next.getRangesAccepted(t, workflowMap, depth + 1);
                    }
                }
            }
            if (f !== null) {
                currentRange = f;
            } else {
                return accepted;
            }
        }
        if (this.else === 'A') {
            return accepted + currentRange.getCombinations();
        } else if (this.else === 'R') {
            return accepted;
        } else {
            let next = workflowMap.get(this.else);
            if (next) {
                return accepted + next.getRangesAccepted(currentRange, workflowMap, depth + 1);
            }
        }
        return accepted;
    }
}

type Part = {
    [key in Category]: number;
};

class PartRange {
    minPart: Part;
    maxPart: Part; // Endpoint exclusive

    constructor(minPart: Part, maxPart: Part) {
        this.minPart = minPart;
        this.maxPart = maxPart;
    }

    split(rule: Rule): [PartRange | null, PartRange | null] {
        // Returns a pair of ranges that are true and false respectively
        return rule.split(this);
    }

    getCombinations(): number {
        return (this.maxPart.x - this.minPart.x) 
             * (this.maxPart.m - this.minPart.m)
             * (this.maxPart.a - this.minPart.a)
             * (this.maxPart.s - this.minPart.s);
    }
    private copyPart(p: Part): Part {
        return {
            x: p.x,
            m: p.m,
            a: p.a,
            s: p.s
        };
    }
    copy(): PartRange {
        return new PartRange(this.copyPart(this.minPart), this.copyPart(this.maxPart))
    }
    setMax(key: Category, n: number): void {
        this.maxPart[key] = Math.max(n, this.minPart[key]);
    }
    setMin(key: Category, n: number): void {
        this.minPart[key] = Math.min(n, this.maxPart[key]);
    }
}

function parseCategory(category: string): Category {
    switch (category) {
        case 'x':
            return 'x';
        case 'm':
            return 'm';
        case 'a':
            return 'a';
        case 's':
            return 's';
        default:
            throw new Error("Unknown Category: " + category);
    }
}
function parseRules(rules: string[]): [Rule[], string] {
    let elseRule = rules[rules.length - 1]
    let ruleArray: Rule[] = [];
    for (let i = 0; i < rules.length - 1; i++) {
        let match = rules[i].match(/(.+)(<|>)(\d+):(.+)/);
        if (match == null || match.length < 5) {
            throw new Error("Unable to parse rule:" + rules[i]);
        }
        let category = parseCategory(match[1])
        switch (match[2]) {
            case '<':
                ruleArray.push(new LessThan(category, parseInt(match[3]), match[4]));
                break;
            case '>': 
                ruleArray.push(new GreaterThan(category, parseInt(match[3]), match[4]));
                break;
            default:
                throw new Error("Unknown operator in rule:" + rules[i]);
        }

    }
    return [ruleArray, elseRule];
}

function parseWorkflow(line: string): [string, Workflow] {
    let match = line.match(/(.+){(.+)}/);
    if (match === null || match.length < 3) {
        throw new Error("Unable to parse Workflow: " + line);
    }
    let name = match[1];
    try {
        let [rules, _else] = parseRules(match[2].split(/,/));
        return [name, new Workflow(rules, _else)];
    } catch {
        throw new Error("Unable to parse Workflow: " + line);
    }
}
function parseWorkflows(workflowLines: string[]): Map<string, Workflow> {
    let workflowMap = new Map<string, Workflow>();
    for (let str of workflowLines) {
        if (str.length == 0) {
            continue;
        }
        let [name, workflow] = parseWorkflow(str);
        workflowMap.set(name, workflow);
    }
    return workflowMap;
}
function parseParts(partLines: string[]): Part[] {
    let parts: Part[] = [];
    for (let line of partLines) {
        if (line.length == 0) {
            continue;
        }
        let match = line.match(/{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}/);
        if (match === null || match.length < 5) {
            throw new Error("Unable to parse Part: " + line);
        }
        parts.push({
            x: parseInt(match[1]),
            m: parseInt(match[2]),
            a: parseInt(match[3]),
            s: parseInt(match[4])
        })
    }
    return parts;
}

function isAccepted(p: Part, workflowMap: Map<string, Workflow>): boolean {
    let currentWorkflow = 'in';
    let i = 0
    while (i < workflowMap.size) {
        let w = workflowMap.get(currentWorkflow);
        if (w) {
            let output = w.eval(p);
            if (output == 'R') {
                return false;
            } else if (output == 'A') {
                return true;
            } else {
                currentWorkflow = output;
            }
        } else {
            return false;
        }
        i++;
    }
    return false;

}
function partSum(p: Part): number {
    return p.x + p.m + p.a + p.s;
}

function solvePart2(range: PartRange, workflow: string, 
                    workflowMap: Map<string, Workflow>): number {
    let w = workflowMap.get(workflow);
    if (w === undefined) {
        return 0;
    }
    return w.getRangesAccepted(range, workflowMap);
    

}

function solve(lines: string[]): void {
    let split = lines.findIndex((v) => v.length == 0);
    let workflowMap = parseWorkflows(lines.slice(0, split));
    let parts = parseParts(lines.slice(split + 1));

    let sum = 0;
    for (let p of parts) {
        if (isAccepted(p, workflowMap)) {
            sum += partSum(p);
        }
    }
    console.log("Part 1:", sum);

    let range = new PartRange(MINIMUM, MAXIMUM);
    console.log("Part 2:", solvePart2(range, 'in', workflowMap));

}

function main() {
    let lines: string[] = readFileSync("input19.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
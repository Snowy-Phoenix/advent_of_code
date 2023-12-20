import {readFileSync} from "fs";

type Pulse = "high" | "low";

interface PulseStats {
    high: number;
    low: number;
}

abstract class Module {

    name: string;
    destination: Module[];
    source: Module[];

    constructor(name: string) {
        this.name = name;
        this.destination = [];
        this.source = [];
    }

    abstract pulse(p: Pulse, from: Module): [Pulse, Module][];

    addDestination(m: Module) {
        this.destination.push(m);
    }
    addSource(m: Module) {
        this.source.push(m);
    }
    abstract resetState(): void;
}
class FlipFlopModule extends Module {
    on: boolean
    constructor(name: string) {
        super(name);
        this.on = false;
    }
    pulse(p: Pulse): [Pulse, Module][] {
        let output: [Pulse, Module][] = [];
        if (p === "low") {
            let pulse: Pulse = this.on ? "low" : "high";
            this.on = !this.on;
            for (let dest of this.destination) {
                output.push([pulse, dest]);
            }
        }
        return output;
    }
    resetState(): void {
        this.on = false;
    }
}
class ConjunctionModule extends Module {

    memory: Map<string, boolean>;
    count: number;
    
    constructor(name: string) {
        super(name);
        this.memory = new Map();
        this.count = 0
    }
    private updateMemory(p: Pulse, m: Module): void {
        let prev = this.memory.get(m.name);
        if (prev === undefined) {
            console.log(this.name, this.memory);
            throw new Error("Key Error: " + m.name);
        }
        if (p === "high") {
            this.memory.set(m.name, true);
            this.count += prev === true ? 0 : 1;
        } else {
            this.memory.set(m.name, false);
            this.count += prev === false ? 0 : -1;
        }
    }
    private allHigh(): boolean {
        return this.count === this.memory.size;
    }
    pulse(p: Pulse, from: Module): [Pulse, Module][] {
        this.updateMemory(p, from);
        let pulse: Pulse = this.allHigh() ? "low" : "high";
        let output: [Pulse, Module][] = [];
        for (let dest of this.destination) {
            output.push([pulse, dest]);
        }
        
        return output;
    }
    addSource(m: Module) {
        this.source.push(m);
        this.memory.set(m.name, false);
    }
    resetState(): void {
        for (let name of this.memory.keys()) {
            this.memory.set(name, false);
        }
        this.count = 0;
    }
}
class BroadcasterModule extends Module {

    pulse(p: Pulse): [Pulse, Module][] {
        let output: [Pulse, Module][] = [];
        for (let dest of this.destination) {
            output.push([p, dest]);
        }
        return output;
    }
    resetState(): void {}
}

class Machine {
    modules: Map<string, Module>

    constructor(modules: string[]) {
        this.modules = this.parseModules(modules);
    }

    private parseName(name: string): Module {
        switch (name.charAt(0)) {
            case '%': 
                return new FlipFlopModule(name.slice(1));
            case '&':
                return new ConjunctionModule(name.slice(1));
            case 'b':
                return new BroadcasterModule(name);
            default:
                throw new Error("Unable to parse module name: " + name);
        }
    }

    private parseModules(lines: string[]): Map<string, Module> {
        let moduleMap = new Map<string, Module>();
        let nameDestinations = new Map<string, string[]>();
        for (let line of lines) {
            let nameDest = line.split(/ -> /);
            let module = this.parseName(nameDest[0]);
            let destinations = nameDest[1].split(/, /);
            nameDestinations.set(module.name, destinations);
            moduleMap.set(module.name, module);
        }
        for (let currModule of moduleMap.values()) {
            let destinations = nameDestinations.get(currModule.name);
            if (destinations) {
                for (let dest of destinations) {
                    let destModule = moduleMap.get(dest);
                    if (destModule === undefined) {
                        destModule = new BroadcasterModule(dest);
                        moduleMap.set(dest, destModule);
                    }
                    currModule.addDestination(destModule);
                    destModule.addSource(currModule);
                }
            }
        }
        return moduleMap;
    }

    reset(): void {
        for (let m of this.modules.values()) {
            m.resetState();
        }
    }
    getModule(key: string): Module {
        let m = this.modules.get(key);
        if (m === undefined) {
            throw new Error("Unable to find module: " + key);
        }
        return m;
    }
    pressButton(name = 'broadcaster', pulse: Pulse = 'low'): PulseStats {
        let first = this.modules.get(name);
        if (first === undefined) {
            return { high: 0, low: 0 };
        }

        let stats: PulseStats = { high: 0, low: 0 };
        let queue: [Pulse, Module, Module][] = [[pulse, first, first]];

        while (true) {
            let element = queue.shift();
            if (element == undefined) {
                return stats;
            }
            let [pulse, module, from] = element;
            updatePulseStats(pulse, stats);
            let pulses = module.pulse(pulse, from);
            for (let p of pulses) {
                queue.push([p[0], p[1], module]);
            }
        }
    }
    pressButtonRepeatedly(modules: Machine, times: number, 
        name = 'broadcaster', pulse: Pulse = 'low'): PulseStats {
        let stats = { high: 0, low: 0 };
        for (let i = 0; i < times; i++) {
            stats = addPulseStats(stats, modules.pressButton(name, pulse));
        }
        return stats;
    }
}

function updatePulseStats(pulse: Pulse, stats: PulseStats): void {
    switch (pulse) {
        case "high":
            stats.high++;
            break;
        case "low":
            stats.low++;
            break;
    }
}
function addPulseStats(stats1: PulseStats, stats2: PulseStats): PulseStats {
    return {high: stats1.high + stats2.high, low: stats1.low + stats2.low};
}

function pressButtonTesting(modules: Map<string, Module>, iteration: number): void {
    let first = modules.get('broadcaster');
    if (first === undefined) {
        return;
    }

    let queue: [Pulse, Module, Module][] = [["low", first, first]];

    while (true) {
        let element = queue.shift();
        if (element == undefined) {
            return;
        }
        let [pulse, module, from] = element;
        if (from.name === "ft" && pulse == 'high') {
            console.log("ft:", iteration);
        } else if (from.name === "jz" && pulse == 'high') {
            console.log("jz:", iteration);
        } else if (from.name === "sv" && pulse == 'high') {
            console.log("sv:", iteration);
        } else if (from.name === "ng" && pulse == 'high') {
            console.log("ng:", iteration);
        }
        let pulses = module.pulse(pulse, from);
        for (let p of pulses) {
            queue.push([p[0], p[1], module]);
        }
    }
}

function createCycleLengthMap(parent: Module) {
    let sources = parent.source;
    let cycleLength = new Map<string, number>();
    for (let m of sources) {
        cycleLength.set(m.name, -1);
    }
    return cycleLength;
}

function solvePart2(modules: Machine) {
    let rx = modules.getModule('rx');
    let parent = modules.getModule(rx.source[0].name);

    let cycleLength = createCycleLengthMap(parent);
    let count = 0;

    let i = 1;
    parent["origPulse"] = parent.pulse;
    parent.pulse = (p, from) => {
        if (p == "high") {
            let m = cycleLength.get(from.name);
            if (m !== undefined && m === -1) {
                count++;
                cycleLength.set(from.name, i);
            }
        }
        if (parent === undefined) {
            throw new Error("Undefined function.");
        }
        return parent["origPulse"](p, from);
    };

    while (true) {
        modules.pressButton();
        if (count === cycleLength.size) {
            break;
        }
        i++;
    }
    let multiplier = 1;
    for (let n of cycleLength.values()) {
        multiplier *= n;
    }
    return multiplier;
}

function solve(lines: string[]): void {
    let modules = new Machine(lines);
    let stats = modules.pressButtonRepeatedly(modules, 1000);
    console.log("Part 1:", stats.low * stats.high);
    
    modules.reset();

    let multiplier = solvePart2(modules);
    console.log("Part 2:", multiplier);

    // for (let i = 1; i <= 20000; i++) {
    //     pressButtonTesting(modules, i);
    // }
}

function main() {
    let lines: string[] = readFileSync("input20.txt", "utf-8")
                            .split(/\n/)
                            .map(x => x.trim())
                            .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
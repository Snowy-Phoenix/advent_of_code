import {readFileSync} from "fs";

class Range {
    
    start: number; // Endpoints are inclusive
    end: number;

    constructor(start: number, range: number, useRange=true) {
        this.start = start;
        if (useRange) {
            this.end = start + range - 1; // Endpoints are inclusive
            return;
        }
        this.end = range;
    }

    isInRange(n: number): boolean {
        return this.start <= n && n <= this.end;
    }

    getOffset(n: number): number {
        return n - this.start;
    }

    isOverlap(range: Range): boolean {
        return this.isInRange(range.start) 
            || this.isInRange(range.end) 
            || range.isInRange(this.start)
            || range.isInRange(this.end);
    }
    /** Computes the subtraction (region of non overlap) between this and range. */
    getSubtractedRange(range: Range): Range[] {
        let overlap = this.getIntersectionRange(range);
        if (overlap == null) {
            return [range];
        }
        let output: Range[] = [];
        if (overlap.start != this.start) {
            output.push(new Range(this.start, overlap.start - 1, false));
        }
        if (overlap.end != this.end) {
            output.push(new Range(overlap.end + 1, this.end, false))
        }
        return output;
    }

    /** Computes the intersection (region of overlap) of this and range. */
    getIntersectionRange(range: Range): Range | null {
        let start = 0;
        
        // Start
        if (this.isInRange(range.start)) {
            // Starts within region?
            start = range.start;
        } else if (range.isInRange(this.start)) {
            // Starts out of region, but enters region.
            start = this.start;
        } else {
            // Non overlapping
            return null;
        }
        let end = 0;
        // End
        if (this.isInRange(range.end)) {
            // Ends within region?
            end = range.end;
        } else if (range.isInRange(this.end)) {
            // Ends out of the region?
            end = this.end;
        } else {
            // Should not happen.
            console.error("Impossible region overlapping between %o and %o", this, range);
            return null;
        }
        return new Range(start, end, false);
    }
}

class Conversion {
    source: Range;
    destination: Range;
    range: number;

    constructor(destination: number, source: number, range: number) {
        this.source = new Range(source, range);
        this.destination = new Range(destination, range);
        this.range = range;
    }

    isInRange(n: number): boolean {
        return this.source.isInRange(n);
    }
    convert(n: number): number {
        if (this.isInRange(n)) {
            let offset = this.source.getOffset(n);
            return this.destination.start + offset;
        }
        return n;
    }
    isOverlap(range: Conversion | Range): boolean {
        if ("source" in range) {
            return this.source.isOverlap(range.source);
        } else {
            return this.source.isOverlap(range);
        }
    }
    /** Computes the subtraction (region of non overlap) between this and range. */
    getSubtractedRange(range: Conversion | Range): Range[] {
        if ("source" in range) {
            return this.source.getSubtractedRange(range.source);
        } else {
            return this.source.getSubtractedRange(range);
        }
    }
    /** Computes the intersection (region of overlap) of this and range. */
    getIntersectionRange(range: Conversion | Range): Range | null {
        if ("source" in range) {
            return this.source.getIntersectionRange(range.source);
        } else {
            return this.source.getIntersectionRange(range);
        }
    }
    convertRange(range: Range): Range[] {
        let points = this.getIntersectionRange(range);
        if (points === null) {
            return [range];
        }
        let output: Range[] = [];
        if (points.start != range.start) {
            output.push(new Range(range.start, points.start - 1, false));
        }
        output.push(new Range(this.convert(points.start), 
                              this.convert(points.end), 
                              false));
        if (points.end != range.end) {
            output.push(new Range(range.end + 1, points.end, false));
        }
        return output;
    }
}

class ConversionMap {
    from: string;
    to: string;
    ranges: Conversion[];

    constructor(from: string, to: string) {
        this.from = from;
        this.to = to;
        this.ranges = [];
    }

    addRange(rangeString: string): void {
        let tokens = rangeString.trim().split(/ +/);
        let destination = parseInt(tokens[0]);
        let source = parseInt(tokens[1]);
        let range = parseInt(tokens[2]);
        this.ranges.push(new Conversion(destination, source, range));
    }
    map(n: number): number {
        for (let r of this.ranges) {
            if (r.isInRange(n)) {
                return r.convert(n);
            }
        }
        return n;
    }
    mapRange(range: Range): Range[] {
        let mappedRanges: Range[] = [];
        let unmappedRanges = [range];
        let changed = true;
        while (true) {
            let newUnmapped: Range[] = [];
            changed = false;
            for (let unmapped of unmappedRanges) {
                for (let r of this.ranges) {
                    let overlap = r.getIntersectionRange(unmapped);
                    if (overlap !== null) {
                        changed = true;
                        mappedRanges = mappedRanges.concat(r.convertRange(overlap));
                        newUnmapped = newUnmapped.concat(unmapped.getSubtractedRange(r.source));
                        break;
                    }
                }
            }
            if (!changed || unmappedRanges.length === 0) {
                break;
            }
            unmappedRanges = newUnmapped;
        }
        mappedRanges = mappedRanges.concat(unmappedRanges);
        return mappedRanges;
    }
    
}

interface ConversionMapArray {
    [key: string]: ConversionMap;
}

function parseSeeds(seeds: string): number[] {
    return seeds.split(/ /)
                .map((x) => parseInt(x))
                .filter((x) => !Number.isNaN(x));
}
function parseHeader(header: string): [string, string] {
    let words = header.split(/-to-/);
    let to = words[1].split(/ /)[0];
    return [words[0], to];
}

function parsePlots(plots: string[]): [number[], ConversionMapArray] {
    let seeds: number[] = [];
    let header = true;
    let seedsProcessed = false;
    let currentMap = "";
    let maps: ConversionMapArray = {};
    for (let line of plots) {
        if (line == "") {
            header = true;
        } else if (!seedsProcessed) {
            seeds = parseSeeds(line);
            seedsProcessed = true;
        } else if (header) {
            let [fromMap, toMap] = parseHeader(line);
            header = false;
            maps[fromMap] = new ConversionMap(fromMap, toMap);
            currentMap = fromMap;
        } else {
            let map = maps[currentMap];
            map.addRange(line);
        }
    }
    return [seeds, maps];
}
function toRangeArray(numbers: number[]): Range[] {
    let ranges: Range[] = [];
    for (let i = 1; i < numbers.length; i += 2) {
        ranges.push(new Range(numbers[i - 1], numbers[i]));
    }
    return ranges;
}

function solvePart1(seeds: number[], maps: ConversionMapArray): number {
    let minimum = 2**63;
    for (let value of seeds) {
        let currentMapName = "seed";
        let finalMapName = "location";
        while (currentMapName !== finalMapName) {
            let map = maps[currentMapName]
            value = map.map(value);
            currentMapName = map.to;
        }
        minimum = Math.min(minimum, value);
    }
    return minimum;
}
function solvePart2(ranges: Range[], maps: ConversionMapArray): number {
    let minimum = 2**63;
    for (let r of ranges) {
        let currRanges: Range[] = [r];
        let currentMapName = "seed";
        let finalMapName = "location";
        while (currentMapName !== finalMapName) {
            let nextRanges: Range[] = [];
            let map = maps[currentMapName];
            for (let curr of currRanges) {
                nextRanges = nextRanges.concat(map.mapRange(curr));
            }
            currentMapName = map.to;
            currRanges = nextRanges;
        }
        for (let curr of currRanges) {
            minimum = Math.min(minimum, curr.start);
        }
    }
    return minimum;
}

function solve(plots: string[]): void {
    let [seeds, maps] = parsePlots(plots);
    let part1 = solvePart1(seeds, maps);
    console.log("Part 1:", part1);
    let ranges: Range[] = toRangeArray(seeds);
    let part2 = solvePart2(ranges, maps);
    console.log("Part 2:", part2);
}

function main() {
    let lines: string[] = readFileSync("input5.txt", "utf-8").split(/\n/).map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
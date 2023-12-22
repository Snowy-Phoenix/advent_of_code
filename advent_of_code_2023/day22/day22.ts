import { readFileSync } from "fs";

interface Position {
    x: number;
    y: number;
    z: number;
}

interface Brick {
    id: number;
    start: Position;
    end: Position;
    above: Set<number>;
    below: Set<number>;
}

function addBrick(b: Brick, occupied: Map<string, number>): void {
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            for (let z = b.start.z; z <= b.end.z; z++) {
                let hash = x.toString() + ',' + y.toString() + ',' + z.toString();
                occupied.set(hash, b.id);
            }
        }
    }
}
function removeBrick(b: Brick, occupied: Map<string, number>): void {
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            for (let z = b.start.z; z <= b.end.z; z++) {
                let hash = x.toString() + ',' + y.toString() + ',' + z.toString();
                let a = occupied.delete(hash);
            }
        }
    }
}
function getBelow(b: Brick, occupied: Map<string, number>): Set<number> {
    let below = new Set<number>();
    if (b.start.z == 1) {
        return below;
    }
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            let hash = x + ',' + y + ',' + (b.start.z - 1);
            let n = occupied.get(hash);
            if (n !== undefined) {
                below.add(n);
            }
        }
    }
    return below;
}
function getAbove(b: Brick, occupied: Map<string, number>): Set<number> {
    let above = new Set<number>();
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            let hash = x + ',' + y + ',' + (b.end.z + 1);
            let n = occupied.get(hash);
            if (n !== undefined) {
                above.add(n);
            }
        }
    }
    return above;
}

function canDrop(b: Brick, occupied: Map<string, number>): boolean {
    if (b.start.z === 1) {
        return false;
    }
    return getBelow(b, occupied).size === 0;
}

function parseBricks(lines: string[]): Brick[] {
    let bricks: Brick[] = [];
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let tokens = line.split("~")
        let start = tokens[0].split(",");
        let end = tokens[1].split(",");

        let posStart: Position = { x: parseInt(start[0]), y: parseInt(start[1]), z: parseInt(start[2]) };
        let posEnd: Position = { x: parseInt(end[0]), y: parseInt(end[1]), z: parseInt(end[2]) };
        bricks.push({ id: i, start: posStart, end: posEnd, above: new Set(), below: new Set() });
    }
    return bricks;
}

function settleBricks(bricks: Brick[]): Map<string, number> {
    let brickSorter = function(b1: Brick, b2: Brick): number {
        return b1.start.z - b2.start.z;
    }

    bricks.sort(brickSorter);
    let settledBricks: Map<string, number> = new Map();
    for (let b of bricks) {
        while (canDrop(b, settledBricks)) {
            b.start.z--;
            b.end.z--;
        }
        addBrick(b, settledBricks);
    }
    bricks.sort(brickSorter);
    return settledBricks;
}

function linkBricks(bricks: Brick[], occupied: Map<string, number>): void {
    for (let b of bricks) {
        b.above = getAbove(b, occupied);
        b.below = getBelow(b, occupied);
    }
}

function getBrickFromN(n: number, map: Map<number, Brick>): Brick {
    let b = map.get(n);
    if (b === undefined) {
        throw new Error("Key Error: " + n);
    }
    return b;
}

function getTotalFalling(bricks: Brick[], brickMap: Map<number, Brick>): [number, number] {
    let totalFallen = 0;
    let totalDuds = 0;
    let fallenBricks = new Set<number>();
    for (let currentBrick of bricks) {
        fallenBricks.clear()
        fallenBricks.add(currentBrick.id);
        let queue: Brick[] = [currentBrick];
        while (true) {
            let b = queue.shift();
            if (b === undefined) {
                break;
            }
            let nextFallenBricks = getFallingBricks(b, fallenBricks, brickMap);
            for (let  nextBrick of nextFallenBricks) {
                queue.push(nextBrick);
                fallenBricks.add(nextBrick.id);
            }
        }
        if (fallenBricks.size === 1) {
            totalDuds++;
        } else {
            totalFallen += fallenBricks.size - 1;
        }
    }
    return [totalDuds, totalFallen];
}

function getFallingBricks(b: Brick, fallenBricks: Set<number>, brickMap: Map<number, Brick>): Brick[] {
    let falling: Brick[] = [];
    for (let next of b.above) {
        let nextBrick = getBrickFromN(next, brickMap);
        if (willFall(nextBrick, fallenBricks)) {
            falling.push(nextBrick);
        }
    }
    return falling;
}

function willFall(b: Brick, felled: Set<number>): boolean {
    let willFall = true;
    for (let prev of b.below) {
        if (!felled.has(prev)) {
            willFall = false;
            break;
        }
    }
    return willFall;
}

function generateBrickMap(bricks: Brick[]): Map<number, Brick> {
    let map = new Map<number, Brick>();
    for (let b of bricks) {
        map.set(b.id, b);
    }
    return map;
}

function solve(lines: string[]): void {
    let bricks: Brick[] = parseBricks(lines);
    let brickMap = generateBrickMap(bricks);
    let occupied = settleBricks(bricks);
    linkBricks(bricks, occupied);
    let [duds, fallen] = getTotalFalling(bricks, brickMap)
    console.log("Part 1:", duds);
    console.log("Part 2:", fallen);
}

function main() {
    let lines: string[] = readFileSync("input22.txt", "utf-8")
        .split(/\n/)
        .map(x => x.trim())
        .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
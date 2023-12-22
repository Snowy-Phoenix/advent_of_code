import {readFileSync} from "fs";

interface Position {
    x: number;
    y: number;
    z: number;
}

interface Brick {
    start: Position;
    end: Position;
}

function addBrick(b: Brick, occupied: Set<string>): void {
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            for (let z = b.start.z; z <= b.end.z; z++) {
                let hash = x.toString() + ',' + y.toString() + ',' + z.toString();
                occupied.add(hash);
            }
        }
    }
}
function removeBrick(b: Brick, occupied: Set<string>): void {
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            for (let z = b.start.z; z <= b.end.z; z++) {
                let hash = x.toString() + ',' + y.toString() + ',' + z.toString();
                let a = occupied.delete(hash);
            }
        }
    }
}
function canDrop(b: Brick, occupied: Set<string>): boolean {
    if (b.start.z == 1) {
        return false;
    }
    for (let x = b.start.x; x <= b.end.x; x++) {
        for (let y = b.start.y; y <= b.end.y; y++) {
            let hash = x.toString() + ',' + y.toString() + ',' + (b.start.z - 1).toString();
            if (occupied.has(hash)) {
                return false;
            }
        }
    }
    return true;
}

function solve(lines: string[]): void {
    let bricks: Brick[] = [];
    for (let line of lines) {
        let tokens = line.split("~")
        let start = tokens[0].split(",");
        let end = tokens[1].split(",");

        let posStart: Position = {x: parseInt(start[0]), y: parseInt(start[1]), z: parseInt(start[2])};
        let posEnd: Position = {x: parseInt(end[0]), y: parseInt(end[1]), z: parseInt(end[2])};
        bricks.push({start: posStart, end: posEnd});
    }

    let occupied = new Set<string>() // x,y,z
    for (let b of bricks) {
        addBrick(b, occupied);
    }
    let settled = false;
    while (!settled) {
        settled = true;
        for (let b of bricks) {
            if (canDrop(b, occupied)) {
                settled = false;
                removeBrick(b, occupied);
                b.start.z--;
                b.end.z--;
                addBrick(b, occupied);
            }
        }
    }

    let bricksFallen = 0;
    let canRemove = 0;
    for (let b of bricks) {
        removeBrick(b, occupied);
        let removable = true;
        for (let other of bricks) {
            if (other.start.x == b.start.x 
                && other.start.y == b.start.y 
                && other.start.z == b.start.z) {
                    continue;
                }
            
            if (canDrop(other, occupied)) {
                removable = false;
                let removed = new Map<string, Brick>();
                let settled = false;
                while (!settled) {
                    settled = true;
                    for (let brickToRemove of bricks) {
                        if (canDrop(brickToRemove, occupied)) {
                            let hash = brickToRemove.start.x.toString() + ',' +
                            brickToRemove.start.y.toString() + ',' +
                            brickToRemove.start.z.toString();
                            if (removed.has(hash)) {
                                continue;
                            }
                            removeBrick(brickToRemove, occupied);
                            removed.set(hash, brickToRemove);
                            settled = false;
                        }
                    }
                }
                bricksFallen += removed.size;
                for (let brickToAdd of removed.values()) {
                    addBrick(brickToAdd, occupied);
                }
                break;
            }
        }
        addBrick(b, occupied);
        if (removable) {
            canRemove++;
        }
    }
    console.log(canRemove);
    console.log(bricksFallen);
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
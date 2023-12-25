import { readFileSync } from "fs";

interface Vector3 {
    x: number;
    y: number;
    z: number;
}
interface Vector2 {
    x: number;
    y: number;
}

interface Particle {
    position: Vector3;
    velocity: Vector3;
}

function parseParticles(lines: string[]): Particle[] {
    let particles: Particle[] = [];
    for (let line of lines) {
        let posVel = line.split(/ @ /);
        let position = posVel[0].split(', ').map((x) => parseInt(x));
        let velocity = posVel[1].split(', ').map((x) => parseInt(x));
        let posVect: Vector3 = {x: position[0], y: position[1], z: position[2]};
        let velVect: Vector3 = {x: velocity[0], y: velocity[1], z: velocity[2]};
        particles.push({position: posVect, velocity: velVect});
    }
    return particles;
}
function getIntersection2d(p1: Particle, p2: Particle, referenceVector?: Vector2): [Vector2, number, number] {
    if (referenceVector === undefined) {
        referenceVector = {x:0, y:0};
    }
    let gradient1 = (p1.velocity.y - referenceVector.y) / (p1.velocity.x - referenceVector.x);
    let gradient2 = (p2.velocity.y - referenceVector.y) / (p2.velocity.x - referenceVector.x);
    if (gradient1 === gradient2) {
        return [{x: NaN, y: NaN}, NaN, NaN];
    }
    let denominator = gradient1 - gradient2;
    let numerator = gradient1 * p1.position.x - gradient2 * p2.position.x
                    + p2.position.y - p1.position.y;
    let xIntersect = numerator / denominator;
    let yIntersect = gradient1 * (xIntersect - p1.position.x) + p1.position.y;
    let timeOfIntersect1 = (xIntersect - p1.position.x) / (p1.velocity.x - referenceVector.x);
    let timeOfIntersect2 = (xIntersect - p2.position.x) / (p2.velocity.x - referenceVector.x);
    return [{x: xIntersect, y: yIntersect}, timeOfIntersect1, timeOfIntersect2];
}

function isWithinBounds2d(v: Vector2, lower: number, upper: number): boolean {
    if (isNaN(v.x) || isNaN(v.y)) {
        return false;
    }
    return (lower <= v.x && v.x <= upper && lower <= v.y && v.y <= upper);
}
function solvePart1(particles: Particle[]): number {
    let lowerBound = 200000000000000;
    let upperBound = 400000000000000;
    let withinBounds = 0;
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            let [intersect, time1, time2] = getIntersection2d(particles[i], particles[j]);
            if (time1 < 0 || time2 < 0) {
                continue;
            }
            if (isWithinBounds2d(intersect, lowerBound, upperBound)) {
                withinBounds++;
            }
        }
    }
    return withinBounds;
}

function solve(lines: string[]): void {
    let particles = parseParticles(lines);
    let withinBounds = solvePart1(particles);
    console.log("Part 1:", withinBounds);
    
    for (let x = -500; x <= 500; x++) {
        for (let y = -500; y <= 500; y++) {
            let common = 0;
            let parallel = false;
            let vector: Vector2 = {x: x, y: y};
            let p1 = particles[0];
            let p2 = particles[1];
            let [point, t1, t2] = getIntersection2d(p1, p2, vector);
            if (Number.isNaN(point.x)) {
                continue;
            }
            if (isNaN(point.x) || isNaN(point.y)) {
                continue;
            }
            let isCommon = true;
            for (let i = 2; i < particles.length; i += 1) {
                let p3 = particles[i];
                let p4 = particles[i - 1];
                let [newpoint, t1, t2] = getIntersection2d(p3, p4, vector);
                // console.log(newpoint, t1, t2);
                if (isNaN(newpoint.x)) {
                    if (parallel) {
                        isCommon = false;
                        break;
                    }
                    parallel = true;
                    continue;
                } else if (point.x !== newpoint.x || point.y !== newpoint.y) {
                    // console.log(point, newpoint);
                    isCommon = false;
                    continue;
                }
                common++;
                console.log(p3, "intersect", p4, "at", t1, t2)
            }
            if (isCommon) {
                console.log("c-all", vector, common, point);
                
            } else if (common > 0) {
                console.log("c<all", vector, common, point);
            }
        }
    }

}

function main() {
    let lines: string[] = readFileSync("input24.txt", "utf-8")
        .split(/\n/)
        .map(x => x.trim())
        .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    //x: 201, y: 202
    // Manually extracted values from output.
    // TODO: Generalise this.
    let x = 149909452680584 + (198 - 201) * 165665775938;
    let y = 220522474055239+(-73-202)*165665775938;
    let vz = (215024246295982 + 190 * 165665775938 - (368913364777462 - 107 * 728495792217 ))/(165665775938 - 728495792217);
    let z =  368913364777462 -107 * 728495792217 - vz * 728495792217;
    console.log("Part 2:", x + y + z);
    console.timeEnd("Time taken");
}

main();
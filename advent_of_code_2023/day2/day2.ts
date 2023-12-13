import {readFileSync} from "fs";

interface Match {
    red: number;
    blue: number;
    green: number;
}
interface Game {
    id: number;
    matches: Match[];
}


function parseMatches(line: string): Match[] {
    var matches: Match[] = [];
    var matchStrings = line.split("; ");

    for (var matchString of matchStrings) {
        var red = 0;
        var blue = 0;
        var green = 0;
        var cubes = matchString.split(", ");
        for (let c of cubes) {
            var ncolour = c.split(" ");
            var n = parseInt(ncolour[0]);
            var colour = ncolour[1];
            if (colour === "red") {
                red = Math.max(red, n);
            } else if (colour === "blue") {
                blue = Math.max(blue, n);
            } else if (colour === "green") {
                green = Math.max(green, n);
            }
        }
        var match: Match = {
            red: red,
            blue: blue,
            green: green
        };
        matches.push(match);
    }
    return matches;
}
function parseGame(line: string): Game {
    var gameRolls = line.split(": ");
    var gameId = parseInt(gameRolls[0].split(" ")[1]);
    var matches = parseMatches(gameRolls[1]);
    var game: Game = {
        id: gameId,
        matches: matches
    };
    return game;
}
function parseGames(lines: string[]): Game[] {
    var games: Game[] = []
    for (var line of lines) {
        if (line.length == 0) {
            continue;
        }
        games.push(parseGame(line));
    }
    return games;
}

function isValidGame(game: Game, maxRed: number, 
                     maxGreen: number, maxBlue: number): boolean {
    for (var match of game.matches) {
        if (match.blue > maxBlue ||
            match.green > maxGreen ||
            match.red > maxRed) {
                return false;
            }
    }
    return true;
}
function computePower(game: Game): number {
    var red = 0;
    var blue = 0;
    var green = 0;
    for (var match of game.matches) {
        red = Math.max(match.red, red);
        blue = Math.max(match.blue, blue);
        green = Math.max(match.green, green);
    }
    return red * blue * green;
}

function solve(lines: string[]): void {
    var games = parseGames(lines);
    var sumValidGames = 0;
    var power = 0;
    const REDMAX = 12;
    const GREENMAX = 13;
    const BLUEMAX = 14;
    for (var game of games) {
        if (isValidGame(game, REDMAX, GREENMAX, BLUEMAX)) {
            sumValidGames += game.id;
        }
        power += computePower(game);
    }
    console.log("Part 1:", sumValidGames);
    console.log("Part 2:", power);
}

function main() {
    let lines: string[] = readFileSync("input2.txt", "utf-8").split('\n').map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
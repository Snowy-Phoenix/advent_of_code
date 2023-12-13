import {readFileSync} from "fs";

interface Ticket {
    cardNumber: number;
    winners: number[];
    numbers: number[];
}

function parseNumbers(str: String): number[] {
    return str.trim()
              .split(/ +/)
              .map((v) => parseInt(v));
}

function parseTicket(str: string): Ticket {
    var tokens = str.split(/:|\|/);
    var cardNumber = parseInt(tokens[0].split(/ +/)[1]);
    var winners = parseNumbers(tokens[1]);
    var numbers = parseNumbers(tokens[2]);
    return {cardNumber: cardNumber, 
            winners: winners, 
            numbers: numbers};
}
function parseTickets(ticketStrings: string[]): Ticket[] {
    var tickets: Ticket[] = [];
    for (var line of ticketStrings) {
        if (line.length == 0) {
            continue;
        }
        tickets.push(parseTicket(line));
    }
    return tickets;
}

function countWinningNumbers(ticket: Ticket): number {
    let n = 0;
    for (let winningNumber of ticket.winners) {
        if (ticket.numbers.includes(winningNumber)) {
            n++;
        }
    }
    return n;
}
function calculatePoints(n: number): number {
    if (n == 0) {
        return 0;
    }
    let points = 1;
    for (let i = 1; i < n; i++) {
        points *= 2;
    }
    return points;
}
function getCardIndex(ticket: Ticket): number {
    return ticket.cardNumber - 1
}
function addCards(ticket: Ticket, n: number, cards: number[]): void {
    let currentCards = getCardTotal(ticket, cards);
    let cardi = getCardIndex(ticket);
    for (let i = 1; i <= n; i++) {
        cards[cardi + i] += currentCards;
    }
}
function getCardTotal(ticket: Ticket, cards: number[]): number {
    return cards[getCardIndex(ticket)];
}

function solve(ticketStrings: string[]): void {
    var tickets = parseTickets(ticketStrings);
    var cards = tickets.map(() => 1);
    let totalPoints = 0;
    let totalCards = 0;
    for (var t of tickets) {
        totalCards += getCardTotal(t, cards);
        let winners = countWinningNumbers(t);
        addCards(t, winners, cards);
        totalPoints += calculatePoints(winners);
    }
    console.log("Part 1:", totalPoints);
    console.log("Part 2:", totalCards);
}

function main() {
    let lines: string[] = readFileSync("input4.txt", "utf-8").split('\n').map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import {readFileSync} from "fs";

enum HandQuality {ONE, TWO, TWOPAIR, THREE, FULLHOUSE, FOUR, FIVE}
interface CardCounts {
    [key: string]: number;
}

class Hand {

    hand: string;
    bid: number;
    quality: HandQuality;
    counts: CardCounts;
    jokers: number;
    jokerQuality: HandQuality;

    constructor(hand: string, bid: number) {
        this.hand = hand;
        this.bid = bid;
        this.counts = this.countCards();
        this.jokers = this.countJokers();
        this.quality = this.getQuality();
        this.jokerQuality = this.getJokerQuality();

    }
    calculateWinnings(rank: number) {
        return rank * this.bid;
    }

    countCards(): CardCounts {
        let cards: CardCounts = {};
        for (let h of this.hand) {
            if (!(h in cards)) {
                cards[h] = 0;
            }
            cards[h]++;
        }
        return cards;
    }
    countJokers(): number {
        if (this.jokers === undefined) {
            if ('J' in this.counts) {
                return this.counts['J'];
            }
            return 0;
        } else {
            return this.jokers;
        }
    }
    getQuality(): HandQuality {
        if (this.quality !== undefined) {
            return this.quality;
        }
        let pairs = 0;
        let triples = 0;
        let cards = this.counts;
        for (let key in cards) {
            if (cards[key] == 5) {
                return HandQuality.FIVE;
            } else if (cards[key] == 4) {
                return HandQuality.FOUR;
            } else if (cards[key] == 3) {
                triples++;
            } else if (cards[key] == 2) {
                pairs++;
            }
        }
        if (triples == 1 && pairs == 1) {
            return HandQuality.FULLHOUSE;
        } else if (triples == 1) {
            return HandQuality.THREE;
        } else if (pairs == 2) {
            return HandQuality.TWOPAIR;
        } else if (pairs == 1) {
            return HandQuality.TWO;
        } else {
            return HandQuality.ONE;
        }
    }
    getJokerQuality(): HandQuality {
        if (this.jokerQuality !== undefined) {
            return this.jokerQuality;
        }
        let highestCount = 0;
        let pairs = 0;
        for (let card in this.counts) {
            if (card == "J") {
                continue;
            }
            let count = this.counts[card]
            highestCount = Math.max(count, highestCount);
            if (count == 2) {
                pairs++;
            }
        }
        if (highestCount + this.jokers == 5) {
            return HandQuality.FIVE;
        } else if (highestCount + this.jokers == 4) {
            return HandQuality.FOUR;
        } else if (highestCount + this.jokers == 3) {
            if (pairs == 1 && this.jokers == 0 
                || pairs == 2) {
                return HandQuality.FULLHOUSE;
            } else {
                return HandQuality.THREE;
            }
        } else if (highestCount + this.jokers == 2) {
            if (pairs == 2) {
                return HandQuality.TWOPAIR;
            } else {
                return HandQuality.TWO;
            }
        } else {
            return HandQuality.ONE;
        }
    }
    compareHands(other: Hand, useJoker=false): number {
        let order: String[];
        let quality: number;
        if (useJoker) {
            quality = this.jokerQuality - other.getJokerQuality()
            order = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
        } else {
            quality = this.quality - other.getQuality()
            order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        }
        if (quality == 0) {
            let h1 = this.hand;
            let h2 = other.hand;
            for (let i = 0; i < h1.length; i++) {
                let i1 = order.findIndex((x) => x === h1[i]);
                let i2 = order.findIndex((x) => x === h2[i]);
                if (i1 !== i2) {
                    return i1 - i2;
                }
            }
        }
        return quality;
    }
}

function parseHand(hand: string): Hand {
    let handBid = hand.split(/ /);
    return new Hand(handBid[0], parseInt(handBid[1]));
}
function calculateTotalWinnings(hands: Hand[]): number {
    let winnings = 0;
    for (let i = 0; i < hands.length; i++) {
        let h = hands[i];
        winnings += h.calculateWinnings(i + 1);
    }
    return winnings;
}

function solve(handStrings: string[]): void {
    let hands: Hand[] = [];
    for (let h of handStrings) {
        if (h.length === 0) {
            continue;
        }
        hands.push(parseHand(h));
    }
    hands.sort((x, y) => x.compareHands(y));
    let winnings = calculateTotalWinnings(hands);
    console.log("Part 1:", winnings);
    
    hands.sort((x, y) => x.compareHands(y, true));
    winnings = calculateTotalWinnings(hands);
    console.log("Part 2:", winnings);
}

function main() {
    let lines: string[] = readFileSync("input7.txt", "utf-8").split(/\n/).map(x => x.trim());
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
import { readFileSync } from "fs";

interface Node {
    name: string;
    neighbours: Node[];
}
interface SearchNode {
    node: Node;
    prev: SearchNode | null;
    edge: [string, string];
}

class Graph {
    nodes: Map<string, Node>;
    root: Node;
    edges = 0;

    constructor(lines: string[]) {
        this.parseNodes(lines);
    }

    parseNodes(lines: string[]): void {
        this.nodes = new Map();
        for (let line of lines) {
            this.parseNode(line);
        }
    }

    parseNode(line: string): void {
        let names = line.split(/:? /);
        let parent = this.addNode(names[0]);
        if (this.root === undefined) {
            this.root = parent;
        }
        for (let i = 1; i < names.length; i++) {
            let child = this.addNode(names[i]);
            this.addEdge(parent, child);
        }   
    }

    addNode(name: string): Node {
        let node = this.nodes.get(name);
        if (node !== undefined) {
            return node;
        }
        node = {name: name, neighbours: []};
        this.nodes.set(name, node);
        return node;
    }
    addEdge(n1: Node, n2: Node): void {
        
        for (let n of n1.neighbours) {
            if (n.name === n2.name) {
                return;
            }
        }
        n1.neighbours.push(n2);
        n2.neighbours.push(n1);
        this.edges++;
    }
    solve(): void {
        let num3 = 0;
        for (let endNode of this.nodes.values()) {
            if (endNode.name === this.root.name) {
                continue;
            }
            let flow = 0;
            let residual = new Set<string>();
            while (true) {
                let queue: SearchNode[] = [{node: this.root, prev: null, edge: ['', '']}];
                let visited = new Set<string>();
                visited.add(this.root.name);
                let newFlow = false;
                while (true) {
                    let searchNode = queue.pop();
                    if (searchNode === undefined) {
                        break;
                    }
                    let node = searchNode.node;
                    if (node.name === endNode.name) {
                        flow++;
                        newFlow = true;
                        while (searchNode.prev !== null) {
                            let hash = searchNode.edge[0] + ',' + searchNode.edge[1];                            
                            residual.add(hash);
                            searchNode = searchNode.prev;
                        }
                        break;
                    } else {
                        for (let n of node.neighbours) {
                            let hash = node.name + ',' + n.name;
                            if (residual.has(hash)) {
                                continue;
                            } else if (visited.has(n.name)) {
                                continue;
                            }
                            queue.push({
                                node: n,
                                prev: searchNode,
                                edge: [node.name, n.name]
                            });
                            visited.add(n.name);
                        }
                    }
                }
                if (!newFlow) {
                    break;
                }
            }
            if (flow === 3) {
                num3++;
            }
        }
        console.log("Part 1: ", (this.nodes.size - num3) * num3);
        
    }
}

function solve(lines: string[]): void {
    let g = new Graph(lines);
    g.solve();
}

function main() {
    let lines: string[] = readFileSync("input25.txt", "utf-8")
        .split(/\n/)
        .map(x => x.trim())
        .filter((x => x.length != 0));
    console.time("Time taken");
    solve(lines);
    console.timeEnd("Time taken");
}

main();
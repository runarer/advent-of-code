use std::collections::HashMap;
use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let steps: Vec<(char, char)> = content.lines().map(|line| parse_step(line)).collect();

    let graph = build_graph(steps);

    for (node, nodes) in &graph {
        println!("{},{:?}", node, nodes);
    }

    let order = find_order(&graph);

    println!("Part 1: {}", order);

    Ok(())
}

fn parse_step(line: &str) -> (char, char) {
    let point = line.chars().nth(36).unwrap_or('0');
    let depend_on = line.chars().nth(5).unwrap_or('0');
    return (point, depend_on);
}

fn build_graph(steps: Vec<(char, char)>) -> HashMap<char, Vec<char>> {
    let mut graph: HashMap<char, Vec<char>> = HashMap::new();

    for (step, depend_on) in &steps {
        if !graph.contains_key(step) {
            graph.insert(*step, Vec::new());
        }
        graph.get_mut(step).unwrap().push(*depend_on);
    }

    let mut missing_nodes: Vec<char> = Vec::new();
    // Find missing nodes
    for (_, depend) in &graph {
        for d in depend {
            if !graph.contains_key(d) {
                missing_nodes.push(*d);
            }
        }
    }

    for node in &missing_nodes {
        graph.insert(*node, Vec::new());
    }

    graph
}

fn find_order(in_graph: &HashMap<char, Vec<char>>) -> String {
    let mut graph = in_graph.clone();
    let mut order: String = String::new();

    while graph.len() > 0 {
        // find first (sorted)
        let mut empty_lists = find_empty(&graph);
        println!("{:?}", empty_lists);
        empty_lists.sort();
        let last_added = empty_lists[0];

        // add it to order
        order.push(last_added);

        // Remove it from graph
        graph.remove(&last_added);

        for (_, dependensies) in graph.iter_mut() {
            if dependensies.contains(&last_added) {
                dependensies.retain(|&n| n != last_added);
            }
        }
    }

    order
}

fn find_empty(graph: &HashMap<char, Vec<char>>) -> Vec<char> {
    let mut empty_lists: Vec<char> = Vec::new();

    for (node, dependensies) in graph {
        if dependensies.len() == 0 {
            empty_lists.push(*node);
        }
    }

    empty_lists
}

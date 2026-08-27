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

    let order = find_order(&graph);

    let seconds_lapsed = find_time_with_five_workers(&graph);

    println!("Part 1: {}", order);
    println!("Part 2: {}", seconds_lapsed);

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
        empty_lists.sort();
        let last_added = empty_lists[0];

        // add it to order
        order.push(last_added);

        // Remove it from graph
        graph.remove(&last_added);

        for (_, dependensies) in graph.iter_mut() {
            if let Some(index) = dependensies.iter().position(|&x| x == last_added) {
                dependensies.swap_remove(index);
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

fn find_time_with_five_workers(in_graph: &HashMap<char, Vec<char>>) -> usize {
    let mut graph = in_graph.clone();

    let mut workers = vec![
        (0, None::<char>),
        (0, None::<char>),
        (0, None::<char>),
        (0, None::<char>),
        (0, None::<char>),
    ];

    let mut total_time = 0;
    // There's more work to be done or are workers working or
    while graph.len() > 0 || workers.iter().any(|(sec, _)| *sec > 0) {
        // let all working workers work
        for (sec, _) in workers.iter_mut() {
            if *sec > 0 {
                *sec -= 1;
            }
        }

        // Find work that is done and remove it from the dependecies
        for (sec, node) in workers.iter_mut() {
            if *sec == 0 && node.is_some() {
                let just_done = node.unwrap();

                for (_, dependensies) in graph.iter_mut() {
                    if let Some(index) = dependensies.iter().position(|&x| x == just_done) {
                        dependensies.swap_remove(index);
                    }
                }
                // Free worker
                *node = None;
            }
        }

        // Find new work
        let mut empty_lists = find_empty(&graph);
        empty_lists.sort();

        // Assign new work to workers
        while empty_lists.len() > 0 && workers.iter().any(|(_, node)| node.is_none()) {
            let label = empty_lists[0];

            for (sec, node) in workers.iter_mut() {
                if node.is_none() {
                    // Assign work
                    *node = Some(label);
                    *sec = 60 + (label as u8) - 64; // 65 is the value of 'A' so using 64 to make it 1

                    // Remove work from graph
                    graph.remove(&label);

                    // work is assigned, avoid new assignments
                    break;
                }
            }

            empty_lists.swap_remove(0);
        }

        total_time += 1;
    }

    total_time - 1 // remove last lap before returning
}

/* NOTES
    For del 2 trenger vi en loop for work som ticker pr sec. Vi må ha en oversikt over arbeidere.
    Kan være en array på 5 med antall sekunder igjen for arbeidet og label for node.

    loop pr sec:
        Hent alle tomme lister.
            Hvis null
                continue
            else
                Sorter liste over noder
                For hver node:
                    Ledig arbeider?
                        assign
                        remove node from graph
        reduser alle ikke 0 arbeidre
        hvis arbeider har node og er null:
            fjern node fra dependensies.

    Del 2 ble implementer i en litt annen rekkefølge.
*/

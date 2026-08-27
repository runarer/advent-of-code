use std::io;

struct Node {
    nodes: Vec<Node>,
    metadata: Vec<usize>,
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    // parse input to an array of ints
    let input: Vec<usize> = content
        .trim()
        .split(' ')
        .map(|c| c.parse::<usize>().expect("Not a valid number"))
        .collect();

    let (root, _) = create_node(&input, 0);

    let metadata_sum = sum_metadata(&root);

    println!("Part 1: {}", metadata_sum);

    let sum_values = sum_value_of_node(&root);

    println!("Part 2: {}", sum_values);

    Ok(())
}

fn create_node(numbers: &Vec<usize>, start: usize) -> (Node, usize) {
    let node_fields = numbers[start];
    let metadata_fields = numbers[start + 1];

    let mut node = Node {
        nodes: Vec::with_capacity(node_fields),
        metadata: Vec::with_capacity(metadata_fields),
    };

    // Read and create subnodes
    let mut offset = start + 2;
    if node_fields > 0 {
        for _ in 0..node_fields {
            let (subnode, end) = create_node(numbers, offset);
            offset = end;
            node.nodes.push(subnode);
        }
    }

    // Read metadata
    if metadata_fields > 0 {
        for data_index in 0..metadata_fields {
            node.metadata.push(numbers[offset + data_index]);
        }
        offset += metadata_fields;
    }

    (node, offset)
}

fn sum_metadata(root: &Node) -> usize {
    let mut sum = root.metadata.iter().sum();

    for subnode in root.nodes.iter() {
        sum += sum_metadata(subnode);
    }

    sum
}

fn sum_value_of_node(root: &Node) -> usize {
    if root.nodes.len() == 0 {
        return root.metadata.iter().sum();
    }

    let mut sum = 0;

    for subnode_ref in &root.metadata {
        if *subnode_ref == 0 {
            continue;
        }
        // does it not exist
        if *subnode_ref > root.nodes.len() {
            continue;
        }
        sum += sum_value_of_node(&root.nodes[subnode_ref - 1]);
    }

    sum
}

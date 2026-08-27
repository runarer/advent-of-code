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

    // println!("{:?}", input);
    let (root, _) = create_node(&input, 0);

    println!("{:?}", root.metadata);

    Ok(())
}

fn create_node(numbers: &Vec<usize>, start: usize) -> (Node, usize) {
    let node_fields = numbers[start];
    let metadata_fields = numbers[start + 1];
    println!("{},{},{}", start, node_fields, metadata_fields);

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
            // node.nodes[subnode_index] = subnode;
            node.nodes.push(subnode);
        }
    }

    // Read metadata
    if metadata_fields > 0 {
        for data_index in 0..metadata_fields {
            // node.metadata[data_index] = numbers[offset + data_index];
            node.metadata.push(numbers[offset + data_index]);
        }
        offset += metadata_fields;
    }

    (node, offset)
}

use std::{collections::HashMap, io};

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let cleaned_polymer = clean_polymer(&content);

    println!("Part 1: {}", cleaned_polymer.len());
    println!("Part 2: {}", find_shortest_polymer(content));

    Ok(())
}

fn match_type_and_polarity(a: char, b: char) -> bool {
    if a.to_ascii_lowercase() != b.to_ascii_lowercase() || a == b {
        return false;
    }
    true
}

// Worked on first try, no AI,
fn clean_polymer(polymer_as_string: &str) -> String {
    let polymer: Vec<char> = polymer_as_string.chars().collect();
    let mut removed: Vec<bool> = vec![false; polymer.len()];

    // we keep a pointer to the two chars we want to compare.
    // if they are removed we update pointers by looking at removed
    // chars.
    let mut back = 0;
    let mut front = 1;
    while front < polymer.len() {
        if match_type_and_polarity(polymer[back], polymer[front]) {
            removed[back] = true;
            removed[front] = true;
            while front < polymer.len() && removed[front] {
                front += 1;
            }
            // find the first char behind removed
            while back > 0 && removed[back] {
                back -= 1;
            }
            // if we are at the beginning and all is removed jump to the front.
            if back == 0 && removed[back] {
                back = front;
                front += 1;
            }
        } else {
            while front < polymer.len() && removed[front] {
                front += 1;
            }
            back = front;
            front += 1;
        }
    }

    // Combine the polymer and removed, then filter out removed and end line chars.
    // Pick the char and create a string.
    polymer
        .iter()
        .zip(removed)
        .filter(|(p, r)| !r && p.is_alphabetic())
        .map(|(p, _)| p)
        .collect()
}

// we make a hashmap for each char in the polymer and insert length of
// reduced and cleaned polymer.
fn find_shortest_polymer(polymer: String) -> usize {
    let mut produced_by_removing: HashMap<char, usize> = HashMap::new();

    for to_remove in polymer.chars() {
        let to_remove = to_remove.to_ascii_lowercase();

        if produced_by_removing.contains_key(&to_remove) {
            continue;
        }

        // filter out char, both lower and uppercase
        let reduced_polymer: String = polymer
            .chars()
            .filter(|c| c.to_ascii_lowercase() != to_remove)
            .collect();

        let cleaned_polymer = clean_polymer(&reduced_polymer);

        produced_by_removing.insert(to_remove, cleaned_polymer.len());
    }

    *produced_by_removing.values().min().unwrap()
}

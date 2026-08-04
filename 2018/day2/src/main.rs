use std::io;

fn contains_n(s: &str, n: usize) -> bool {
    for c in s.chars() {
        if s.matches(c).count() == n {
            return true;
        }
    }
    false
}

fn differe_by_one(s1: &str, s2: &str) -> bool {
    let mut diff_found: bool = false;

    let s1_chars = s1.chars();
    let s2_chars = s2.chars();

    for (c1, c2) in s1_chars.zip(s2_chars) {
        if c1 != c2 {
            if diff_found {
                return false;
            }
            diff_found = true;
        }
    }
    true
}

fn remove_diff(s1: &str, s2: &str) -> String {
    let s1_chars = s1.chars();
    let s2_chars = s2.chars();

    let mut index = 0;
    for (i, (c1, c2)) in s1_chars.zip(s2_chars).enumerate() {
        if c1 != c2 {
            index = i;
            break;
        }
    }

    let result = s1
        .chars()
        .enumerate()
        .filter(|(i, _)| *i != index)
        .map(|(_, c)| c)
        .collect();
    result
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let mut sum = content
        .lines()
        .map(|line| contains_n(line, 2))
        .filter(|&b| b)
        .count();

    sum *= content
        .lines()
        .map(|line| contains_n(line, 3))
        .filter(|&b| b)
        .count();

    println!("Part 1: {}", sum);

    for line in content.lines() {
        for other_line in content.lines() {
            if line == other_line {
                continue;
            }

            if differe_by_one(line, other_line) {
                let result = remove_diff(line, other_line);
                println!("Part 2: {}", result);
                return Ok(());
            }
        }
    }

    Ok(())
}

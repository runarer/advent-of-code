use std::collections::HashSet;
use std::fs;
use std::io::{self, Error, ErrorKind};

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1])?;

    let mut sum = 0;

    let numbers: Vec<i32> = content
        .lines()
        .map(|line| line.parse::<i32>()) // This result in Ok(i32) or Err(ParseIntError)
        .collect::<Result<Vec<_>, _>>() // Compbines into a Result<Vec<i32>, ParseIntError>
        .map_err(|e| Error::new(ErrorKind::InvalidData, e))?;

    // Part 1
    for n in &numbers {
        sum += n;
    }

    println!("Part 1: {}", sum);

    // Part 2
    let mut frequencies = HashSet::new();
    let mut current_frequency = 0;
    let mut index = 0;
    while !frequencies.contains(&current_frequency) {
        frequencies.insert(current_frequency);
        current_frequency = current_frequency + numbers[index % numbers.len()];
        index += 1;
    }

    println!("Part 2: {}", current_frequency);

    Ok(())
}

use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let steps: Vec<(char, char)> = content.lines().map(|line| parse_step(line)).collect();

    for step in steps {
        println!("({},{})", step.0, step.1);
    }

    Ok(())
}

fn parse_step(line: &str) -> (char, char) {
    let point = line.chars().nth(5).unwrap_or('0');
    let depend_on = line.chars().nth(36).unwrap_or('0');
    return (point, depend_on);
}

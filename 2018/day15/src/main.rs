use std::io;

struct Cave {
    height: usize,
    width: usize,
    map: Vec<char>,
}

impl Cave {
    fn new(content: &str) -> Self {
        let lines: Vec<&str> = content.lines().collect();

        Cave {
            height: lines.len(),
            width: lines.first().unwrap().len(),
            map: lines.iter().flat_map(|line| line.trim().chars()).collect(),
        }
    }
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;
    let cave = Cave::new(&content);

    for row in 0..cave.height {
        for col in 0..cave.width {
            print!("{}", cave.map[col + row * cave.width]);
        }
        println!();
    }

    Ok(())
}

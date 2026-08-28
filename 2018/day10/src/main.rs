use regex::Regex;
use std::io;

struct Light {
    position: (i32, i32),
    velocity: (i32, i32),
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;
    let lights = parse_lines(content);

    Ok(())
}

fn parse_lines(content: String) -> Vec<Light> {
    let re = Regex::new(r"").unwrap();

    let lights: Vec<Light> = content
        .lines()
        .map(|line| {
            let capture = re.captures(line).unwrap();
            let xpos = capture[1].parse::<i32>().unwrap();
            let ypos = capture[2].parse::<i32>().unwrap();
            let xvel = capture[3].parse::<i32>().unwrap();
            let yvel = capture[4].parse::<i32>().unwrap();

            Light {
                position: (xpos, ypos),
                velocity: (xvel, yvel),
            }
        })
        .collect();
    lights
}

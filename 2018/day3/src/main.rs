use regex::Regex;
use std::io;

fn overlapping_cells(squares: &Vec<(usize, usize, usize, usize, usize)>) -> Vec<Vec<usize>> {
    let mut fabric = vec![vec![0; 1000]; 1000]; // Må være vec for å ikke få stack overflow!

    // * derefererer verdiene, pga &squares.
    for (_, x, y, width, height) in squares {
        for i in *x..(*x + *width) {
            for j in *y..(*y + *height) {
                fabric[i][j] += 1;
            }
        }
    }

    fabric
}

fn sum_overlapping_cells(fabric: &Vec<Vec<usize>>) -> usize {
    let mut sum = 0;
    for row in fabric {
        for &cell in row {
            if cell > 1 {
                sum += 1;
            }
        }
    }
    sum
}

fn non_overlapping_square(
    fabric: &Vec<Vec<usize>>,
    squares: &Vec<(usize, usize, usize, usize, usize)>,
) -> Result<usize, &'static str> {
    'top: for (id, x, y, width, height) in squares {
        for i in *x..(*x + *width) {
            for j in *y..(*y + *height) {
                if fabric[i][j] > 1 {
                    // fant overlap, sjekk neste kvadrat
                    continue 'top;
                }
            }
        }
        return Ok(*id);
    }

    Err("no non-overlapping claim found")
}

fn main() -> io::Result<()> {
    let re = Regex::new(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();

    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let squares = content
        .lines()
        .map(|line| {
            let caps = re.captures(line).unwrap();
            let id = caps[1].parse::<usize>().unwrap();
            let x = caps[2].parse::<usize>().unwrap();
            let y = caps[3].parse::<usize>().unwrap();
            let width = caps[4].parse::<usize>().unwrap();
            let height = caps[5].parse::<usize>().unwrap();
            (id, x, y, width, height)
        })
        .collect::<Vec<_>>();

    let fabric = overlapping_cells(&squares);

    let sum = sum_overlapping_cells(&fabric);
    println!("Part 1: {}", sum);

    match non_overlapping_square(&fabric, &squares) {
        Ok(id) => println!("Part 2: {}", id),
        Err(e) => eprintln!("Part 2 error: {}", e),
    }

    Ok(())
}

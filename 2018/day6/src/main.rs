use std::collections::VecDeque;
use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let points: Vec<(i32, i32)> = content
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| parse_coordinates(line.trim()))
        .collect();

    println!("lenght points: {}", points.len());

    let locked_points: Vec<(i32, i32)> = points
        .iter()
        .filter(|point| locked(point, &points))
        .map(|point| *point)
        .collect();
    println!("lenght locked points: {}", locked_points.len());

    for point in locked_points {
        println!("({},{})", point.0, point.1)
    }

    Ok(())
}

fn parse_coordinates(line: &str) -> (i32, i32) {
    if let Some((x, y)) = line.split_once(',') {
        let x = x.trim().parse::<i32>().unwrap();
        let y = y.trim().parse::<i32>().unwrap();

        return (x, y);
    }

    (0, 0)
}

fn distance((x1, y1): (i32, i32), (x2, y2): (i32, i32)) -> i32 {
    (x1 - x2).abs() + (y1 - y2).abs()
}

fn locked(point: &(i32, i32), points: &Vec<(i32, i32)>) -> bool {
    let north_point = (point.0, point.1 - 1);
    let east_point = (point.0 + 1, point.1);
    let south_point = (point.0, point.1 + 1);
    let west_point = (point.0 - 1, point.1);

    let mut north_locked = false;
    let mut east_locked = false;
    let mut south_locked = false;
    let mut west_locked = false;

    for &other_point in points {
        if other_point == *point {
            continue;
        }

        // check for each of the four points around if we get closer to other_point
        // moving in that direction
        let distant_points = distance(*point, other_point);
        if distant_points > distance(north_point, other_point) {
            north_locked = true;
        }
        if distant_points > distance(east_point, other_point) {
            east_locked = true;
        }
        if distant_points > distance(south_point, other_point) {
            south_locked = true;
        }
        if distant_points > distance(west_point, other_point) {
            west_locked = true;
        }

        if north_locked && east_locked && south_locked && west_locked {
            return true;
        }
    }

    false
}

fn calcualte_area(point: (i32, i32), points: &Vec<(i32, i32)>) -> usize {
    let mut queue: VecDeque<(i32, i32)> = VecDeque::new();
    let mut visited: Vec<(i32, i32)> = Vec::new();

    queue.push_back(point);

    while queue.len() > 0 {
        let current_point = queue.pop_front().expect("Queue was empty after check!");
        visited.push(current_point);
        let neighbors = get_neighbors(current_point);

        for neighbor in neighbors {
            if visited.contains(&neighbor) || queue.contains(&neighbor) {
                continue;
            }
            queue.push_back(neighbor);
        }
    }

    0
}

fn get_neighbors((x, y): (i32, i32)) -> [(i32, i32); 4] {
    [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
}

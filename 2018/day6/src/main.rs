use std::collections::VecDeque;
use std::io;

/*
    Der avstanden mellom to punkter er lik så får man to eller tre linjer.
    Disse linjene vil skape et "bilde" delt opp i deler. Den største ikke evige
    delen er det vi er ute etter.

    Må beregne og representer disse linjene, noen vil være evige i en retning.
    Krysspunkter deler opp i nye linjer.

    Tenk to punkter der x1 != x2, y1 != y2 og punktene er ikke 45 grader ovenfor
    hverandre. Dette gir tre linjer.
     - En linje mellom to "nye" punkter
     - En linje fra hvert nytt punkt og ut i evigheten fra dette punktet.

    Spesielle tilfeller, skjekk om disse eksistere så vi kan unngå å håndtere dem
    hvis ikke.
     - Hvis x1 == x2 eller x1 == y2 så får vi en linje, evig i begge retninger.
     - 45 grader ovenfor hverandre vil gi 5 linjer og 2 områder hvor avstanden er lik.
*/
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

    // println!("lenght points: {}", points.len());

    let locked_points: Vec<(i32, i32)> = points
        .iter()
        .filter(|point| locked(point, &points))
        .map(|point| *point)
        .collect();
    println!("lenght locked points: {}", locked_points.len());

    for point in &locked_points {
        println!("({},{})", point.0, point.1)
    }

    let largest_area = locked_points
        .iter()
        .map(|point| calcualte_area(point, &points))
        .max()
        .expect("No largest area was found");

    println!("Part 1: {}", largest_area);

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

fn calcualte_area(point: &(i32, i32), points: &Vec<(i32, i32)>) -> usize {
    let mut queue: VecDeque<(i32, i32)> = VecDeque::new();
    let mut visited: Vec<(i32, i32)> = Vec::new();

    queue.push_back(*point);

    while queue.len() > 0 {
        let current_point = queue.pop_front().expect("Queue was empty after check!");
        // println!(
        //     "{},{} - {},{}",
        //     point.0, point.1, current_point.0, current_point.1
        // );
        visited.push(current_point);
        let neighbors = get_neighbors(current_point);

        for neighbor in neighbors {
            if visited.contains(&neighbor) || queue.contains(&neighbor) {
                continue;
            }
            // This need to be the shortest
            let dist_from_point = distance(neighbor, *point);
            let mut tie_or_higher = false;
            // check the other points
            for other_points in points {
                // Skip point
                if *other_points == *point {
                    continue;
                }
                let dist_other_point = distance(neighbor, *other_points);

                if dist_other_point <= dist_from_point {
                    tie_or_higher = true;
                    break;
                }
            }

            if !tie_or_higher {
                queue.push_back(neighbor);
            }
        }
    }

    visited.len()
}

fn get_neighbors((x, y): (i32, i32)) -> [(i32, i32); 4] {
    [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
}

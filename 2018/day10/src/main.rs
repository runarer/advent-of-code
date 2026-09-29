/* For hver runde, etter alle er flyttet, så for alle; sjekk naboer om de eksisterer, gi poeng for hver nabo,
   høy poengsum indikerer at noe foregår.
*/

/* Optimaliseringsmuligheter
    Kan lage et slags hash, en array på lengde med antall lys og for hver runde nullstilles
    den og for hvert lys så tar man lys_x_pos[x % antall_lys]++, når vi får en "stor" verdi i
    en array pos så har vi muligens en bokstav. Kan være at vi trenger en "stor" verdi i flere.
    Denne fungerte ikke spesielt bra.

    Når vi regner ut lysenes bevegelser så kan vi også regne ut max og min for x og y. Dette
    gir oss mulighet til å kun sjekke for nærhet av lys når mange er nærme hverandre, altså når
    differansen på min og max ikke er for stor.
*/
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
    let mut lights = parse_lines(content);

    let mut seconds = 0;

    loop {
        seconds += 1;
        let mut points = 0;
        let mut min_x = i32::MAX;
        let mut max_x = i32::MIN;
        let mut min_y = i32::MAX;
        let mut max_y = i32::MIN;

        for light in lights.iter_mut() {
            light.position.0 += light.velocity.0;
            light.position.1 += light.velocity.1;

            // Kan ta vare på max og min verdier
            if light.position.0 > max_x {
                max_x = light.position.0;
            }
            if light.position.0 < min_x {
                min_x = light.position.0;
            }
            if light.position.1 > max_y {
                max_y = light.position.1;
            }
            if light.position.1 < min_y {
                min_y = light.position.1;
            }
        }

        // kun sjekke dette når max og min er "nærme hverandre"
        let diff_x = max_x - min_x;
        let diff_y = max_y - min_y;

        if diff_x < 100 && diff_y < 11 {
            for light in &lights {
                for (neighbor_x, neighbor_y) in [
                    (light.position.0, light.position.1 + 1), // north
                    (light.position.0 + 1, light.position.1), // east
                    (light.position.0, light.position.1 - 1), // south
                    (light.position.0 - 1, light.position.1), // west
                ] {
                    if contains(neighbor_x, neighbor_y, &lights) {
                        points += 1;
                    }
                }
            }
        }

        if points > 400 {
            break;
        }
    }

    println!("Part 1:");
    print_sky(&lights);
    println!("Part 2:  {seconds}");

    Ok(())
}

fn parse_lines(content: String) -> Vec<Light> {
    let re =
        Regex::new(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>").unwrap();

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

fn contains(x: i32, y: i32, lights: &Vec<Light>) -> bool {
    for light in lights {
        if light.position.0 == x && light.position.1 == y {
            return true;
        }
    }
    false
}

fn print_sky(lights: &Vec<Light>) {
    let max_x = lights.iter().fold(i32::MIN, |acc, light| {
        if acc < light.position.0 {
            return light.position.0;
        }
        acc
    });
    let min_x = lights.iter().fold(i32::MAX, |acc, light| {
        if acc > light.position.0 {
            return light.position.0;
        }
        acc
    });
    let max_y = lights.iter().fold(i32::MIN, |acc, light| {
        if acc < light.position.1 {
            return light.position.1;
        }
        acc
    });
    let min_y = lights.iter().fold(i32::MAX, |acc, light| {
        if acc > light.position.1 {
            return light.position.1;
        }
        acc
    });
    let width = max_x - min_x + 1;
    let height = max_y - min_y + 1;

    for i in (0..height).rev() {
        for j in (0..width).rev() {
            if contains(max_x - j, max_y - i, &lights) {
                print!("#");
            } else {
                print!(".");
            }
        }
        println!();
    }
}

use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    // Henter ut initial states.
    let initial_states = content
        .lines()
        .next()
        .expect("Didn't get first line")
        .split(':')
        .skip(1)
        .next()
        .expect("First line not parsed correctly")
        .trim();

    // Fyller ut regelsettet.
    let rules = content
        .lines()
        .skip(2)
        .map(|line| line.split_once("=>").expect("Rule not parsed correctly"))
        .fold([false; 32], |mut acc, (pattern, result)| {
            // Patterns er # eller . og kan representeres som en 5-bit integer.
            let mut index = 0;
            if result.trim() == "#" {
                for (i, c) in pattern.trim().chars().enumerate() {
                    if c == '#' {
                        index |= 1 << (4 - i);
                    }
                }
                acc[index] = true;
            }
            acc
        });

    let pots = initial_states.chars().map(|c| c == '#').collect::<Vec<_>>();

    let generations = 20;
    let sum = grow_plants(&pots, &rules, generations);
    println!("Part 1: {}", sum);

    Ok(())
}

fn add_pots(pots: &mut Vec<bool>, first_pot_index: &mut isize) {
    let leading_dots = pots.iter().take_while(|&&x| !x).count();
    if leading_dots < 4 {
        pots.splice(..0, std::iter::repeat(false).take(4 - leading_dots));
        *first_pot_index -= 4 - leading_dots as isize;
    }

    let trailing_dots = pots.iter().rev().take_while(|&&x| !x).count();
    if trailing_dots < 4 {
        pots.splice(
            pots.len()..,
            std::iter::repeat(false).take(4 - trailing_dots),
        );
    }
}

// fn print_pots(pots: &Vec<bool>) {
//     for pot in pots {
//         print!("{}", if *pot { '#' } else { '.' });
//     }
//     println!();
// }

fn grow_plants(initial_pots: &Vec<bool>, rules: &[bool; 32], generations: usize) -> isize {
    let mut pots = initial_pots.clone();
    let mut first_pot_index = 0;

    for _ in 0..generations {
        add_pots(&mut pots, &mut first_pot_index);
        let mut new_pots = vec![false; pots.len()];

        for pot in 2..pots.len() - 2 {
            let mut rule_index = 0;
            for j in 0..5 {
                if pots[pot + j - 2] {
                    rule_index |= 1 << (4 - j);
                }
            }

            if rules[rule_index] {
                new_pots[pot] = true;
            }
        }

        pots = new_pots;
    }

    let mut index = first_pot_index;
    let mut sum = 0;
    for pot in pots {
        if pot {
            sum += index;
        }
        index += 1;
    }
    sum
}

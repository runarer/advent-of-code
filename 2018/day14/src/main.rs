use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;
    let recipies = content.lines().next().unwrap().parse::<usize>().unwrap();

    let next_ten_numbers = next_ten(recipies);
    println!("Part 1: {next_ten_numbers}");

    let recipies_before_number = recipies_before(recipies);
    println!("Part 2: {recipies_before_number}");

    Ok(())
}

fn next_ten(recipies: usize) -> String {
    let mut row: Vec<i8> = Vec::with_capacity(recipies * 2);
    row.push(3);
    row.push(7);

    let mut elf_one = 0;
    let mut elf_two = 1;

    while row.len() < recipies + 10 {
        let new_recipie = row[elf_one] + row[elf_two];

        // add new recipie/s
        if new_recipie >= 10 {
            row.push(1);
            row.push(new_recipie % 10);
        } else {
            row.push(new_recipie);
        }

        // move elfs
        elf_one += 1 + row[elf_one] as usize;
        elf_one %= row.len();
        elf_two += 1 + row[elf_two] as usize;
        elf_two %= row.len();
    }

    return row
        .iter()
        .skip(recipies)
        .take(10)
        .map(|i| i.to_string())
        .collect::<Vec<String>>()
        .concat();
}

fn recipies_before(recipies: usize) -> usize {
    let to_match: Vec<i8> = recipies
        .to_string()
        .chars()
        .map(|c| c.to_string().parse::<i8>().unwrap())
        .collect();
    let mut row: Vec<i8> = Vec::with_capacity(recipies * 2);
    row.push(3);
    row.push(7);

    let mut elf_one = 0;
    let mut elf_two = 1;

    loop {
        let new_recipie = row[elf_one] + row[elf_two];

        // add new recipie/s
        if new_recipie >= 10 {
            row.push(1);
            row.push(new_recipie % 10);
        } else {
            row.push(new_recipie);
        }

        // move elfs
        elf_one += 1 + row[elf_one] as usize;
        elf_one %= row.len();
        elf_two += 1 + row[elf_two] as usize;
        elf_two %= row.len();

        if row.len() > to_match.len() + 1 {
            let mut trailing = 0;

            let match_from = row.len() - to_match.len() - 1;
            let mut got_match = true;
            for i in 0..to_match.len() {
                if row[match_from + i] != to_match[i] {
                    got_match = false;
                    break;
                }
            }
            if !got_match {
                trailing = 1;
                let match_from = row.len() - to_match.len() - 2;
                for i in 0..to_match.len() {
                    if row[match_from + i] != to_match[i] {
                        got_match = false;
                        break;
                    }
                }
            }
            if got_match {
                return row.len() - to_match.len() - trailing - 1; // subtrack the number and trailing number if one
            }
        }
    }
}

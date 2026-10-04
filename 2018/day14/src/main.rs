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
    // let next_ten_numbers = next_ten(9);
    println!("Part 1: {next_ten_numbers}");
    // let next_ten_numbers = next_ten(5);
    // println!("Part 1: {next_ten_numbers}");

    // let next_ten_numbers = next_ten(18);
    // println!("Part 1: {next_ten_numbers}");

    // let next_ten_numbers = next_ten(2018);
    // println!("Part 1: {next_ten_numbers}");

    Ok(())
}

fn next_ten(recipies: usize) -> String {
    let mut row: Vec<i8> = Vec::with_capacity(recipies * 2);
    row.push(3);
    row.push(7);

    let mut elf_one = 0;
    let mut elf_two = 1;

    while row.len() < recipies + 10 {
        // println!("{:?}", row);
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

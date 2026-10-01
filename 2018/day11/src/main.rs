use std::{cmp, io};

const GRID_SIZE: usize = 300;

// Since the assignment uses coordination starting at 1 I have use those in the code.
// This leads to a lot of -1.
struct FuelCellGrid {
    grid: Vec<i32>,
}

impl FuelCellGrid {
    fn new(serial_number: usize) -> Self {
        let mut grid = vec![0; GRID_SIZE * GRID_SIZE];

        for x in 1..=GRID_SIZE {
            for y in 1..=GRID_SIZE {
                let rack_id = x as i64 + 10;
                let mut power_level = rack_id * y as i64;
                power_level += serial_number as i64;
                power_level *= rack_id;
                // Keep only the hundreds digit
                power_level %= 1000;
                power_level /= 100;

                power_level -= 5;

                grid[(y - 1) * GRID_SIZE + (x - 1)] = power_level as i32;
            }
        }

        Self { grid }
    }

    pub fn square_value(&self, x: usize, y: usize, size: usize) -> i32 {
        let mut sum = 0;
        for i in (x - 1)..(x + size - 1) {
            for j in (y - 1)..(y + size - 1) {
                sum += self.grid[j * GRID_SIZE + i];
            }
        }
        sum
    }
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;
    let grid_serial_number = content.lines().next().unwrap().parse::<usize>().unwrap();

    let fuel_cell_grid = FuelCellGrid::new(grid_serial_number);

    let mut max = i32::MIN;
    let mut max_x = 0;
    let mut max_y = 0;
    let size = 3;
    for x in 1..=(GRID_SIZE - size + 1) {
        for y in 1..=(GRID_SIZE - size + 1) {
            let value = fuel_cell_grid.square_value(x, y, size);
            if max < value {
                max = value;
                max_x = x;
                max_y = y;
            }
        }
    }
    println!("Part 1: {max_x},{max_y}");

    // Denne løsninger en treg, tar rundt 10sec.

    let mut min_square_size = 1;
    let mut max = i32::MIN;
    let mut max_x = 0;
    let mut max_y = 0;
    let mut max_size = 0;
    // Vi kan avslutte søket hvis hva som gjenstår ikke er stort nok til å inneholde
    // en større verdi en hva som er funnet.
    for x in 1..(GRID_SIZE - min_square_size + 1) {
        for y in 1..(GRID_SIZE - min_square_size + 1) {
            let max_grid_size = GRID_SIZE - cmp::max(x, y) + 1;
            let mut sum = fuel_cell_grid.square_value(x, y, min_square_size); // denne kan endres til å legge til nye celler

            for size in min_square_size..=max_grid_size {
                // hvis summen et større enn et lite kvadrat kan maksimalt inneholde
                // trenger vi ikke lenger sjekke kvadrat av denne størrelsen.
                if sum > max {
                    max = sum;
                    max_x = x;
                    max_y = y;
                    max_size = size - 1; // it was the last run
                    while sum > (min_square_size * min_square_size) as i32 * 9 {
                        min_square_size += 1;
                    }
                }
                // add the new cells to the sum
                if size > min_square_size {
                    for i in (x - 1)..(x + size - 1) {
                        sum += fuel_cell_grid.grid[(y + size - 2) * GRID_SIZE + i];
                    }
                    for i in (y - 1)..(y + size - 1) {
                        sum += fuel_cell_grid.grid[i * GRID_SIZE + (x + size - 2)];
                    }
                }
            }
        }
    }

    println!("Part 2: {max_x},{max_y},{max_size}");

    Ok(())
}

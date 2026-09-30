use std::io;

const GRID_SIZE: usize = 300;

struct FuelCellGrid {
    grid: Vec<i32>,
}

impl FuelCellGrid {
    fn new(serial_number: usize) -> Self {
        let mut grid = vec![0; GRID_SIZE * GRID_SIZE];

        for x in 1..=GRID_SIZE {
            for y in 1..GRID_SIZE {
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
    for x in 1..=(GRID_SIZE - 2) {
        for y in 1..=(GRID_SIZE - 2) {
            let value = fuel_cell_grid.square_value(x, y, 3);
            if max < value {
                max = value;
                max_x = x;
                max_y = y;
            }
        }
    }
    println!("Part 1: {max_x},{max_y}");

    Ok(())
}

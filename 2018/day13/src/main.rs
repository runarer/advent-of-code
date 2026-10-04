use std::io;

#[derive(Clone)]
struct Cart {
    direction: Direction,
    next_turn: NextTurn,
    position: (usize, usize),
}

impl Cart {
    fn new(direction: Direction, position: (usize, usize)) -> Self {
        Cart {
            direction,
            next_turn: NextTurn::Left,
            position,
        }
    }

    // Se: https://users.rust-lang.org/t/replace-enum-variant-inside-match/95937
    // for noen hint om hva som foregår her.
    // Bruker match for kontrollflyten i funksjonen.
    pub fn move_forward(&mut self) {
        match self.direction {
            Direction::Up => self.position.1 -= 1,
            Direction::Down => self.position.1 += 1,
            Direction::Left => self.position.0 -= 1,
            Direction::Right => self.position.0 += 1,
        }
    }

    pub fn turn(&mut self, track_type: &TrackType) {
        match track_type {
            TrackType::RightCurve => {
                self.direction = match self.direction {
                    Direction::Up => Direction::Right,
                    Direction::Down => Direction::Left,
                    Direction::Left => Direction::Down,
                    Direction::Right => Direction::Up,
                }
            }
            TrackType::LeftCurve => {
                self.direction = match self.direction {
                    Direction::Up => Direction::Left,
                    Direction::Down => Direction::Right,
                    Direction::Left => Direction::Up,
                    Direction::Right => Direction::Down,
                }
            }
            TrackType::Intersection => {
                self.direction = match (&self.direction, &self.next_turn) {
                    (Direction::Up, NextTurn::Left) => Direction::Left,
                    (Direction::Up, NextTurn::Straight) => Direction::Up,
                    (Direction::Up, NextTurn::Right) => Direction::Right,

                    (Direction::Down, NextTurn::Left) => Direction::Right,
                    (Direction::Down, NextTurn::Straight) => Direction::Down,
                    (Direction::Down, NextTurn::Right) => Direction::Left,

                    (Direction::Left, NextTurn::Left) => Direction::Down,
                    (Direction::Left, NextTurn::Straight) => Direction::Left,
                    (Direction::Left, NextTurn::Right) => Direction::Up,

                    (Direction::Right, NextTurn::Left) => Direction::Up,
                    (Direction::Right, NextTurn::Straight) => Direction::Right,
                    (Direction::Right, NextTurn::Right) => Direction::Down,
                }
            }
            TrackType::Empty => {
                println!(
                    "Cart at ({}, {}) is on an empty track!",
                    self.position.0, self.position.1
                );
            }
            TrackType::Straight => {}
        };

        if matches!(track_type, TrackType::Intersection) {
            self.next_turn = match self.next_turn {
                NextTurn::Left => NextTurn::Straight,
                NextTurn::Straight => NextTurn::Right,
                NextTurn::Right => NextTurn::Left,
            };
        }
    }
}

// Need to allow dead code for LastTurn enum since compiler can't see that it is
// used in the turn function for the Cart struct.
#[allow(dead_code)]
#[derive(Clone)]
enum NextTurn {
    Left,
    Straight,
    Right,
}

#[derive(Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Clone)]
enum TrackType {
    // Left and right are based on moving down the track.
    RightCurve,   // /
    LeftCurve,    // \
    Straight,     // - |
    Intersection, // +
    Empty,
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let tracks = content
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| match c {
                    '/' => TrackType::RightCurve,
                    '\\' => TrackType::LeftCurve,
                    '-' | '|' | '<' | '>' | '^' | 'v' => TrackType::Straight,
                    '+' => TrackType::Intersection,
                    ' ' => TrackType::Empty,
                    _ => panic!("Unknown track type: {}", c),
                })
                .collect::<Vec<TrackType>>()
        })
        .collect::<Vec<Vec<TrackType>>>();

    // flat_map er som map, men flater ut iteratorer. Bruk map når det produseres verdier, flat_map når
    // det produseres iteratorer.
    // filter_map er klar, den tar bare med der det ble produsert en verdi.
    // move må jeg se mer på.
    let carts = content
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.chars().enumerate().filter_map(move |(x, c)| match c {
                '^' => Some(Cart::new(Direction::Up, (x, y))),
                'v' => Some(Cart::new(Direction::Down, (x, y))),
                '<' => Some(Cart::new(Direction::Left, (x, y))),
                '>' => Some(Cart::new(Direction::Right, (x, y))),
                _ => None,
            })
        })
        .collect::<Vec<Cart>>();

    let first_crash_position = run_untill_first_crash(&tracks, &carts);
    println!(
        "Part 1: {},{}",
        first_crash_position.0, first_crash_position.1
    );

    let last_cart = run_untill_last_cart(&tracks, &carts);
    println!("Part 2: {},{}", last_cart.0, last_cart.1);

    // print_tracks(&tracks);
    // println!();
    // print_carts(&carts);

    Ok(())
}

fn run_untill_first_crash(tracks: &Vec<Vec<TrackType>>, carts: &Vec<Cart>) -> (usize, usize) {
    let mut carts = carts.clone();
    loop {
        // println!("-------------------------------");
        carts.sort_by_key(|item| (item.position.1, item.position.0));
        // print_carts(&carts);
        for i in 0..carts.len() {
            let cart = &mut carts[i];
            cart.move_forward();
            let track_type = &tracks[cart.position.1][cart.position.0];
            cart.turn(track_type);

            // Check for collisions
            for j in 0..carts.len() {
                if i != j && carts[i].position == carts[j].position {
                    return carts[i].position;
                }
            }
        }
    }
}

fn run_untill_last_cart(tracks: &Vec<Vec<TrackType>>, carts: &Vec<Cart>) -> (usize, usize) {
    let mut carts: Vec<(Cart, bool)> = carts.iter().map(|cart| (cart.clone(), false)).collect();
    loop {
        // create move order
        carts.sort_by_key(|item| (item.0.position.1, item.0.position.0));
        // reset moves
        carts.iter_mut().for_each(|cart| cart.1 = false);

        // Move carts
        let mut i: isize = 0;
        loop {
            // Are all moved?
            if carts.iter().all(|cart| cart.1) {
                break;
            }

            // current cart and if it has moved
            let cart = &mut carts[i as usize];
            if cart.1 {
                i += 1;
                continue;
            }

            // Move cart
            cart.0.move_forward();
            let track_type = &tracks[cart.0.position.1][cart.0.position.0];
            cart.0.turn(track_type);
            cart.1 = true;

            // check for collitions, remove both and reset i.
            let mut j: isize = 0;
            while j < carts.len() as isize {
                if i != j && carts[i as usize].0.position == carts[j as usize].0.position {
                    carts.remove(j.max(i) as usize);
                    carts.remove(i.min(j) as usize);
                    i = 0;
                    break;
                }
                j += 1;
            }
        }

        // Are we done? One cart left.
        if carts.len() == 1 {
            return carts[0].0.position;
        }
    }
}

// fn print_tracks(tracks: &Vec<Vec<TrackType>>) {
//     for row in tracks {
//         for track in row {
//             let c = match track {
//                 TrackType::RightCurve => 'R',
//                 TrackType::LeftCurve => 'L',
//                 TrackType::Straight => 'S',
//                 TrackType::Intersection => 'I',
//                 TrackType::Empty => ' ',
//             };
//             print!("{}", c);
//         }
//         println!();
//     }
// }

// fn print_carts(carts: &Vec<Cart>) {
//     for cart in carts {
//         let direction = match cart.direction {
//             Direction::Up => "Up",
//             Direction::Down => "Down",
//             Direction::Left => "Left",
//             Direction::Right => "Right",
//         };

//         println!(
//             "Cart at ({}, {}) with direction {}",
//             cart.position.0, cart.position.1, direction
//         );
//     }
//     println!();
// }

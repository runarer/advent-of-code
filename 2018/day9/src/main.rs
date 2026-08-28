use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    // Parse input
    let content_parts: Vec<&str> = content.split(' ').collect();

    let players = content_parts[0]
        .parse::<usize>()
        .expect("Players not usize");
    let last_marble_points = content_parts[6]
        .parse::<usize>()
        .expect("Last marble not usize");

    let highest_score = play_game(players, last_marble_points);
    println!("Part 1: {}", highest_score);

    let highest_score_big_game = play_big_game(players, last_marble_points * 100);
    println!("Part 2: {}", highest_score_big_game);

    Ok(())
}

/*  Players kan representeres med en vec<usize> hvor index er player nummer, sett alle til 0.
    Sirkelen kan representeres med en vec<usize>. Sett av plass
*/
/* The Naive solution, works fine for part 1 */
fn play_game(players: usize, last_marble_points: usize) -> usize {
    let mut players = vec![0; players];
    let mut circle: Vec<usize> = Vec::with_capacity(last_marble_points);

    // game start
    circle.push(0);
    let mut current_marble: usize = 0;
    let mut current_index: usize = 0;
    let mut current_player: usize = 0;

    while current_marble < last_marble_points {
        current_marble += 1;
        current_player = (current_player + 1) % players.len();

        if (current_marble % 23) == 0 {
            players[current_player] += current_marble;
            let new_index = (current_index as i32 - 7).rem_euclid(circle.len() as i32);
            current_index = new_index as usize;
            players[current_player] += circle.remove(current_index);
            current_index %= circle.len(); // if we removed the last item.
        } else {
            // find insert position
            current_index = (current_index + 2) % circle.len();
            circle.insert(current_index, current_marble);
        }
    }

    *players.iter().max().unwrap()
}

/* The fast solution, needed for part 2 */
struct Node<T> {
    element: T,
    next: usize,
    prev: usize,
}

fn play_big_game(players: usize, last_marble_points: usize) -> usize {
    let mut players = vec![0; players];
    let mut circle: Vec<Node<usize>> = Vec::with_capacity(last_marble_points);
    let mut current_node = 0;
    circle.push(Node {
        element: 0,
        next: 0,
        prev: 0,
    });

    let mut current_marble = 0;
    let mut current_player = 0;
    while current_marble < last_marble_points {
        // print_circle(&circle, circle[current_node].element, current_player);

        current_marble += 1;
        current_player = (current_player + 1) % players.len();

        if (current_marble % 23) == 0 {
            players[current_player] += current_marble;

            // we remove by unlisting
            // first move back 7 times
            for _ in 0..7 {
                current_node = circle[current_node].prev;
            }

            // get marble
            players[current_player] += circle[current_node].element;

            // "remove" marble
            let before_node = circle[current_node].prev;
            let after_node = circle[current_node].next;

            circle[after_node].prev = before_node;
            circle[before_node].next = after_node;

            current_node = after_node;
        } else {
            let before_node = circle[current_node].next;
            let after_node = circle[before_node].next;
            let new_index = circle.len();

            // Update existing nodes
            circle[before_node].next = new_index;
            circle[after_node].prev = new_index;

            // insert node
            circle.push(Node {
                element: current_marble,
                next: after_node,
                prev: before_node,
            });
            current_node = circle.len() - 1;
        }
    }

    *players.iter().max().unwrap()
}

// fn print_circle(circle: &Vec<Node<usize>>, current_element: usize, player: usize) {
//     let mut current_node = 0;

//     print!("[{}] [ ", player);
//     for _ in 0..circle.len() {
//         if circle[current_node].element == current_element {
//             print!("({}) ", circle[current_node].element);
//         } else {
//             print!("{} ", circle[current_node].element);
//         }
//         current_node = circle[current_node].next;
//         if circle[current_node].element == 0 {
//             break;
//         }
//     }
//     println!("] {}", circle.len());
// }

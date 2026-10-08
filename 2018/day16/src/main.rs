use std::io;

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let mut lines = content.lines();

    loop {
        let before_line = lines.next();
        if before_line == None {
            break;
        }
        let before_line = before_line.unwrap();
        let number_lien = lines.next().expect("Number line not found");
        let after_line = lines.next().expect("after line not found");
        _ = lines.next().expect("empty line missing");
    }

    Ok(())
}

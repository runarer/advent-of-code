use regex::Regex;
use std::io;

enum EventKind {
    BeginShift(usize),
    FallAsleep,
    WakeUp,
}
struct Event {
    year: usize,
    month: usize,
    day: usize,
    hour: usize,
    minute: usize,
    event_kind: EventKind,
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    let re = Regex::new(r"\[(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)\] ((?:Guard #(\d+) begins shift)|(?:falls asleep)|(?:wakes up))").unwrap();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let log = content
        .lines()
        .map(|line| {
            let capture = re.captures(line).unwrap();
            let year = capture[1].parse::<usize>().unwrap();
            let month = capture[2].parse::<usize>().unwrap();
            let day = capture[3].parse::<usize>().unwrap();
            let hour = capture[4].parse::<usize>().unwrap();
            let minute = capture[5].parse::<usize>().unwrap();
            let mut kind = EventKind::FallAsleep;
            if &capture[6] == "wakes up" {
                kind = EventKind::WakeUp;
            } else if capture[6].starts_with("Guard") {
                let guard_id = capture[7].parse::<usize>().unwrap();
                kind = EventKind::BeginShift(guard_id);
            }
            Event {
                year,
                month,
                day,
                hour,
                minute,
                event_kind: kind,
            }
        })
        .collect::<Vec<Event>>();

    print_log(log);

    Ok(())
}

fn print_log(log: Vec<Event>) {
    for event in log {
        print!(
            "{}-{:02}-{:02} {:02}:{:02}",
            event.year, event.month, event.day, event.hour, event.minute
        );
        println!(
            " {}",
            match event.event_kind {
                EventKind::BeginShift(id) => format!("Guard #{} begins shift", id),
                EventKind::FallAsleep => "falls asleep".to_string(),
                EventKind::WakeUp => "wakes up".to_string(),
            }
        );
    }
}

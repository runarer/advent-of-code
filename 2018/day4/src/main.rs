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

struct Guard {
    id: usize,
    total_sleep: usize,
    sleep_minutes: [usize; 60],
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let log = parse_log_content(content);

    let guards = calculate_guard_sleep(&log);
    let sleepiest_guard = find_sleepiest_guard(&guards).unwrap();
    let most_asleep_minute = find_minute_most_asleeped(sleepiest_guard);
    println!("Part 1: {}", sleepiest_guard.id * most_asleep_minute);

    let max_minute_sleeper_time_id = find_guard_with_higest_sleep_minute(guards);
    println!("Part 2: {}", max_minute_sleeper_time_id);

    Ok(())
}

fn parse_log_content(content: String) -> Vec<Event> {
    let re = Regex::new(r"\[(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)\] ((?:Guard #(\d+) begins shift)|(?:falls asleep)|(?:wakes up))").unwrap();

    let mut log = content
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

    sort_log(&mut log);
    log
}

// fn print_log(log: &Vec<Event>) {
//     for event in log {
//         println!(
//             "{}-{:02}-{:02} {:02}:{:02} {}",
//             event.year,
//             event.month,
//             event.day,
//             event.hour,
//             event.minute,
//             match event.event_kind {
//                 EventKind::BeginShift(id) => format!("Guard #{} begins shift", id),
//                 EventKind::FallAsleep => "falls asleep".to_string(),
//                 EventKind::WakeUp => "wakes up".to_string(),
//             }
//         );
//     }
// }

// fn print_guards(guards: &Vec<Guard>) {
//     for guard in guards {
//         println!(
//             "Guard #{}: total sleep {} minutes\n\tsleep minutes: {:?}",
//             guard.id, guard.total_sleep, guard.sleep_minutes
//         );
//     }
// }

fn sort_log(log: &mut Vec<Event>) {
    log.sort_by(|a, b| {
        (a.year, a.month, a.day, a.hour, a.minute).cmp(&(b.year, b.month, b.day, b.hour, b.minute))
    });
}

fn calculate_guard_sleep(log: &Vec<Event>) -> Vec<Guard> {
    let mut guards: Vec<Guard> = Vec::new();
    let mut current_guard: Option<&mut Guard> = None;
    let mut guard_fell_asleep_at = 0;

    for event in log {
        match event.event_kind {
            EventKind::BeginShift(id) => {
                if let Some(guard) = guards.iter_mut().find(|g| g.id == id) {
                    current_guard = Some(guard);
                } else {
                    guards.push(Guard {
                        id,
                        total_sleep: 0,
                        sleep_minutes: [0; 60],
                    });
                    current_guard = guards.last_mut();
                }
            }
            EventKind::FallAsleep => {
                guard_fell_asleep_at = event.minute;
            }
            EventKind::WakeUp => {
                if let Some(guard) = current_guard.as_mut() {
                    for minute in guard_fell_asleep_at..event.minute {
                        guard.sleep_minutes[minute] += 1;
                    }
                    let duration = event.minute - guard_fell_asleep_at;
                    guard.total_sleep += duration;
                }
            }
        }
    }

    guards
}

fn find_sleepiest_guard(guards: &Vec<Guard>) -> Option<&Guard> {
    guards.iter().max_by_key(|g| g.total_sleep)
}

// iter og enumerate lager par med veriden og minuttet(index)
// så finner vi maks minutter
// deretter hentes ut minuttet
fn find_minute_most_asleeped(guard: &Guard) -> usize {
    guard
        .sleep_minutes
        .iter()
        .enumerate()
        .max_by_key(|(_, count)| *count)
        .map(|(minute, _)| minute)
        .unwrap_or(0)
}

fn find_guard_with_higest_sleep_minute(guards: Vec<Guard>) -> usize {
    let mut max_guard_id = 0;
    let mut max_count = 0;
    let mut max_minute = 0;

    for guard in guards {
        let (minute, count) = guard
            .sleep_minutes
            .iter()
            .enumerate()
            .max_by_key(|(_, count)| *count)
            .unwrap();

        if count > &max_count {
            max_count = *count;
            max_minute = minute;
            max_guard_id = guard.id;
        }
    }

    max_guard_id * max_minute
}

use std::io;

pub struct Instruction {
    pub opcode: u8,
    pub input_a: i32,
    pub input_b: i32,
    pub output: i32,
}

pub struct TestCase {
    pub before: [i32; 4], //Vec<i32>,
    pub after: [i32; 4],  //Vec<i32>,
    pub instruction: Instruction,
}

impl Instruction {
    pub fn new(line: &str) -> Self {
        let mut parts = line.trim().split_whitespace();

        Instruction {
            opcode: parts
                .next()
                .expect("Opcode not found")
                .parse::<u8>()
                .expect("Opcode not parsed"),
            input_a: parts
                .next()
                .expect("Input A not found")
                .parse::<i32>()
                .expect("Input B not parsed"),
            input_b: parts
                .next()
                .expect("Input B not found")
                .parse::<i32>()
                .expect("Input A not parsed"),
            output: parts
                .next()
                .expect("Outcode not found")
                .parse::<i32>()
                .expect("Outcode not parsed"),
        }
    }
}

impl TestCase {
    pub fn new(before: &str, instructions: &str, after: &str) -> Self {
        TestCase {
            before: create_register(before),
            after: create_register(after),
            instruction: Instruction::new(instructions),
        }
    }
}

fn create_register(register: &str) -> [i32; 4] {
    let temp = register
        .trim()
        .split_once('[')
        .expect("Could not split")
        .1
        .trim_matches(']')
        .split(',')
        .map(|n| n.trim().parse::<i32>().expect("register not parsed"))
        .collect::<Vec<i32>>();

    [temp[0], temp[1], temp[2], temp[3]]
}

pub fn parse_content(content: &String) -> Result<(Vec<TestCase>, Vec<Instruction>), String> {
    let parts = match content.split_once("\n\n\n") {
        Some(s) => s,
        None => return Err("Could not splitt lines".to_string()),
    };
    // .expect("Could not splitt lines");
    let mut lines = parts.0.lines();

    let mut test_cases: Vec<TestCase> = Vec::new();

    // Grab four lines and parse them into test cases.
    loop {
        let before_line = lines.next();
        if before_line == None {
            break;
        }
        let before_line = before_line.unwrap();
        let number_line = match lines.next() {
            Some(s) => s,
            None => return Err("Number line not found".to_string()),
        }; //.expect("Number line not found");
        let after_line = match lines.next() {
            Some(s) => s,
            None => return Err("After line not found".to_string()),
        }; //.expect("after line not found");
        lines.next();
        test_cases.push(TestCase::new(before_line, number_line, after_line));
    }

    // Parse the instructions
    let lines = parts.1.lines();
    let instructions: Vec<Instruction> = lines
        .filter(|line| !line.trim().is_empty())
        .map(|line| Instruction::new(line))
        .collect();

    Ok((test_cases, instructions))
}

pub fn addr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] + register[input_b as usize];
}

pub fn addi(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] + input_b;
}

pub fn mulr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] * register[input_b as usize];
}

pub fn muli(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] * input_b;
}

pub fn banr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] & register[input_b as usize];
}

pub fn bani(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] & input_b;
}

pub fn borr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] | register[input_b as usize];
}
pub fn bori(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize] | input_b;
}

pub fn setr(register: &mut [i32; 4], input_a: i32, _input_b: i32, output: u8) {
    register[output as usize] = register[input_a as usize]
}
pub fn seti(register: &mut [i32; 4], input_a: i32, _input_b: i32, output: u8) {
    register[output as usize] = input_a;
}

pub fn gtir(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if input_a > register[input_b as usize] {
        1
    } else {
        0
    };
}
pub fn gtri(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if register[input_a as usize] > input_b {
        1
    } else {
        0
    };
}
pub fn gtrr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if register[input_a as usize] > register[input_b as usize] {
        1
    } else {
        0
    };
}

pub fn eqir(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if input_a == register[input_b as usize] {
        1
    } else {
        0
    };
}
pub fn eqri(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if register[input_a as usize] == input_b {
        1
    } else {
        0
    };
}
pub fn eqrr(register: &mut [i32; 4], input_a: i32, input_b: i32, output: u8) {
    register[output as usize] = if register[input_a as usize] == register[input_b as usize] {
        1
    } else {
        0
    };
}

fn compare_regs(a: &[i32; 4], b: &[i32; 4]) -> bool {
    a[0] == b[0] && a[1] == b[1] && a[2] == b[2] && a[3] == b[3]
}

fn main() -> io::Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&args[1])?;

    let (test_cases, _instructions) = parse_content(&content).unwrap();
    let mut current_processing = 0;
    let computer = [
        addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri,
        eqrr,
    ];

    let mut three_or_more = 0;
    loop {
        if current_processing >= test_cases.len() {
            break;
        }
        let mut hit = 0;
        for i in 0..16 {
            let mut reg: [i32; 4] = test_cases[current_processing].before.clone();
            computer[i](
                &mut reg,
                test_cases[current_processing].instruction.input_a,
                test_cases[current_processing].instruction.input_b,
                test_cases[current_processing].instruction.output as u8,
            );
            if compare_regs(&reg, &test_cases[current_processing].after) {
                hit += 1;
            }
        }
        if hit >= 3 {
            three_or_more += 1;
        }
        current_processing += 1;
    }

    println!("Part 1: {three_or_more}");

    Ok(())
}

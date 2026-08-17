#![allow(dead_code)]

use std::cell::RefCell;
use std::io::{self, Read};

/// A position on the board: `(row, column)`, each in `0..SIZE`.
pub type Coordinate = (usize, usize);
/// The value printed on a tile (always a power of two).
pub type Value = u64;

const SIZE: usize = 4;
const WIN_TILE: u64 = 2048;

// ------------------------------------------------------------------
// Provided spawner. You must NOT modify anything in this section.
//
// `next_spawn` returns the coordinate and value of the next tile to
// place. It is driven by a small deterministic pseudo-random generator
// seeded from the `TFE_SEED` environment variable (default 1), so the
// sequence is fixed for a given seed. If the coordinate it returns is
// already occupied, just call `next_spawn` again and try the next one.
// ------------------------------------------------------------------
thread_local! {
    static RNG_STATE: RefCell<u64> = RefCell::new(spawn_seed());
}

fn spawn_seed() -> u64 {
    std::env::var("TFE_SEED")
        .ok()
        .and_then(|s| s.parse::<u64>().ok())
        .filter(|&s| s != 0)
        .unwrap_or(1)
}

fn next_rng() -> u64 {
    RNG_STATE.with(|state| {
        let mut x = *state.borrow();
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        *state.borrow_mut() = x;
        x
    })
}

pub fn next_spawn() -> (Coordinate, Value) {
    let r = next_rng();
    let row = (r % SIZE as u64) as usize;
    let col = ((r / SIZE as u64) % SIZE as u64) as usize;
    let value = if (r >> 8) % 10 == 0 { 4 } else { 2 };
    ((row, col), value)
}
// ------------------------------------------------------------------

type Board = [[u64; SIZE]; SIZE];

fn spawn_tile(board: &mut Board) {
    loop {
        let ((row, col), value) = next_spawn();
        if board[row][col] == 0 {
            board[row][col] = value;
            return;
        }
    }
}

fn print_board(board: &Board) {
    for row in board {
        let cells: Vec<String> = row
            .iter()
            .map(|&v| {
                if v == 0 {
                    format!("{:>4}", ".")
                } else {
                    format!("{:>4}", v)
                }
            })
            .collect();
        println!("{}", cells.join(" "));
    }
}

fn compress_line(line: &[u64], score: &mut u64) -> Vec<u64> {
    let mut out = vec![0u64; SIZE];
    let mut idx = 0;
    let mut just_merged = false;
    for &v in line.iter().filter(|&&v| v != 0) {
        if idx > 0 && out[idx - 1] == v && !just_merged {
            out[idx - 1] = v * 2;
            *score += v * 2;
            just_merged = true;
        } else {
            out[idx] = v;
            idx += 1;
            just_merged = false;
        }
    }
    out
}

fn do_move(board: &mut Board, dir: &str, score: &mut u64) -> bool {
    let mut changed = false;
    for i in 0..SIZE {
        let coords: Vec<Coordinate> = match dir {
            "L" => (0..SIZE).map(|j| (i, j)).collect(),
            "R" => (0..SIZE).rev().map(|j| (i, j)).collect(),
            "U" => (0..SIZE).map(|j| (j, i)).collect(),
            "D" => (0..SIZE).rev().map(|j| (j, i)).collect(),
            _ => unreachable!(),
        };
        let line: Vec<u64> = coords.iter().map(|&(r, c)| board[r][c]).collect();
        let new_line = compress_line(&line, score);
        for (idx, &(r, c)) in coords.iter().enumerate() {
            if board[r][c] != new_line[idx] {
                board[r][c] = new_line[idx];
                changed = true;
            }
        }
    }
    changed
}

fn has_won(board: &Board) -> bool {
    board.iter().flatten().any(|&v| v >= WIN_TILE)
}

fn any_move_possible(board: &Board) -> bool {
    for r in 0..SIZE {
        for c in 0..SIZE {
            if board[r][c] == 0 {
                return true;
            }
            if r + 1 < SIZE && board[r][c] == board[r + 1][c] {
                return true;
            }
            if c + 1 < SIZE && board[r][c] == board[r][c + 1] {
                return true;
            }
        }
    }
    false
}

fn main() {
    // TODO: Implement 2048 here!
    let mut board: Board = [[0; SIZE]; SIZE];
    let mut score: u64 = 0;

    spawn_tile(&mut board);
    spawn_tile(&mut board);

    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    for line in input.lines() {
        match line.trim() {
            "PRINT" => print_board(&board),
            "SCORE" => println!("Score: {score}"),
            dir @ ("L" | "R" | "U" | "D") => {
                let changed = do_move(&mut board, dir, &mut score);
                if changed {
                    if has_won(&board) {
                        println!("You win!");
                        print_board(&board);
                        println!("Score: {score}");
                        return;
                    }
                    spawn_tile(&mut board);
                    if !any_move_possible(&board) {
                        println!("You lost!");
                        print_board(&board);
                        println!("Score: {score}");
                        return;
                    }
                }
            }
            _ => {}
        }
    }
}

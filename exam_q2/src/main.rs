use exam_q2_lib::{first_line_or, Scanner};

fn main() {
    let text = "name: Robin\nrole: admin\nrole: guest";
    let line = first_line_or(text, "role:", "role: none");
    println!("First role line: {line}");

    let mut scanner = Scanner::new("  the quick,brown  fox ", " ,");
    print!("Tokens:");
    while let Some(tok) = scanner.next_token() {
        print!(" {tok}");
    }
    println!();
}

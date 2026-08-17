use exam_q2::{first_line_or, Scanner};

fn main() {
    let text = "user: alice\nrole: admin\nshell: bash";
    let line = first_line_or(text, "role", "role: none");
    println!("First role line: {line}");

    let mut scanner = Scanner::new("  the quick  brown fox ", " ");
    let mut tokens = Vec::new();
    while let Some(token) = scanner.next_token() {
        tokens.push(token);
    }
    println!("Tokens: {}", tokens.join(" "));
}

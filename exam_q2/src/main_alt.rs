use exam_q2_lib::{first_line_or, Scanner};

fn main() {
    let text = String::from("id: 7\nname: Sam");
    let fallback = String::from("(none)");
    let found;
    {
        let prefix = String::from("name:");
        found = first_line_or(&text, &prefix, &fallback);
    }
    println!("Found: {found}");

    let source = String::from("a-b-c");
    let mut collected: Vec<&str> = Vec::new();
    let mut scanner = Scanner::new(&source, "-");
    while let Some(tok) = scanner.next_token() {
        collected.push(tok);
    }
    drop(scanner);
    println!("Collected: {collected:?}");
}

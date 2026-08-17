use exam_q2::{first_line_or, Scanner};

fn main() {
    // `prefix` lives shorter than the returned reference, so this only
    // compiles if `prefix` has its own independent lifetime.
    let text = String::from("id: 42\nname: Sam\ncity: Sydney");
    let found;
    {
        let prefix = String::from("name");
        found = first_line_or(&text, &prefix, "name: unknown");
    }
    println!("Found: {found}");

    // The delimiters and the Scanner itself are dropped before the tokens
    // are used, so this only compiles if tokens borrow from the source
    // (&'src str) rather than from the scanner (&mut self).
    let source = "a,b;c";
    let collected: Vec<&str>;
    {
        let delims = String::from(",;");
        let mut scanner = Scanner::new(source, &delims);
        let mut tokens = Vec::new();
        while let Some(token) = scanner.next_token() {
            tokens.push(token);
        }
        collected = tokens;
    }
    println!("Collected: {collected:?}");
}

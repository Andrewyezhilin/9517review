use require_lifetimes::require_lifetimes;

/// Returns the first line of `text` that starts with `prefix`.
/// If no line matches, returns `fallback` instead.
/// (4 marks)
#[require_lifetimes]
pub fn first_line_or<'a, 'b>(text: &'a str, prefix: &'b str, fallback: &'a str) -> &'a str {
    for line in text.lines() {
        if line.starts_with(prefix) {
            return line;
        }
    }
    fallback
}

/// A scanner containing the delimiter characters,
/// and the text it has not scanned yet.
/// (2 marks: this struct and `new`)
pub struct Scanner<'src, 'delim> {
    remaining: &'src str,
    delimiters: &'delim str,
}

impl<'src, 'delim> Scanner<'src, 'delim> {
    #[require_lifetimes]
    pub fn new(source: &'src str, delimiters: &'delim str) -> Scanner<'src, 'delim> {
        Scanner {
            remaining: source,
            delimiters,
        }
    }

    /// Returns the run of characters up to the next delimiter.
    /// Leading delimiters are skipped. Returns `None` once no tokens remain.
    /// (4 marks)
    #[require_lifetimes]
    pub fn next_token<'a>(&'a mut self) -> Option<&'src str> {
        let delimiters = self.delimiters;
        let start = self.remaining.trim_start_matches(|c: char| delimiters.contains(c));
        if start.is_empty() {
            self.remaining = start;
            return None;
        }
        let end = start.find(|c: char| delimiters.contains(c)).unwrap_or(start.len());
        let (token, rest) = start.split_at(end);
        self.remaining = rest;
        Some(token)
    }
}

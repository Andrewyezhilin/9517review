use exam_q5::Grouped;

fn main() {
    // Basic: String keys, i32 values (original behaviour).
    let mut g: Grouped<String, i32> = Grouped::new();
    for n in [10, 20, 30, 40, 50, 60] {
        g.insert_with(n, |v| if v % 2 == 0 { "even".to_string() } else { "odd".to_string() });
    }
    println!("Total: {}", g.total());
    println!("Sorted: {:?}", g.into_sorted());

    // char keys, String-derived values: generic K.
    let mut byc: Grouped<char, usize> = Grouped::new();
    for w in ["apple", "banana", "cherry", "avocado", "cheese"] {
        byc.insert(w.chars().next().unwrap(), w.len());
    }
    println!("Total: {}", byc.total());
    println!("Sorted: {:?}", byc.into_sorted());

    // retain_groups with an environment-capturing closure (not a fn pointer).
    let mut r: Grouped<String, i32> = Grouped::new();
    for (k, v) in [("N", 1), ("S", 2), ("N", 3), ("W", 4), ("S", 5)] {
        r.insert(k.to_string(), v);
    }
    let min_len = 2;
    r.retain_groups(|_k, vs| vs.len() >= min_len);
    println!("Total after retain: {}", r.total());
    for (k, vs) in r.into_sorted() {
        println!("{k}: {vs:?}");
    }

    // map_values changing the value type (i32 -> String) with an FnMut
    // closure that mutates a captured counter.
    let mut m: Grouped<String, i32> = Grouped::new();
    for v in [1, 2, 3] {
        m.insert("nums".to_string(), v);
    }
    let mut counter = 0;
    let mapped: Grouped<String, String> = m.map_values(|v| {
        counter += 1;
        format!("#{v}")
    });
    println!("Sorted: {:?}", mapped.into_sorted());
    println!("Counter: {counter}");

    // insert_with with an FnOnce closure that consumes a captured value:
    // only compiles if the bound really is FnOnce.
    let mut once: Grouped<String, i32> = Grouped::new();
    let owned_key = String::from("moved");
    once.insert_with(7, move |_| owned_key);
    println!("Total: {}", once.total());

    // A key type that is Eq + Hash but NOT Ord still works for everything
    // except into_sorted: proves into_sorted's Ord bound is method-local.
    #[derive(PartialEq, Eq, Hash, Debug)]
    struct NoOrd(u8);
    let mut n: Grouped<NoOrd, i32> = Grouped::new();
    n.insert(NoOrd(1), 100);
    println!("Total: {}", n.total());
}

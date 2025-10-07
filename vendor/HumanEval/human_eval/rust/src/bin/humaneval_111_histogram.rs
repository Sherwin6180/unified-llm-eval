use std::collections::HashMap;

/// Given a string representing a space separated lowercase letters, return a HashMap
/// of the letter with the most repetition and containing the corresponding count.
/// If several letters have the same occurrence, return all of them.
/// Example:
/// >>> histogram(String::from("a b c"))
/// HashMap::from([(String::from("a"), 1), (String::from("b"), 1), (String::from("c"), 1)])
/// >>> histogram(String::from("a b b a"))
/// HashMap::from([(String::from("a"), 2), (String::from("b"), 2)])
/// >>> histogram(String::from("a b c a b"))
/// HashMap::from([(String::from("a"), 2), (String::from("b"), 2)])
/// >>> histogram(String::from("b b b b a"))
/// HashMap::from([(String::from("b"), 4)])
/// >>> histogram(String::from(""))
/// HashMap::from([])
fn histogram(test: String) -> HashMap<String, isize> {


    let mut map: HashMap<String, isize> = HashMap::new();
    let words: Vec<&str> = test.split_whitespace().collect();
    for word in words {
        let count = map.entry(word.to_string()).or_insert(0);
        *count += 1;
    }
    map}

fn main() {
    let candidate = histogram;
    assert_eq!(candidate(String::from("a b b a")), HashMap::from([(String::from("a"), 2), (String::from("b"), 2)]));
    assert_eq!(candidate(String::from("a b c a b")), HashMap::from([(String::from("a"), 2), (String::from("b"), 2)]));
    assert_eq!(candidate(String::from("a b c d g")), HashMap::from([(String::from("a"), 1), (String::from("b"), 1), (String::from("c"), 1), (String::from("d"), 1), (String::from("g"), 1)]));
    assert_eq!(candidate(String::from("r t g")), HashMap::from([(String::from("r"), 1), (String::from("t"), 1), (String::from("g"), 1)]));
    assert_eq!(candidate(String::from("b b b b a")), HashMap::from([(String::from("b"), 4)]));
    assert_eq!(candidate(String::from("r t g")), HashMap::from([(String::from("r"), 1), (String::from("t"), 1), (String::from("g"), 1)]));
    assert_eq!(candidate(String::from("")), HashMap::from([]));
    assert_eq!(candidate(String::from("a")), HashMap::from([(String::from("a"), 1)]));
}

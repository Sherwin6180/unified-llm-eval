/// Given a string s and a natural number n, you have been tasked to implement 
/// a function that returns a vector of all words from string s that contain exactly 
/// n consonants, in order these words appear in the string s.
/// If the string s is empty then the function should return an empty vector.
/// Note: you may assume the input string contains only letters and spaces.
/// Examples:
/// >>> select_words(String::from("Mary had a little lamb"), 4)
/// vec![String::from("little")]
/// >>> select_words(String::from("Mary had a little lamb"), 3)
/// vec![String::from("Mary"), String::from("lamb")]
/// >>> select_words(String::from("simple white space"), 2)
/// Vec::<String>::new()
/// >>> select_words(String::from("Hello world"), 4)
/// vec![String::from("world")]
/// >>> select_words(String::from("Uncle sam"), 3)
/// vec![String::from("Uncle")]
fn select_words(s: String, n: isize) -> Vec<String> {


    let mut words = s.split_whitespace();
    let mut result = Vec::new();
    for word in words {
        let mut consonants = 0;
        for c in word.chars() {
            match c {
                'a'..='z' if "aeiou".contains(c) => {}
                _ => consonants += 1,
            }
        }
        if consonants as isize == n {
            result.push(word.to_string());
        }
    }
    result}

fn main() {
    let candidate = select_words;
    assert_eq!(candidate(String::from("Mary had a little lamb"), 4), vec![String::from("little")]);
    assert_eq!(candidate(String::from("Mary had a little lamb"), 3), vec![String::from("Mary"), String::from("lamb")]);
    assert_eq!(candidate(String::from("simple white space"), 2), Vec::<String>::new());
    assert_eq!(candidate(String::from("Hello world"), 4), vec![String::from("world")]);
    assert_eq!(candidate(String::from("Uncle sam"), 3), vec![String::from("Uncle")]);
    assert_eq!(candidate(String::from(""), 4), Vec::<String>::new());
    assert_eq!(candidate(String::from("a b c d e f"), 1), vec![String::from("b"), String::from("c"), String::from("d"), String::from("f")]);
}

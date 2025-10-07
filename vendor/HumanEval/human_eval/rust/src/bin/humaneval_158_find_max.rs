/// Write a function that accepts a vector of strings.
/// The vector contains different words. Return the word with maximum number
/// of unique characters. If multiple strings have maximum number of unique
/// characters, return the one which comes first in lexicographical order.
/// >>> find_max(vec![String::from("name"), String::from("of"), String::from("string")])
/// String::from("string")
/// >>> find_max(vec![String::from("name"), String::from("enam"), String::from("game")])
/// String::from("enam")
/// >>> find_max(vec![String::from("aaaaaaa"), String::from("bb"), String::from("cc")])
/// String::from("aaaaaaa")
fn find_max(words: Vec<String>) -> String {


    let mut max_word = words[0].clone();
    let mut max_unique_chars = 0;

    for word in words {
        let unique_chars = word.chars().collect::<std::collections::HashSet<_>>().len();
        if unique_chars > max_unique_chars || (unique_chars == max_unique_chars && word < max_word) {
            max_word = word;
            max_unique_chars = unique_chars;
        }
    }

    max_word}

fn main() {
    let candidate = find_max;
    assert_eq!(candidate(vec![String::from("name"), String::from("of"), String::from("string")]), String::from("string"));
    assert_eq!(candidate(vec![String::from("name"), String::from("enam"), String::from("game")]), String::from("enam"));
    assert_eq!(candidate(vec![String::from("aaaaaaa"), String::from("bb"), String::from("cc")]), String::from("aaaaaaa"));
    assert_eq!(candidate(vec![String::from("abc"), String::from("cba")]), String::from("abc"));
    assert_eq!(candidate(vec![String::from("play"), String::from("this"), String::from("game"), String::from("of"), String::from("footbott")]), String::from("footbott"));
    assert_eq!(candidate(vec![String::from("we"), String::from("are"), String::from("gonna"), String::from("rock")]), String::from("gonna"));
    assert_eq!(candidate(vec![String::from("we"), String::from("are"), String::from("a"), String::from("mad"), String::from("nation")]), String::from("nation"));
    assert_eq!(candidate(vec![String::from("this"), String::from("is"), String::from("a"), String::from("prrk")]), String::from("this"));
    assert_eq!(candidate(vec![String::from("b")]), String::from("b"));
    assert_eq!(candidate(vec![String::from("play"), String::from("play"), String::from("play")]), String::from("play"));
}

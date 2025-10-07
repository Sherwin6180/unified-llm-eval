/// Write a function that takes a string and returns an ordered version of it.
/// Ordered version of string, is a string where all words (separated by space)
/// are replaced by a new word where all the characters arranged in
/// ascending order based on ascii value.
/// Note: You should keep the order of words and blank spaces in the sentence.
/// For example:
/// >>> anti_shuffle(String::from("Hi"))
/// String::from("Hi")
/// >>> anti_shuffle(String::from("hello"))
/// String::from("ehllo")
/// >>> anti_shuffle(String::from("Hello World!!!"))
/// String::from("Hello !!!Wdlor")
fn anti_shuffle(s: String) -> String {


    let mut words = s.split_whitespace();
    let mut result = String::new();
    for word in words {
        let mut chars: Vec<char> = word.chars().collect();
        chars.sort_unstable();
        result.push_str(&chars.concat());
        result.push_str(" ");
    }
    result.trim_end().to_string()}

fn main() {
    let candidate = anti_shuffle;
    assert_eq!(candidate(String::from("Hi")), String::from("Hi"));
    assert_eq!(candidate(String::from("hello")), String::from("ehllo"));
    assert_eq!(candidate(String::from("number")), String::from("bemnru"));
    assert_eq!(candidate(String::from("abcd")), String::from("abcd"));
    assert_eq!(candidate(String::from("Hello World!!!")), String::from("Hello !!!Wdlor"));
    assert_eq!(candidate(String::from("")), String::from(""));
    assert_eq!(candidate(String::from("Hi. My name is Mister Robot. How are you?")), String::from(".Hi My aemn is Meirst .Rboot How aer ?ouy"));
}

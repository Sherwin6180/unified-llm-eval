/// Find the shortest palindrome that begins with a supplied string.
/// Algorithm idea is simple:
/// - Find the longest postfix of supplied string that is a palindrome.
/// - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
/// >>> make_palindrome(String::from(""))
/// String::from("")
/// >>> make_palindrome(String::from("cat"))
/// String::from("catac")
/// >>> make_palindrome(String::from("cata"))
/// String::from("catac")
fn make_palindrome(string: String) -> String {


    let chars: Vec<char> = string.chars().collect();
    let len = string.len();
    let mut i = 0;
    while i < len && chars[i] == chars[len - 1 - i] {
        i += 1;
    }
    let palindrome_suffix = &string[0..len - i];
    let non_palindrome_prefix = &string[len - i..];
    format!("{}{}", string, non_palindrome_prefix.chars().rev().collect::<String>())}

fn main() {
    let candidate = make_palindrome;
    assert_eq!(candidate(String::from("")), String::from(""));
    assert_eq!(candidate(String::from("x")), String::from("x"));
    assert_eq!(candidate(String::from("xyz")), String::from("xyzyx"));
    assert_eq!(candidate(String::from("xyx")), String::from("xyx"));
    assert_eq!(candidate(String::from("jerry")), String::from("jerryrrej"));
}

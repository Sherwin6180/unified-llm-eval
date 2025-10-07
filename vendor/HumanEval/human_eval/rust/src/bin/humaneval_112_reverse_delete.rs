/// Task
/// We are given two strings s and c, you have to deleted all the characters in s that are equal to any character in c
/// then check if the result string is palindrome.
/// A string is called palindrome if it reads the same backward as forward.
/// You should return a tuple containing the result string and true/false for the check.
/// Example
/// >>> reverse_delete(String::from("abcde"), String::from("ae"))
/// (String::from("bcd"), false)
/// >>> reverse_delete(String::from("abcdef"), String::from("b"))
/// (String::from("acdef"), false)
/// >>> reverse_delete(String::from("abcdedcba"), String::from("ab"))
/// (String::from("cdedc"), true)
fn reverse_delete(s: String, c: String) -> (String, bool) {


    let mut s = s.chars().filter(|&ch| !c.contains(ch)).collect::<String>();
    let is_palindrome = s == s.chars().rev().collect::<String>();
    (s, is_palindrome)}

fn main() {
    let candidate = reverse_delete;
    assert_eq!(candidate(String::from("abcde"), String::from("ae")), (String::from("bcd"), false));
    assert_eq!(candidate(String::from("abcdef"), String::from("b")), (String::from("acdef"), false));
    assert_eq!(candidate(String::from("abcdedcba"), String::from("ab")), (String::from("cdedc"), true));
    assert_eq!(candidate(String::from("dwik"), String::from("w")), (String::from("dik"), false));
    assert_eq!(candidate(String::from("a"), String::from("a")), (String::from(""), true));
    assert_eq!(candidate(String::from("abcdedcba"), String::from("")), (String::from("abcdedcba"), true));
    assert_eq!(candidate(String::from("abcdedcba"), String::from("v")), (String::from("abcdedcba"), true));
    assert_eq!(candidate(String::from("vabba"), String::from("v")), (String::from("abba"), true));
    assert_eq!(candidate(String::from("mamma"), String::from("mia")), (String::from(""), true));
}

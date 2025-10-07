/// Create a function that returns true if the last character
/// of a given string is an alphabetical character and is not
/// a part of a word, and false otherwise.
/// Note: "word" is a group of characters separated by space.
/// Examples:
/// >>> check_if_last_char_is_a_letter(String::from("apple pie"))
/// false
/// >>> check_if_last_char_is_a_letter(String::from("apple pi e"))
/// true
/// >>> check_if_last_char_is_a_letter(String::from("apple pi e "))
/// false
/// >>> check_if_last_char_is_a_letter(String::from(""))
/// false
fn check_if_last_char_is_a_letter(txt: String) -> bool {


    if txt.is_empty() {
        return false;
    }
    let last_char = txt.chars().last().unwrap();
    last_char.is_alphabetic() && last_char.is_whitespace()}

fn main() {
    let candidate = check_if_last_char_is_a_letter;
    assert_eq!(candidate(String::from("apple")), false);
    assert_eq!(candidate(String::from("apple pi e")), true);
    assert_eq!(candidate(String::from("eeeee")), false);
    assert_eq!(candidate(String::from("A")), true);
    assert_eq!(candidate(String::from("Pumpkin pie ")), false);
    assert_eq!(candidate(String::from("Pumpkin pie 1")), false);
    assert_eq!(candidate(String::from("")), false);
    assert_eq!(candidate(String::from("eeeee e ")), false);
    assert_eq!(candidate(String::from("apple pie")), false);
    assert_eq!(candidate(String::from("apple pi e ")), false);
}

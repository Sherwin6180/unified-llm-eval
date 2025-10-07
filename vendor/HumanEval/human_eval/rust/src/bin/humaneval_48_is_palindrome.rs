/// Checks if given string is a palindrome
/// >>> is_palindrome(String::from(""))
/// true
/// >>> is_palindrome(String::from("aba"))
/// true
/// >>> is_palindrome(String::from("aaaaa"))
/// true
/// >>> is_palindrome(String::from("zbcd"))
/// false
fn is_palindrome(text: String) -> bool {


    let text = text.chars().collect::<Vec<char>>();
    let len = text.len();
    for i in 0..len / 2 {
        if text[i] != text[len - 1 - i] {
            return false;
        }
    }
    true}

fn main() {
    let candidate = is_palindrome;
    assert_eq!(candidate(String::from("")), true);
    assert_eq!(candidate(String::from("aba")), true);
    assert_eq!(candidate(String::from("aaaaa")), true);
    assert_eq!(candidate(String::from("zbcd")), false);
    assert_eq!(candidate(String::from("xywyx")), true);
    assert_eq!(candidate(String::from("xywyz")), false);
    assert_eq!(candidate(String::from("xywzx")), false);
}

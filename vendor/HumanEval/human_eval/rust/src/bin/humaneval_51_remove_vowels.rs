/// remove_vowels is a function that takes string and returns string without vowels.
/// >>> remove_vowels(String::from(""))
/// String::from("")
/// >>> remove_vowels(String::from("abcdef"))
/// String::from("bcdf")
/// >>> remove_vowels(String::from("aaaaa"))
/// String::from("")
/// >>> remove_vowels(String::from("aaBAA"))
/// String::from("B")
/// >>> remove_vowels(String::from("zbcd"))
/// String::from("zbcd")
fn remove_vowels(text: String) -> String {


    let vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'];
    let mut result = String::new();
    for c in text.chars() {
        if !vowels.contains(&c) {
            result.push(c);
        }
    }
    result}

fn main() {
    let candidate = remove_vowels;
    assert_eq!(candidate(String::from("")), String::from(""));
    assert_eq!(candidate(String::from("abcdef
ghijklm")), String::from("bcdf
ghjklm"));
    assert_eq!(candidate(String::from("fedcba")), String::from("fdcb"));
    assert_eq!(candidate(String::from("eeeee")), String::from(""));
    assert_eq!(candidate(String::from("acBAA")), String::from("cB"));
    assert_eq!(candidate(String::from("EcBOO")), String::from("cB"));
    assert_eq!(candidate(String::from("ybcd")), String::from("ybcd"));
}

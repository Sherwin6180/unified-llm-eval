/// Given a string text, replace all spaces in it with underscores, 
/// and if a string has more than 2 consecutive spaces, 
/// then replace all consecutive spaces with - 
/// >>> fix_spaces(String::from(" Example"))
/// String::from("Example")
/// >>> fix_spaces(String::from(" Example 1"))
/// String::from("Example_1")
/// >>> fix_spaces(String::from(" Example 2"))
/// String::from("_Example_2")
/// >>> fix_spaces(String::from(" Example 3"))
/// String::from("_Example-3")
fn fix_spaces(text: String) -> String {


    let mut result = String::new();
    let mut last_char = ' ';
    for c in text.chars() {
        if c == ' ' {
            if last_char != ' ' {
                result.push('_');
            } else {
                result.push('-');
            }
        } else {
            result.push(c);
        }
        last_char = c;
    }
    result}

fn main() {
    let candidate = fix_spaces;
    assert_eq!(candidate(String::from("Example")), String::from("Example"));
    assert_eq!(candidate(String::from("Mudasir Hanif ")), String::from("Mudasir_Hanif_"));
    assert_eq!(candidate(String::from("Yellow Yellow  Dirty  Fellow")), String::from("Yellow_Yellow__Dirty__Fellow"));
    assert_eq!(candidate(String::from("Exa   mple")), String::from("Exa-mple"));
    assert_eq!(candidate(String::from("   Exa 1 2 2 mple")), String::from("-Exa_1_2_2_mple"));
}

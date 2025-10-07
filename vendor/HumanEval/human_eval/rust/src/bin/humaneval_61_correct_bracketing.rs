/// brackets is a string of "(" and ")".
/// return true if every opening bracket has a corresponding closing bracket.
/// >>> correct_bracketing(String::from("("))
/// false
/// >>> correct_bracketing(String::from("()"))
/// true
/// >>> correct_bracketing(String::from("(()())"))
/// true
/// >>> correct_bracketing(String::from(")(()"))
/// false
fn correct_bracketing(brackets: String) -> bool {


    let mut count = 0;
    for c in brackets.chars() {
        match c {
            '(' => count += 1,
            ')' => count -= 1,
            _ => (),
        }
        if count < 0 {
            return false;
        }
    }
    count == 0}

fn main() {
    let candidate = correct_bracketing;
    assert_eq!(candidate(String::from("()")), true);
    assert_eq!(candidate(String::from("(()())")), true);
    assert_eq!(candidate(String::from("()()(()())()")), true);
    assert_eq!(candidate(String::from("()()((()()())())(()()(()))")), true);
    assert_eq!(candidate(String::from("((()())))")), false);
    assert_eq!(candidate(String::from(")(()")), false);
    assert_eq!(candidate(String::from("(")), false);
    assert_eq!(candidate(String::from("((((")), false);
    assert_eq!(candidate(String::from(")")), false);
    assert_eq!(candidate(String::from("(()")), false);
    assert_eq!(candidate(String::from("()()(()())())(()")), false);
    assert_eq!(candidate(String::from("()()(()())()))()")), false);
}

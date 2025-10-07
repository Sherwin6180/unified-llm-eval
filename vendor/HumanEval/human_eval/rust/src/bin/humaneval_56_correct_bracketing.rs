/// brackets is a string of "<" and ">".
/// return true if every opening bracket has a corresponding closing bracket.
/// >>> correct_bracketing(String::from("<"))
/// false
/// >>> correct_bracketing(String::from("<>"))
/// true
/// >>> correct_bracketing(String::from("<<><>>"))
/// true
/// >>> correct_bracketing(String::from("><<>"))
/// false
fn correct_bracketing(brackets: String) -> bool {


    let mut stack = Vec::new();
    for c in brackets.chars() {
        match c {
            '<' => stack.push(c),
            '>' => {
                if stack.is_empty() {
                    return false;
                }
                stack.pop();
            }
            _ => (),
        }
    }
    stack.is_empty()}

fn main() {
    let candidate = correct_bracketing;
    assert_eq!(candidate(String::from("<>")), true);
    assert_eq!(candidate(String::from("<<><>>")), true);
    assert_eq!(candidate(String::from("<><><<><>><>")), true);
    assert_eq!(candidate(String::from("<><><<<><><>><>><<><><<>>>")), true);
    assert_eq!(candidate(String::from("<<<><>>>>")), false);
    assert_eq!(candidate(String::from("><<>")), false);
    assert_eq!(candidate(String::from("<")), false);
    assert_eq!(candidate(String::from("<<<<")), false);
    assert_eq!(candidate(String::from(">")), false);
    assert_eq!(candidate(String::from("<<>")), false);
    assert_eq!(candidate(String::from("<><><<><>><>><<>")), false);
    assert_eq!(candidate(String::from("<><><<><>><>>><>")), false);
}

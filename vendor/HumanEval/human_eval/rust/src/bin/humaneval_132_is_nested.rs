/// Create a function that takes a string as input which contains only square brackets.
/// The function should return true if and only if there is a valid subsequence of brackets 
/// where at least one bracket in the subsequence is nested.
/// >>> is_nested(String::from("[[]]"))
/// true
/// >>> is_nested(String::from("[]]]]]]][[[[[]"))
/// false
/// >>> is_nested(String::from("[][]"))
/// false
/// >>> is_nested(String::from("[]"))
/// false
/// >>> is_nested(String::from("[[][]]"))
/// true
/// >>> is_nested(String::from("[[]][["))
/// true
fn is_nested(string: String) -> bool {


    let mut stack = Vec::new();
    for c in string.chars() {
        match c {
            '[' => stack.push(c),
            ']' => {
                if stack.is_empty() || stack.pop() != Some('[') {
                    return false;
                }
            }
            _ => (),
        }
    }
    stack.is_empty()}

fn main() {
    let candidate = is_nested;
    assert_eq!(candidate(String::from("[[]]")), true);
    assert_eq!(candidate(String::from("[]]]]]]][[[[[]")), false);
    assert_eq!(candidate(String::from("[][]")), false);
    assert_eq!(candidate(String::from("[]")), false);
    assert_eq!(candidate(String::from("[[[[]]]]")), true);
    assert_eq!(candidate(String::from("[]]]]]]]]]]")), false);
    assert_eq!(candidate(String::from("[][][[]]")), true);
    assert_eq!(candidate(String::from("[[]")), false);
    assert_eq!(candidate(String::from("[]]")), false);
    assert_eq!(candidate(String::from("[[]][[")), true);
    assert_eq!(candidate(String::from("[[][]]")), true);
    assert_eq!(candidate(String::from("")), false);
    assert_eq!(candidate(String::from("[[[[[[[[")), false);
    assert_eq!(candidate(String::from("]]]]]]]]")), false);
}

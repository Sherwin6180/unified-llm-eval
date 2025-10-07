/// You are given a vector of two strings, both strings consist of open
/// parentheses '(' or close parentheses ')' only.
/// Your job is to check if it is possible to concatenate the two strings in
/// some order, that the resulting string will be good.
/// A string S is considered to be good if and only if all parentheses in S
/// are balanced. For example: the string '(())()' is good, while the string
/// '())' is not.
/// Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.
/// Examples:
/// >>> match_parens(vec![String::from("()("), String::from(")")])
/// String::from("Yes")
/// >>> match_parens(vec![String::from(")"), String::from(")")])
/// String::from("No")
fn match_parens(lst: Vec<String>) -> String {


    let mut open = 0;
    for s in lst.iter() {
        for c in s.chars() {
            match c {
                '(' => open += 1,
                ')' => open -= 1,
                _ => (),
            }
            if open < 0 {
                return String::from("No");
            }
        }
    }
    if open == 0 {
        String::from("Yes")
    } else {
        String::from("No")
    }}

fn main() {
    let candidate = match_parens;
    assert_eq!(candidate(vec![String::from("()("), String::from(")")]), String::from("Yes"));
    assert_eq!(candidate(vec![String::from(")"), String::from(")")]), String::from("No"));
    assert_eq!(candidate(vec![String::from("(()(())"), String::from("())())")]), String::from("No"));
    assert_eq!(candidate(vec![String::from(")())"), String::from("(()()(")]), String::from("Yes"));
    assert_eq!(candidate(vec![String::from("(())))"), String::from("(()())((")]), String::from("Yes"));
    assert_eq!(candidate(vec![String::from("()"), String::from("())")]), String::from("No"));
    assert_eq!(candidate(vec![String::from("(()("), String::from("()))()")]), String::from("Yes"));
    assert_eq!(candidate(vec![String::from("(((("), String::from("((())")]), String::from("No"));
    assert_eq!(candidate(vec![String::from(")(()"), String::from("(()(")]), String::from("No"));
    assert_eq!(candidate(vec![String::from(")("), String::from(")(")]), String::from("No"));
    assert_eq!(candidate(vec![String::from("("), String::from(")")]), String::from("Yes"));
    assert_eq!(candidate(vec![String::from(")"), String::from("(")]), String::from("Yes"));
}

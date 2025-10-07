/// Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
/// separate those group into separate strings and return the vector of those.
/// Separate groups are balanced (each open brace is properly closed) and not nested within each other
/// Ignore any spaces in the input string.
/// >>> separate_paren_groups(String::from("( ) (( )) (( )( ))"))
/// vec![String::from("()"), String::from("(())"), String::from("(()())")]
fn separate_paren_groups(paren_string: String) -> Vec<String> {


    let mut paren_vec: Vec<String> = vec![];
    let mut current_group: String = String::new();
    let mut open_braces = 0;

    for c in paren_string.chars() {
        if c == '(' {
            open_braces += 1;
        } else if c == ')' {
            open_braces -= 1;
        }

        current_group.push(c);

        if open_braces == 0 {
            paren_vec.push(current_group.clone());
            current_group.clear();
        }
    }

    paren_vec}

fn main() {
    let candidate = separate_paren_groups;
    assert_eq!(candidate(String::from("(()()) ((())) () ((())()())")), vec![String::from("(()())"), String::from("((()))"), String::from("()"), String::from("((())()())")]);
    assert_eq!(candidate(String::from("() (()) ((())) (((())))")), vec![String::from("()"), String::from("(())"), String::from("((()))"), String::from("(((())))")]);
    assert_eq!(candidate(String::from("(()(())((())))")), vec![String::from("(()(())((())))")]);
    assert_eq!(candidate(String::from("( ) (( )) (( )( ))")), vec![String::from("()"), String::from("(())"), String::from("(()())")]);
}

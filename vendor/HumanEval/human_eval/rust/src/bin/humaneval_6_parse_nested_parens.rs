/// Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
/// For each of the group, output the deepest level of nesting of parentheses.
/// E.g. (()()) has maximum two levels of nesting while ((())) has three.
/// >>> parse_nested_parens(String::from("(()()) ((())) () ((())()())"))
/// vec![2, 3, 1, 3]
fn parse_nested_parens(paren_string: String) -> Vec<isize> {


    let mut result = vec![];
    for group in paren_string.split_whitespace() {
        let mut stack = vec![];
        for c in group.chars() {
            match c {
                '(' => stack.push(c),
                ')' => {
                    if let Some(&'(') = stack.pop() {
                        // do nothing
                    } else {
                        panic!("Mismatched parentheses");
                    }
                }
                _ => panic!("Invalid character in parentheses group"),
            }
        }
        if stack.is_empty() {
            result.push(0);
        } else {
            result.push(stack.len() as isize);
        }
    }
    result}

fn main() {
    let candidate = parse_nested_parens;
    assert_eq!(candidate(String::from("(()()) ((())) () ((())()())")), vec![2, 3, 1, 3]);
    assert_eq!(candidate(String::from("() (()) ((())) (((())))")), vec![1, 2, 3, 4]);
    assert_eq!(candidate(String::from("(()(())((())))")), vec![4]);
}

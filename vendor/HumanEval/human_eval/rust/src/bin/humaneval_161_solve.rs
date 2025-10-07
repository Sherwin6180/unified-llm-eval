/// You are given a string s.
/// if s[i] is a letter, reverse its case from lower to upper or vise versa, 
/// otherwise keep it as it is.
/// If the string contains no letters, reverse the string.
/// The function should return the resulted string.
/// Examples
/// >>> solve(String::from("1234"))
/// String::from("4321")
/// >>> solve(String::from("ab"))
/// String::from("AB")
/// >>> solve(String::from("#a@C"))
/// String::from("#A@c")
fn solve(s: String) -> String {


    let mut chars = s.chars().collect::<Vec<char>>();
    let mut result = String::new();
    for c in chars.into_iter().rev() {
        if c.is_lowercase() {
            result.push(c.to_uppercase().next().unwrap());
        } else if c.is_uppercase() {
            result.push(c.to_lowercase().next().unwrap());
        } else {
            result.push(c);
        }
    }
    result}

fn main() {
    let candidate = solve;
    assert_eq!(candidate(String::from("AsDf")), String::from("aSdF"));
    assert_eq!(candidate(String::from("1234")), String::from("4321"));
    assert_eq!(candidate(String::from("ab")), String::from("AB"));
    assert_eq!(candidate(String::from("#a@C")), String::from("#A@c"));
    assert_eq!(candidate(String::from("#AsdfW^45")), String::from("#aSDFw^45"));
    assert_eq!(candidate(String::from("#6@2")), String::from("2@6#"));
    assert_eq!(candidate(String::from("#$a^D")), String::from("#$A^d"));
    assert_eq!(candidate(String::from("#ccc")), String::from("#CCC"));
}

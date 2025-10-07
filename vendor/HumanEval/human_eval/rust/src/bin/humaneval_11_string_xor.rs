/// Input are two strings a and b consisting only of 1s and 0s.
/// Perform binary XOR on these inputs and return result also as a string.
/// >>> string_xor(String::from("010"), String::from("110"))
/// String::from("100")
fn string_xor(a: String, b: String) -> String {


    let mut result = String::new();
    for (c1, c2) in a.chars().zip(b.chars()) {
        match (c1, c2) {
            ('0', '0') | ('1', '1') => result.push('0'),
            _ => result.push('1'),
        }
    }
    result}

fn main() {
    let candidate = string_xor;
    assert_eq!(candidate(String::from("111000"), String::from("101010")), String::from("010010"));
    assert_eq!(candidate(String::from("1"), String::from("1")), String::from("0"));
    assert_eq!(candidate(String::from("0101"), String::from("0000")), String::from("0101"));
}

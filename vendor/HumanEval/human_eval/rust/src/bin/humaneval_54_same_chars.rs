/// Check if two words have the same characters.
/// >>> same_chars(String::from("eabcdzzzz"), String::from("dddzzzzzzzddeddabc"))
/// true
/// >>> same_chars(String::from("abcd"), String::from("dddddddabc"))
/// true
/// >>> same_chars(String::from("dddddddabc"), String::from("abcd"))
/// true
/// >>> same_chars(String::from("eabcd"), String::from("dddddddabc"))
/// false
/// >>> same_chars(String::from("abcd"), String::from("dddddddabce"))
/// false
/// >>> same_chars(String::from("eabcdzzzz"), String::from("dddzzzzzzzddddabc"))
/// false
fn same_chars(s0: String, s1: String) -> bool {


    let mut chars0 = s0.chars().collect::<Vec<char>>();
    let mut chars1 = s1.chars().collect::<Vec<char>>();

    chars0.sort();
    chars1.sort();

    chars0 == chars1}

fn main() {
    let candidate = same_chars;
    assert_eq!(candidate(String::from("eabcdzzzz"), String::from("dddzzzzzzzddeddabc")), true);
    assert_eq!(candidate(String::from("abcd"), String::from("dddddddabc")), true);
    assert_eq!(candidate(String::from("dddddddabc"), String::from("abcd")), true);
    assert_eq!(candidate(String::from("eabcd"), String::from("dddddddabc")), false);
    assert_eq!(candidate(String::from("abcd"), String::from("dddddddabcf")), false);
    assert_eq!(candidate(String::from("eabcdzzzz"), String::from("dddzzzzzzzddddabc")), false);
    assert_eq!(candidate(String::from("aabb"), String::from("aaccc")), false);
}

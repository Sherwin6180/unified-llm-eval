/// You are given a string s.
/// Your task is to check if the string is haprs or not.
/// A string is haprs if its length is at least 3 and every 3 consecutive letters are distinct
/// For example:
/// >>> is_happy(String::from("a"))
/// false
/// >>> is_happy(String::from("aa"))
/// false
/// >>> is_happy(String::from("abcd"))
/// true
/// >>> is_happy(String::from("aabb"))
/// false
/// >>> is_happy(String::from("adb"))
/// true
/// >>> is_happy(String::from("xyy"))
/// false
fn is_happy(s: String) -> bool {


    let chars: Vec<char> = s.chars().collect();
    if chars.len() < 3 {
        return false;
    }
    for i in 0..chars.len() - 2 {
        if chars[i] == chars[i + 1] || chars[i] == chars[i + 2] || chars[i + 1] == chars[i + 2] {
            return false;
        }
    }
    true}

fn main() {
    let candidate = is_happy;
    assert_eq!(candidate(String::from("a")), false);
    assert_eq!(candidate(String::from("aa")), false);
    assert_eq!(candidate(String::from("abcd")), true);
    assert_eq!(candidate(String::from("aabb")), false);
    assert_eq!(candidate(String::from("adb")), true);
    assert_eq!(candidate(String::from("xyy")), false);
    assert_eq!(candidate(String::from("iopaxpoi")), true);
    assert_eq!(candidate(String::from("iopaxioi")), false);
}

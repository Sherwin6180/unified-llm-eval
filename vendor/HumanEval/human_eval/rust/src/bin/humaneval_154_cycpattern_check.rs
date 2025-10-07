/// You are given 2 words. You need to return true if the second word or any of its rotations is a substring in the first word
/// >>> cycpattern_check(String::from("abcd"), String::from("abd"))
/// false
/// >>> cycpattern_check(String::from("hello"), String::from("ell"))
/// true
/// >>> cycpattern_check(String::from("whassup"), String::from("psus"))
/// false
/// >>> cycpattern_check(String::from("abab"), String::from("baa"))
/// true
/// >>> cycpattern_check(String::from("efef"), String::from("eeff"))
/// false
/// >>> cycpattern_check(String::from("himenss"), String::from("simen"))
/// true
fn cycpattern_check(a: String, b: String) -> bool {


    let len = a.len();
    let b_len = b.len();
    if len < b_len {
        return false;
    }
    let mut b_rotations = vec![b.clone(); 4];
    for i in 1..4 {
        b_rotations[i] = b_rotations[i - 1].chars().skip(1).collect::<String>() + &b_rotations[i - 1].chars().next().unwrap().to_string();
    }
    for br in &b_rotations {
        if a.contains(&br) {
            return true;
        }
    }
    false}

fn main() {
    let candidate = cycpattern_check;
    assert_eq!(candidate(String::from("xyzw"), String::from("xyw")), false);
    assert_eq!(candidate(String::from("yello"), String::from("ell")), true);
    assert_eq!(candidate(String::from("whattup"), String::from("ptut")), false);
    assert_eq!(candidate(String::from("efef"), String::from("fee")), true);
    assert_eq!(candidate(String::from("abab"), String::from("aabb")), false);
    assert_eq!(candidate(String::from("winemtt"), String::from("tinem")), true);
}

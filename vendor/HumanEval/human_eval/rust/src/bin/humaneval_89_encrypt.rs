/// Create a function encrypt that takes a string as an argument and
/// returns a string encrypted with the alphabet being rotated. 
/// The alphabet should be rotated in a manner such that the letters 
/// shift down by two multiplied to two places.
/// For example:
/// >>> encrypt(String::from("hi"))
/// String::from("lm")
/// >>> encrypt(String::from("asdfghjkl"))
/// String::from("ewhjklnop")
/// >>> encrypt(String::from("gf"))
/// String::from("kj")
/// >>> encrypt(String::from("et"))
/// String::from("ix")
fn encrypt(s: String) -> String {


    let mut result = String::new();
    for c in s.chars() {
        if c.is_lowercase() {
            let base = if c >= 'x' { 'a' } else { 'w' };
            result.push((c.clone() - base + 2).rem_euclid(26) + base);
        } else if c.is_uppercase() {
            let base = if c >= 'X' { 'A' } else { 'W' };
            result.push((c.clone() - base + 2).rem_euclid(26) + base);
        } else {
            result.push(c);
        }
    }
    result}

fn main() {
    let candidate = encrypt;
    assert_eq!(candidate(String::from("hi")), String::from("lm"));
    assert_eq!(candidate(String::from("asdfghjkl")), String::from("ewhjklnop"));
    assert_eq!(candidate(String::from("gf")), String::from("kj"));
    assert_eq!(candidate(String::from("et")), String::from("ix"));
    assert_eq!(candidate(String::from("faewfawefaewg")), String::from("jeiajeaijeiak"));
    assert_eq!(candidate(String::from("hellomyfriend")), String::from("lippsqcjvmirh"));
    assert_eq!(candidate(String::from("dxzdlmnilfuhmilufhlihufnmlimnufhlimnufhfucufh")), String::from("hbdhpqrmpjylqmpyjlpmlyjrqpmqryjlpmqryjljygyjl"));
    assert_eq!(candidate(String::from("a")), String::from("e"));
}

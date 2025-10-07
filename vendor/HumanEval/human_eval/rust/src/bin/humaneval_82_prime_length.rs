/// Write a function that takes a string and returns true if the string
/// length is a prime number or false otherwise
/// Examples
/// >>> prime_length(String::from("Hello"))
/// true
/// >>> prime_length(String::from("abcdcba"))
/// true
/// >>> prime_length(String::from("kittens"))
/// true
/// >>> prime_length(String::from("orange"))
/// false
fn prime_length(string: String) -> bool {


    let length = string.len();
    if length < 2 {
        return false;
    }
    for i in 2..length {
        if length % i == 0 {
            return false;
        }
    }
    true}

fn main() {
    let candidate = prime_length;
    assert_eq!(candidate(String::from("Hello")), true);
    assert_eq!(candidate(String::from("abcdcba")), true);
    assert_eq!(candidate(String::from("kittens")), true);
    assert_eq!(candidate(String::from("orange")), false);
    assert_eq!(candidate(String::from("wow")), true);
    assert_eq!(candidate(String::from("world")), true);
    assert_eq!(candidate(String::from("MadaM")), true);
    assert_eq!(candidate(String::from("Wow")), true);
    assert_eq!(candidate(String::from("")), false);
    assert_eq!(candidate(String::from("HI")), true);
    assert_eq!(candidate(String::from("go")), true);
    assert_eq!(candidate(String::from("gogo")), false);
    assert_eq!(candidate(String::from("aaaaaaaaaaaaaaa")), false);
    assert_eq!(candidate(String::from("Madam")), true);
    assert_eq!(candidate(String::from("M")), false);
    assert_eq!(candidate(String::from("0")), false);
}

/// Write a function vowels_count which takes a string representing
/// a word as input and returns the number of vowels in the string.
/// Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
/// vowel, but only when it is at the end of the given word.
/// Example:
/// >>> vowels_count(String::from("abcde"))
/// 2
/// >>> vowels_count(String::from("ACEDY"))
/// 3
fn vowels_count(s: String) -> isize {


    let mut count = 0;
    let last_char = s.chars().last().unwrap();
    for c in s.chars() {
        match c {
            'a' | 'e' | 'i' | 'o' | 'u' | 'A' | 'E' | 'I' | 'O' | 'U' => count += 1,
            _ => (),
        }
    }
    if last_char == 'y' || last_char == 'Y' {
        count += 1;
    }
    count}

fn main() {
    let candidate = vowels_count;
    assert_eq!(candidate(String::from("abcde")), 2);
    assert_eq!(candidate(String::from("Alone")), 3);
    assert_eq!(candidate(String::from("key")), 2);
    assert_eq!(candidate(String::from("bye")), 1);
    assert_eq!(candidate(String::from("keY")), 2);
    assert_eq!(candidate(String::from("bYe")), 1);
    assert_eq!(candidate(String::from("ACEDY")), 3);
}

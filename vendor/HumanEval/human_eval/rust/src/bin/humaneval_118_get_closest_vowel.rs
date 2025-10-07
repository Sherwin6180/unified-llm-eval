/// You are given a word. Your task is to find the closest vowel that stands between 
/// two consonants from the right side of the word (case sensitive).
/// Vowels in the beginning and ending doesn't count. Return empty string if you didn't
/// find any vowel met the above condition. 
/// You may assume that the given string contains English letter only.
/// Example:
/// >>> get_closest_vowel(String::from("yogurt"))
/// String::from("u")
/// >>> get_closest_vowel(String::from("FULL"))
/// String::from("U")
/// >>> get_closest_vowel(String::from("quick"))
/// String::from("")
/// >>> get_closest_vowel(String::from("ab"))
/// String::from("")
fn get_closest_vowel(word: String) -> String {


    let vowels = vec!['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'];
    let word_chars: Vec<char> = word.chars().collect();
    let mut closest_vowel = None;
    let mut min_distance = std::usize::MAX;

    for (i, &c) in word_chars.iter().enumerate() {
        if vowels.contains(&c) {
            if i > 0 && i < word_chars.len() - 1 {
                if !vowels.contains(&word_chars[i - 1]) && !vowels.contains(&word_chars[i + 1]) {
                    let distance = i;
                    if distance < min_distance {
                        min_distance = distance;
                        closest_vowel = Some(c);
                    }
                }
            }
        }
    }

    match closest_vowel {
        Some(c) => c.to_string(),
        None => "".to_string(),
    }}

fn main() {
    let candidate = get_closest_vowel;
    assert_eq!(candidate(String::from("yogurt")), String::from("u"));
    assert_eq!(candidate(String::from("full")), String::from("u"));
    assert_eq!(candidate(String::from("easy")), String::from(""));
    assert_eq!(candidate(String::from("eAsy")), String::from(""));
    assert_eq!(candidate(String::from("ali")), String::from(""));
    assert_eq!(candidate(String::from("bad")), String::from("a"));
    assert_eq!(candidate(String::from("most")), String::from("o"));
    assert_eq!(candidate(String::from("ab")), String::from(""));
    assert_eq!(candidate(String::from("ba")), String::from(""));
    assert_eq!(candidate(String::from("quick")), String::from(""));
    assert_eq!(candidate(String::from("anime")), String::from("i"));
    assert_eq!(candidate(String::from("Asia")), String::from(""));
    assert_eq!(candidate(String::from("Above")), String::from("o"));
}

/// You'll be given a string of words, and your task is to count the number
/// of boredoms. A boredom is a sentence that starts with the word "I".
/// Sentences are delimited by '.', '?' or '!'.
/// For example:
/// >>> is_bored(String::from("Hello world"))
/// 0
/// >>> is_bored(String::from("The sky is blue. The sun is shining. I love this weather"))
/// 1
fn is_bored(S: String) -> isize {


    let mut count = 0;
    let mut words = S.split_whitespace();
    let mut first_word = words.next().unwrap_or(&"");
    while !first_word.is_empty() {
        if first_word.starts_with('I') {
            count += 1;
        }
        first_word = words.next().unwrap_or(&"");
    }
    count}

fn main() {
    let candidate = is_bored;
    assert_eq!(candidate(String::from("Hello world")), 0);
    assert_eq!(candidate(String::from("Is the sky blue?")), 0);
    assert_eq!(candidate(String::from("I love It !")), 1);
    assert_eq!(candidate(String::from("bIt")), 0);
    assert_eq!(candidate(String::from("I feel good today. I will be productive. will kill It")), 2);
    assert_eq!(candidate(String::from("You and I are going for a walk")), 0);
}

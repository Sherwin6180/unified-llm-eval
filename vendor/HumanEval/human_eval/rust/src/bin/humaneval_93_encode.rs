/// Write a function that takes a message, and encodes in such a 
/// way that it swaps case of all letters, replaces all vowels in 
/// the message with the letter that appears 2 places ahead of that 
/// vowel in the english alphabet. 
/// Assume only letters. 
/// Examples:
/// >>> encode(String::from("test"))
/// String::from("TGST")
/// >>> encode(String::from("This is a message"))
/// String::from("tHKS KS C MGSSCGG")
fn encode(message: String) -> String {


    let mut result = String::new();
    for c in message.chars() {
        if c.is_lowercase() {
            result.push(c.to_ascii_uppercase());
        } else {
            result.push(c.to_ascii_lowercase());
        }
    }
    result}

fn main() {
    let candidate = encode;
    assert_eq!(candidate(String::from("TEST")), String::from("tgst"));
    assert_eq!(candidate(String::from("Mudasir")), String::from("mWDCSKR"));
    assert_eq!(candidate(String::from("YES")), String::from("ygs"));
    assert_eq!(candidate(String::from("This is a message")), String::from("tHKS KS C MGSSCGG"));
    assert_eq!(candidate(String::from("I DoNt KnOw WhAt tO WrItE")), String::from("k dQnT kNqW wHcT Tq wRkTg"));
}

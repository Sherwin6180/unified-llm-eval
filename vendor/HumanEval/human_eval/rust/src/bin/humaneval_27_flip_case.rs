/// For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
/// >>> flip_case(String::from("Hello"))
/// String::from("hELLO")
fn flip_case(string: String) -> String {


    string.chars().map(|c| if c.is_lowercase() { c.to_uppercase().next().unwrap() } else { c.to_lowercase().next().unwrap() }).collect()}

fn main() {
    let candidate = flip_case;
    assert_eq!(candidate(String::from("")), String::from(""));
    assert_eq!(candidate(String::from("Hello!")), String::from("hELLO!"));
    assert_eq!(candidate(String::from("These violent delights have violent ends")), String::from("tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS"));
}

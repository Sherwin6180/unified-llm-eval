/// Return vector of all prefixes from shortest to longest of the input string
/// >>> all_prefixes(String::from("abc"))
/// vec![String::from("a"), String::from("ab"), String::from("abc")]
fn all_prefixes(string: String) -> Vec<String> {


    let mut prefixes = vec![];
    for i in 0..string.len() {
        prefixes.push(string[0..=i].to_string());
    }
    prefixes}

fn main() {
    let candidate = all_prefixes;
    assert_eq!(candidate(String::from("")), Vec::<String>::new());
    assert_eq!(candidate(String::from("asdfgh")), vec![String::from("a"), String::from("as"), String::from("asd"), String::from("asdf"), String::from("asdfg"), String::from("asdfgh")]);
    assert_eq!(candidate(String::from("WWW")), vec![String::from("W"), String::from("WW"), String::from("WWW")]);
}

/// Concatenate vector of strings into a single string
/// >>> concatenate(vec![])
/// String::from("")
/// >>> concatenate(vec![String::from("a"), String::from("b"), String::from("c")])
/// String::from("abc")
fn concatenate(strings: Vec<String>) -> String {


    strings.concat()}

fn main() {
    let candidate = concatenate;
    assert_eq!(candidate(Vec::<String>::new()), String::from(""));
    assert_eq!(candidate(vec![String::from("x"), String::from("y"), String::from("z")]), String::from("xyz"));
    assert_eq!(candidate(vec![String::from("x"), String::from("y"), String::from("z"), String::from("w"), String::from("k")]), String::from("xyzwk"));
}

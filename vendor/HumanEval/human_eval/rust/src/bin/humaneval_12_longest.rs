/// Out of vector of strings, return the longest one. Return the first one in case of multiple
/// strings of the same length. Return None in case the input vector is empty.
/// >>> longest(vec![])
/// None
/// >>> longest(vec![String::from("a"), String::from("b"), String::from("c")])
/// Some(String::from("a"))
/// >>> longest(vec![String::from("a"), String::from("bb"), String::from("ccc")])
/// Some(String::from("ccc"))
fn longest(strings: Vec<String>) -> Option<String> {


    strings.iter().max_by_key(|s| s.len()).cloned()}

fn main() {
    let candidate = longest;
    assert_eq!(candidate(Vec::<String>::new()), None);
    assert_eq!(candidate(vec![String::from("x"), String::from("y"), String::from("z")]), Some(String::from("x")));
    assert_eq!(candidate(vec![String::from("x"), String::from("yyy"), String::from("zzzz"), String::from("www"), String::from("kkkk"), String::from("abc")]), Some(String::from("zzzz")));
}

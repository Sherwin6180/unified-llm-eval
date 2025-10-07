/// Filter an input vector of strings only for ones that start with a given prefix.
/// >>> filter_by_prefix(vec![], String::from("a"))
/// Vec::<String>::new()
/// >>> filter_by_prefix(vec![String::from("abc"), String::from("bcd"), String::from("cde"), String::from("array")], String::from("a"))
/// vec![String::from("abc"), String::from("array")]
fn filter_by_prefix(strings: Vec<String>, prefix: String) -> Vec<String> {


    strings.into_iter().filter(|s| s.starts_with(&prefix)).collect()}

fn main() {
    let candidate = filter_by_prefix;
    assert_eq!(candidate(Vec::<String>::new(), String::from("john")), Vec::<String>::new());
    assert_eq!(candidate(vec![String::from("xxx"), String::from("asd"), String::from("xxy"), String::from("john doe"), String::from("xxxAAA"), String::from("xxx")], String::from("xxx")), vec![String::from("xxx"), String::from("xxxAAA"), String::from("xxx")]);
}

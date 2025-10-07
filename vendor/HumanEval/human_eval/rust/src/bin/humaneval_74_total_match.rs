/// Write a function that accepts two vectors of strings and returns the vector that has 
/// total number of chars in the all strings of the vector less than the other vector.
/// if the two vectors have the same number of chars, return the first vector.
/// Examples
/// >>> total_match(vec![], vec![])
/// Vec::<String>::new()
/// >>> total_match(vec![String::from("hi"), String::from("admin")], vec![String::from("hI"), String::from("Hi")])
/// vec![String::from("hI"), String::from("Hi")]
/// >>> total_match(vec![String::from("hi"), String::from("admin")], vec![String::from("hi"), String::from("hi"), String::from("admin"), String::from("project")])
/// vec![String::from("hi"), String::from("admin")]
/// >>> total_match(vec![String::from("hi"), String::from("admin")], vec![String::from("hI"), String::from("hi"), String::from("hi")])
/// vec![String::from("hI"), String::from("hi"), String::from("hi")]
/// >>> total_match(vec![String::from("4")], vec![String::from("1"), String::from("2"), String::from("3"), String::from("4"), String::from("5")])
/// vec![String::from("4")]
fn total_match(lst1: Vec<String>, lst2: Vec<String>) -> Vec<String> {


    let total_chars1 = lst1.iter().map(|s| s.len()).sum::<usize>();
    let total_chars2 = lst2.iter().map(|s| s.len()).sum::<usize>();

    if total_chars1 < total_chars2 {
        lst1
    } else {
        lst2
    }}

fn main() {
    let candidate = total_match;
    assert_eq!(candidate(Vec::<String>::new(), Vec::<String>::new()), Vec::<String>::new());
    assert_eq!(candidate(vec![String::from("hi"), String::from("admin")], vec![String::from("hi"), String::from("hi")]), vec![String::from("hi"), String::from("hi")]);
    assert_eq!(candidate(vec![String::from("hi"), String::from("admin")], vec![String::from("hi"), String::from("hi"), String::from("admin"), String::from("project")]), vec![String::from("hi"), String::from("admin")]);
    assert_eq!(candidate(vec![String::from("4")], vec![String::from("1"), String::from("2"), String::from("3"), String::from("4"), String::from("5")]), vec![String::from("4")]);
    assert_eq!(candidate(vec![String::from("hi"), String::from("admin")], vec![String::from("hI"), String::from("Hi")]), vec![String::from("hI"), String::from("Hi")]);
    assert_eq!(candidate(vec![String::from("hi"), String::from("admin")], vec![String::from("hI"), String::from("hi"), String::from("hi")]), vec![String::from("hI"), String::from("hi"), String::from("hi")]);
    assert_eq!(candidate(vec![String::from("hi"), String::from("admin")], vec![String::from("hI"), String::from("hi"), String::from("hii")]), vec![String::from("hi"), String::from("admin")]);
    assert_eq!(candidate(Vec::<String>::new(), vec![String::from("this")]), Vec::<String>::new());
    assert_eq!(candidate(vec![String::from("this")], Vec::<String>::new()), Vec::<String>::new());
}

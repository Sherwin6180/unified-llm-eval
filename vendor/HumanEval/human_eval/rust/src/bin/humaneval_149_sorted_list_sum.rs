/// Write a function that accepts a vector of strings as a parameter,
/// deletes the strings that have odd lengths from it,
/// and returns the resulted vector with a sorted order,
/// The vector is always a vector of strings and never a vector of numbers,
/// and it may contain duplicates.
/// The order of the vector should be ascending by length of each word, and you
/// should return the vector sorted by that rule.
/// If two words have the same length, sort the vector alphabetically.
/// The function should return a vector of strings in sorted order.
/// You may assume that all words will have the same length.
/// For example:
/// >>> list_sort(vec![String::from("aa"), String::from("a"), String::from("aaa")])
/// vec![String::from("aa")]
/// >>> list_sort(vec![String::from("ab"), String::from("a"), String::from("aaa"), String::from("cd")])
/// vec![String::from("ab"), String::from("cd")]
fn sorted_list_sum(lst: Vec<String>) -> Vec<String> {


    let mut vec = lst.into_iter().filter(|s| s.len() % 2 == 0).collect::<Vec<String>>();
    vec.sort_by(|a, b| {
        let len_cmp = a.len().cmp(&b.len());
        if len_cmp == std::cmp::Ordering::Equal {
            a.cmp(b)
        } else {
            len_cmp
        }
    });
    vec}

fn main() {
    let candidate = sorted_list_sum;
    assert_eq!(candidate(vec![String::from("aa"), String::from("a"), String::from("aaa")]), vec![String::from("aa")]);
    assert_eq!(candidate(vec![String::from("school"), String::from("AI"), String::from("asdf"), String::from("b")]), vec![String::from("AI"), String::from("asdf"), String::from("school")]);
    assert_eq!(candidate(vec![String::from("d"), String::from("b"), String::from("c"), String::from("a")]), Vec::<String>::new());
    assert_eq!(candidate(vec![String::from("d"), String::from("dcba"), String::from("abcd"), String::from("a")]), vec![String::from("abcd"), String::from("dcba")]);
    assert_eq!(candidate(vec![String::from("AI"), String::from("ai"), String::from("au")]), vec![String::from("AI"), String::from("ai"), String::from("au")]);
    assert_eq!(candidate(vec![String::from("a"), String::from("b"), String::from("b"), String::from("c"), String::from("c"), String::from("a")]), Vec::<String>::new());
    assert_eq!(candidate(vec![String::from("aaaa"), String::from("bbbb"), String::from("dd"), String::from("cc")]), vec![String::from("cc"), String::from("dd"), String::from("aaaa"), String::from("bbbb")]);
}

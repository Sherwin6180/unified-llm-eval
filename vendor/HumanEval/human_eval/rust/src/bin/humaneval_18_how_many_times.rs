/// Find how many times a given substring can be found in the original string. Count overlaping cases.
/// >>> how_many_times(String::from(""), String::from("a"))
/// 0
/// >>> how_many_times(String::from("aaa"), String::from("a"))
/// 3
/// >>> how_many_times(String::from("aaaa"), String::from("aa"))
/// 3
fn how_many_times(string: String, substring: String) -> isize {


    let string_len = string.len();
    let substring_len = substring.len();

    if string_len == 0 || substring_len == 0 || string_len < substring_len {
        return 0;
    }

    let mut count = 0;
    let mut index = 0;

    while index <= string_len - substring_len {
        if string[index..index + substring_len] == substring {
            count += 1;
            index += substring_len - 1;
        }
        index += 1;
    }

    count}

fn main() {
    let candidate = how_many_times;
    assert_eq!(candidate(String::from(""), String::from("x")), 0);
    assert_eq!(candidate(String::from("xyxyxyx"), String::from("x")), 4);
    assert_eq!(candidate(String::from("cacacacac"), String::from("cac")), 4);
    assert_eq!(candidate(String::from("john doe"), String::from("john")), 1);
}

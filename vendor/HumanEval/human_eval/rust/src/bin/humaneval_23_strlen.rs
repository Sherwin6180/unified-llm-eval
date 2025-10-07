/// Return length of given string
/// >>> strlen(String::from(""))
/// 0
/// >>> strlen(String::from("abc"))
/// 3
fn strlen(string: String) -> isize {


    string.chars().count() as isize}

fn main() {
    let candidate = strlen;
    assert_eq!(candidate(String::from("")), 0);
    assert_eq!(candidate(String::from("x")), 1);
    assert_eq!(candidate(String::from("asdasnakj")), 9);
}

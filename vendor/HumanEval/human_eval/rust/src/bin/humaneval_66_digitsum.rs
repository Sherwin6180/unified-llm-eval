/// Task
/// Write a function that takes a string as input and returns the sum of the upper characters only'
/// ASCII codes.
/// Examples:
/// >>> digitSum(String::from(""))
/// 0
/// >>> digitSum(String::from("abAB"))
/// 131
/// >>> digitSum(String::from("abcCd"))
/// 67
/// >>> digitSum(String::from("helloE"))
/// 69
/// >>> digitSum(String::from("woArBld"))
/// 131
/// >>> digitSum(String::from("aAaaaXa"))
/// 153
fn digitSum(s: String) -> isize {


    s.chars()
        .filter(|c| c.is_ascii_uppercase())
        .map(|c| c as isize)
        .sum()}

fn main() {
    let candidate = digitSum;
    assert_eq!(candidate(String::from("")), 0);
    assert_eq!(candidate(String::from("abAB")), 131);
    assert_eq!(candidate(String::from("abcCd")), 67);
    assert_eq!(candidate(String::from("helloE")), 69);
    assert_eq!(candidate(String::from("woArBld")), 131);
    assert_eq!(candidate(String::from("aAaaaXa")), 153);
    assert_eq!(candidate(String::from(" How are yOu?")), 151);
    assert_eq!(candidate(String::from("You arE Very Smart")), 327);
}

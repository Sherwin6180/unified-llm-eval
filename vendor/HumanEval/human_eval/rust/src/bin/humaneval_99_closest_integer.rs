/// Create a function that takes a value (string) representing a number
/// and returns the closest integer to it. If the number is equidistant
/// from two integers, round it away from zero.
/// Examples
/// >>> closest_integer(String::from("10"))
/// 10
/// >>> closest_integer(String::from("15.3"))
/// 15
/// Note:
/// Rounding away from zero means that if the given number is equidistant
/// from two integers, the one you should return is the one that is the
/// farthest from zero. For example closest_integer("14.5") should
/// return 15 and closest_integer("-14.5") should return -15.
fn closest_integer(value: String) -> isize {


    let num: f64 = value.parse().unwrap();
    if num.fract() >= 0.5 {
        num.round() as isize
    } else {
        num.floor() as isize
    }}

fn main() {
    let candidate = closest_integer;
    assert_eq!(candidate(String::from("10")), 10);
    assert_eq!(candidate(String::from("14.5")), 15);
    assert_eq!(candidate(String::from("-15.5")), -16);
    assert_eq!(candidate(String::from("15.3")), 15);
    assert_eq!(candidate(String::from("0")), 0);
}

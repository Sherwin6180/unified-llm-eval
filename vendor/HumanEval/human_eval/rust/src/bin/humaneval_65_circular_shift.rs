/// Circular shift the digits of the integer x, shift the digits right by shift
/// and return the result as a string.
/// If shift > number of digits, return digits reversed.
/// >>> circular_shift(12, 1)
/// String::from("21")
/// >>> circular_shift(12, 2)
/// String::from("12")
fn circular_shift(x: isize, shift: isize) -> String {


    let digits = x.to_string().chars().collect::<Vec<char>>();
    let shift = shift % digits.len() as isize;
    if shift < 0 {
        let (front, back) = digits.split_at(digits.len() as isize + shift);
        format!("{}{}", back.into_iter().collect::<String>(), front.into_iter().collect::<String>())
    } else {
        let (front, back) = digits.split_at(shift as usize);
        format!("{}{}", back.into_iter().collect::<String>(), front.into_iter().collect::<String>())
    }}

fn main() {
    let candidate = circular_shift;
    assert_eq!(candidate(100, 2), String::from("001"));
    assert_eq!(candidate(12, 2), String::from("12"));
    assert_eq!(candidate(97, 8), String::from("79"));
    assert_eq!(candidate(12, 1), String::from("21"));
    assert_eq!(candidate(11, 101), String::from("11"));
}

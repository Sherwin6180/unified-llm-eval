/// Given a positive integer N, return the total sum of its digits in binary.
/// Example
/// >>> solve(1000)
/// String::from("1")
/// >>> solve(150)
/// String::from("110")
/// >>> solve(147)
/// String::from("1100")
/// Variables:
/// @N integer
/// Constraints: 0 ≤ N ≤ 10000.
/// Output:
/// a string of binary number
fn solve(N: isize) -> String {


    let binary = format!("{:b}", N);
    let mut sum = 0;
    for c in binary.chars() {
        sum += c.to_digit(10).unwrap() as isize;
    }
    format!("{}", sum)}

fn main() {
    let candidate = solve;
    assert_eq!(candidate(1000), String::from("1"));
    assert_eq!(candidate(150), String::from("110"));
    assert_eq!(candidate(147), String::from("1100"));
    assert_eq!(candidate(333), String::from("1001"));
    assert_eq!(candidate(963), String::from("10010"));
}

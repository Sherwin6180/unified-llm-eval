/// Given a positive integer n, return the count of the numbers of n-digit
/// positive integers that start or end with 1.
fn starts_one_ends(n: isize) -> isize {


    if n == 1 {
        1
    } else {
        (10i64.pow(n - 1) - 1) * 2
    }}

fn main() {
    let candidate = starts_one_ends;
    assert_eq!(candidate(1), 1);
    assert_eq!(candidate(2), 18);
    assert_eq!(candidate(3), 180);
    assert_eq!(candidate(4), 1800);
    assert_eq!(candidate(5), 18000);
}

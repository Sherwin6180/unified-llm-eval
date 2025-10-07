/// Given a positive integer n, return a tuple that has the number of even and odd
/// integer palindromes that fall within the range(1, n), inclusive.
/// Example 1:
/// >>> even_odd_palindrome(3)
/// (1, 2)
/// Explanation:
/// Integer palindrome are 1, 2, 3. one of them is even, and two of them are odd.
/// Example 2:
/// >>> even_odd_palindrome(12)
/// (4, 6)
/// Explanation:
/// Integer palindrome are 1, 2, 3, 4, 5, 6, 7, 8, 9, 11. four of them are even, and 6 of them are odd.
/// Note:
/// 1. 1 <= n <= 10^3
/// 2. returned tuple has the number of even and odd integer palindromes respectively.
fn even_odd_palindrome(n: isize) -> (isize, isize) {


    let mut even = 0;
    let mut odd = 0;
    for i in 1..=n {
        if i.to_string() == i.to_string().chars().rev().collect::<String>() {
            if i % 2 == 0 {
                even += 1;
            } else {
                odd += 1;
            }
        }
    }
    (even, odd)}

fn main() {
    let candidate = even_odd_palindrome;
    assert_eq!(candidate(123), (8, 13));
    assert_eq!(candidate(12), (4, 6));
    assert_eq!(candidate(3), (1, 2));
    assert_eq!(candidate(63), (6, 8));
    assert_eq!(candidate(25), (5, 6));
    assert_eq!(candidate(19), (4, 6));
    assert_eq!(candidate(9), (4, 5));
    assert_eq!(candidate(1), (0, 1));
}

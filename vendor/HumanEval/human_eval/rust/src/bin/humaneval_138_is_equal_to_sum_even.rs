/// Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
/// Example
/// >>> is_equal_to_sum_even(4)
/// false
/// >>> is_equal_to_sum_even(6)
/// false
/// >>> is_equal_to_sum_even(8)
/// true
fn is_equal_to_sum_even(n: isize) -> bool {


    let mut sum = 0;
    let mut count = 0;
    let mut i = 2;
    while sum < n {
        if n % i == 0 {
            sum += i;
            count += 1;
        }
        i += 2;
    }
    sum == n && count == 4}

fn main() {
    let candidate = is_equal_to_sum_even;
    assert_eq!(candidate(4), false);
    assert_eq!(candidate(6), false);
    assert_eq!(candidate(8), true);
    assert_eq!(candidate(10), true);
    assert_eq!(candidate(11), false);
    assert_eq!(candidate(12), true);
    assert_eq!(candidate(13), false);
    assert_eq!(candidate(16), true);
}

/// Given a positive integer n, you have to make a pile of n levels of stones.
/// The first level has n stones.
/// The number of stones in the next level is:
/// - the next odd number if n is odd.
/// - the next even number if n is even.
/// Return the number of stones in each level in a vector, where element at index
/// i represents the number of stones in the level (i+1).
/// Examples:
/// >>> make_a_pile(3)
/// vec![3, 5, 7]
fn make_a_pile(n: isize) -> Vec<isize> {


    let mut result = vec![n];
    let mut next_odd = n + 2;
    let mut next_even = n + 1;
    for _ in 1..n {
        if n % 2 == 0 {
            result.push(next_even);
            next_even += 2;
        } else {
            result.push(next_odd);
            next_odd += 2;
        }
    }
    result}

fn main() {
    let candidate = make_a_pile;
    assert_eq!(candidate(3), vec![3, 5, 7]);
    assert_eq!(candidate(4), vec![4, 6, 8, 10]);
    assert_eq!(candidate(5), vec![5, 7, 9, 11, 13]);
    assert_eq!(candidate(6), vec![6, 8, 10, 12, 14, 16]);
    assert_eq!(candidate(8), vec![8, 10, 12, 14, 16, 18, 20, 22]);
}

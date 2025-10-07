/// triples_sum_to_zero takes a vector of integers as an input.
/// it returns true if there are three distinct elements in the vector that
/// sum to zero, and false otherwise.
/// >>> triples_sum_to_zero(vec![1, 3, 5, 0])
/// false
/// >>> triples_sum_to_zero(vec![1, 3, -2, 1])
/// true
/// >>> triples_sum_to_zero(vec![1, 2, 3, 7])
/// false
/// >>> triples_sum_to_zero(vec![2, 4, -5, 3, 9, 7])
/// true
/// >>> triples_sum_to_zero(vec![1])
/// false
fn triples_sum_to_zero(l: Vec<isize>) -> bool {


    let n = l.len();
    if n < 3 {
        return false;
    }
    l.sort_unstable();
    for i in 0..n {
        let mut left = i + 1;
        let mut right = n - 1;
        while left < right {
            let sum = l[i] + l[left] + l[right];
            if sum == 0 {
                return true;
            } else if sum < 0 {
                left += 1;
            } else {
                right -= 1;
            }
        }
    }
    false}

fn main() {
    let candidate = triples_sum_to_zero;
    assert_eq!(candidate(vec![1, 3, 5, 0]), false);
    assert_eq!(candidate(vec![1, 3, 5, -1]), false);
    assert_eq!(candidate(vec![1, 3, -2, 1]), true);
    assert_eq!(candidate(vec![1, 2, 3, 7]), false);
    assert_eq!(candidate(vec![1, 2, 5, 7]), false);
    assert_eq!(candidate(vec![2, 4, -5, 3, 9, 7]), true);
    assert_eq!(candidate(vec![1]), false);
    assert_eq!(candidate(vec![1, 3, 5, -100]), false);
    assert_eq!(candidate(vec![100, 3, 5, -100]), false);
}

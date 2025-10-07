/// pairs_sum_to_zero takes a vector of integers as an input.
/// it returns true if there are two distinct elements in the vector that
/// sum to zero, and false otherwise.
/// >>> pairs_sum_to_zero(vec![1, 3, 5, 0])
/// false
/// >>> pairs_sum_to_zero(vec![1, 3, -2, 1])
/// false
/// >>> pairs_sum_to_zero(vec![1, 2, 3, 7])
/// false
/// >>> pairs_sum_to_zero(vec![2, 4, -5, 3, 5, 7])
/// true
/// >>> pairs_sum_to_zero(vec![1])
/// false
fn pairs_sum_to_zero(l: Vec<isize>) -> bool {


    let mut set = std::collections::HashSet::new();
    for &i in &l {
        if set.contains(&i) {
            return true;
        }
        set.insert(-i);
    }
    false}

fn main() {
    let candidate = pairs_sum_to_zero;
    assert_eq!(candidate(vec![1, 3, 5, 0]), false);
    assert_eq!(candidate(vec![1, 3, -2, 1]), false);
    assert_eq!(candidate(vec![1, 2, 3, 7]), false);
    assert_eq!(candidate(vec![2, 4, -5, 3, 5, 7]), true);
    assert_eq!(candidate(vec![1]), false);
    assert_eq!(candidate(vec![-3, 9, -1, 3, 2, 30]), true);
    assert_eq!(candidate(vec![-3, 9, -1, 3, 2, 31]), true);
    assert_eq!(candidate(vec![-3, 9, -1, 4, 2, 30]), false);
    assert_eq!(candidate(vec![-3, 9, -1, 4, 2, 31]), false);
}

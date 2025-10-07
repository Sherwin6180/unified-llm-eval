/// Given a vector of numbers, return whether or not they are sorted
/// in ascending order. If vector has more than 1 duplicate of the same
/// number, return false. Assume no negative numbers and only integers.
/// Examples
/// >>> is_sorted(vec![5])
/// true
/// >>> is_sorted(vec![1, 2, 3, 4, 5])
/// true
/// >>> is_sorted(vec![1, 3, 2, 4, 5])
/// false
/// >>> is_sorted(vec![1, 2, 3, 4, 5, 6])
/// true
/// >>> is_sorted(vec![1, 2, 3, 4, 5, 6, 7])
/// true
/// >>> is_sorted(vec![1, 3, 2, 4, 5, 6, 7])
/// false
/// >>> is_sorted(vec![1, 2, 2, 3, 3, 4])
/// true
/// >>> is_sorted(vec![1, 2, 2, 2, 3, 4])
/// false
fn is_sorted(lst: Vec<isize>) -> bool {


    let mut last = None;
    for &n in lst.iter() {
        if last.is_some() && n < last.unwrap() {
            return false;
        }
        last = Some(n);
    }
    true}

fn main() {
    let candidate = is_sorted;
    assert_eq!(candidate(vec![5]), true);
    assert_eq!(candidate(vec![1, 2, 3, 4, 5]), true);
    assert_eq!(candidate(vec![1, 3, 2, 4, 5]), false);
    assert_eq!(candidate(vec![1, 2, 3, 4, 5, 6]), true);
    assert_eq!(candidate(vec![1, 2, 3, 4, 5, 6, 7]), true);
    assert_eq!(candidate(vec![1, 3, 2, 4, 5, 6, 7]), false);
    assert_eq!(candidate(Vec::<isize>::new()), true);
    assert_eq!(candidate(vec![1]), true);
    assert_eq!(candidate(vec![3, 2, 1]), false);
    assert_eq!(candidate(vec![1, 2, 2, 2, 3, 4]), false);
    assert_eq!(candidate(vec![1, 2, 3, 3, 3, 4]), false);
    assert_eq!(candidate(vec![1, 2, 2, 3, 3, 4]), true);
    assert_eq!(candidate(vec![1, 2, 3, 4]), true);
}

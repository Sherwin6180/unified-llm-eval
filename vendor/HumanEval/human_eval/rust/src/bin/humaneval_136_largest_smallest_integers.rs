/// Create a function that returns a tuple (a, b), where 'a' is
/// the largest of negative integers, and 'b' is the smallest
/// of positive integers in a vector.
/// If there is no negative or positive integers, return them as None.
/// Examples:
/// >>> largest_smallest_integers(vec![2, 4, 1, 3, 5, 7])
/// (None, Some(1))
/// >>> largest_smallest_integers(vec![])
/// (None, None)
/// >>> largest_smallest_integers(vec![0])
/// (None, None)
fn largest_smallest_integers(lst: Vec<isize>) -> (Option<isize>, Option<isize>) {


    let mut largest_negative = None;
    let mut smallest_positive = None;

    for &num in lst.iter() {
        if num < 0 && (largest_negative.is_none() || num > largest_negative.unwrap()) {
            largest_negative = Some(num);
        } else if num > 0 && (smallest_positive.is_none() || num < smallest_positive.unwrap()) {
            smallest_positive = Some(num);
        }
    }

    (largest_negative, smallest_positive)}

fn main() {
    let candidate = largest_smallest_integers;
    assert_eq!(candidate(vec![2, 4, 1, 3, 5, 7]), (None, Some(1)));
    assert_eq!(candidate(vec![2, 4, 1, 3, 5, 7, 0]), (None, Some(1)));
    assert_eq!(candidate(vec![1, 3, 2, 4, 5, 6, -2]), (Some(-2), Some(1)));
    assert_eq!(candidate(vec![4, 5, 3, 6, 2, 7, -7]), (Some(-7), Some(2)));
    assert_eq!(candidate(vec![7, 3, 8, 4, 9, 2, 5, -9]), (Some(-9), Some(2)));
    assert_eq!(candidate(Vec::<isize>::new()), (None, None));
    assert_eq!(candidate(vec![0]), (None, None));
    assert_eq!(candidate(vec![-1, -3, -5, -6]), (Some(-1), None));
    assert_eq!(candidate(vec![-1, -3, -5, -6, 0]), (Some(-1), None));
    assert_eq!(candidate(vec![-6, -4, -4, -3, 1]), (Some(-3), Some(1)));
    assert_eq!(candidate(vec![-6, -4, -4, -3, -100, 1]), (Some(-3), Some(1)));
}

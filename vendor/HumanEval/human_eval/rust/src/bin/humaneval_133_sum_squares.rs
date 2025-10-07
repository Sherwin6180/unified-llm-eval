/// You are given a vector of numbers.
/// You need to return the sum of squared numbers in the given vector,
/// round each element in the vector to the upper int(Ceiling) first.
/// Examples:
/// >>> lst(vec![1.0, 2.0, 3.0])
/// 14
/// >>> lst(vec![1.0, 4.0, 9.0])
/// 98
/// >>> lst(vec![1.0, 3.0, 5.0, 7.0])
/// 84
/// >>> lst(vec![1.4, 4.2, 0.0])
/// 29
/// >>> lst(vec![-2.4, 1.0, 1.0])
/// 6
fn sum_squares(lst: Vec<f64>) -> isize {


    lst.iter()
        .map(|x| (x.ceil() as isize).pow(2))
        .sum()}

fn main() {
    let candidate = sum_squares;
    assert_eq!(candidate(vec![1.0, 2.0, 3.0]), 14);
    assert_eq!(candidate(vec![1.0, 2.0, 3.0]), 14);
    assert_eq!(candidate(vec![1.0, 3.0, 5.0, 7.0]), 84);
    assert_eq!(candidate(vec![1.4, 4.2, 0.0]), 29);
    assert_eq!(candidate(vec![-2.4, 1.0, 1.0]), 6);
    assert_eq!(candidate(vec![100.0, 1.0, 15.0, 2.0]), 10230);
    assert_eq!(candidate(vec![10000.0, 10000.0]), 200000000);
    assert_eq!(candidate(vec![-1.4, 4.6, 6.3]), 75);
    assert_eq!(candidate(vec![-1.4, 17.9, 18.9, 19.9]), 1086);
    assert_eq!(candidate(vec![0.0]), 0);
    assert_eq!(candidate(vec![-1.0]), 1);
    assert_eq!(candidate(vec![-1.0, 1.0, 0.0]), 2);
}

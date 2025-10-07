/// Given a vector of numbers, return the sum of squares of the numbers
/// in the vector that are odd. Ignore numbers that are negative or not integers.
/// >>> double_the_difference(vec![1, 3, 2, 0])
/// 10
/// >>> double_the_difference(vec![-1, -2, 0])
/// 0
/// >>> double_the_difference(vec![9, -2])
/// 81
/// >>> double_the_difference(vec![0])
/// 0
/// If the input vector is empty, return 0.
fn double_the_difference(lst: Vec<f64>) -> isize {


    let mut sum = 0;
    for &num in lst.iter() {
        if num.is_integer() && num > 0 && num % 2_f64 != 0.0 {
            sum += num as isize * num as isize;
        }
    }
    sum}

fn main() {
    let candidate = double_the_difference;
    assert_eq!(candidate(Vec::<f64>::new()), 0);
    assert_eq!(candidate(vec![5.0, 4.0]), 25);
    assert_eq!(candidate(vec![0.1, 0.2, 0.3]), 0);
    assert_eq!(candidate(vec![-10.0, -20.0, -30.0]), 0);
    assert_eq!(candidate(vec![-1.0, -2.0, 8.0]), 0);
    assert_eq!(candidate(vec![0.2, 3.0, 5.0]), 34);
    assert_eq!(candidate(vec![-9.0, -7.0, -5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 7.0, 9.0]), 165);
}

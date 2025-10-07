/// Check if in given vector of numbers, are any two numbers closer to each other than
/// given threshold.
/// >>> has_close_elements(vec![1.0, 2.0, 3.0], 0.5)
/// false
/// >>> has_close_elements(vec![1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
/// true
fn has_close_elements(numbers: Vec<f64>, threshold: f64) -> bool {


    let mut last_number = numbers[0];
    for &number in numbers.iter().skip(1) {
        if (number - last_number).abs() < threshold {
            return true;
        }
        last_number = number;
    }
    false}

fn main() {
    let candidate = has_close_elements;
    assert_eq!(candidate(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3), true);
    assert_eq!(candidate(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05), false);
    assert_eq!(candidate(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.95), true);
    assert_eq!(candidate(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.8), false);
    assert_eq!(candidate(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1), true);
    assert_eq!(candidate(vec![1.1, 2.2, 3.1, 4.1, 5.1], 1.0), true);
    assert_eq!(candidate(vec![1.1, 2.2, 3.1, 4.1, 5.1], 0.5), false);
}

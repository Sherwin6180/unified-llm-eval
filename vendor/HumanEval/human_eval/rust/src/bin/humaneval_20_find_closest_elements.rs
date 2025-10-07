/// From a supplied vector of numbers (of length at least two) select and return two that are the closest to each
/// other and return them in order (smaller number, larger number).
/// >>> find_closest_elements(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
/// (2.0, 2.2)
/// >>> find_closest_elements(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
/// (2.0, 2.0)
fn find_closest_elements(numbers: Vec<f64>) -> (f64, f64) {


    let mut numbers = numbers;
    numbers.sort_unstable();
    let mut min_diff = f64::INFINITY;
    let mut result = (0.0, 0.0);
    for i in 1..numbers.len() {
        let diff = numbers[i] - numbers[i - 1];
        if diff < min_diff {
            min_diff = diff;
            result = (numbers[i - 1], numbers[i]);
        }
    }
    result}

fn main() {
    let candidate = find_closest_elements;
    assert_eq!(candidate(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2]), (3.9, 4.0));
    assert_eq!(candidate(vec![1.0, 2.0, 5.9, 4.0, 5.0]), (5.0, 5.9));
    assert_eq!(candidate(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.2]), (2.0, 2.2));
    assert_eq!(candidate(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0]), (2.0, 2.0));
    assert_eq!(candidate(vec![1.1, 2.2, 3.1, 4.1, 5.1]), (2.2, 3.1));
}

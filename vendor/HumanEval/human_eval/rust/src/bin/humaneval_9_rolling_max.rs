/// From a given vector of integers, generate a vector of rolling maximum element found until given moment
/// in the sequence.
/// >>> rolling_max(vec![1, 2, 3, 2, 3, 4, 2])
/// vec![1, 2, 3, 3, 3, 4, 4]
fn rolling_max(numbers: Vec<isize>) -> Vec<isize> {


    let mut result = Vec::new();
    let mut max = numbers[0];
    result.push(max);
    for &number in numbers.iter().skip(1) {
        max = max.max(number);
        result.push(max);
    }
    result}

fn main() {
    let candidate = rolling_max;
    assert_eq!(candidate(Vec::<isize>::new()), Vec::<isize>::new());
    assert_eq!(candidate(vec![1, 2, 3, 4]), vec![1, 2, 3, 4]);
    assert_eq!(candidate(vec![4, 3, 2, 1]), vec![4, 4, 4, 4]);
    assert_eq!(candidate(vec![3, 2, 3, 100, 3]), vec![3, 3, 3, 100, 100]);
}

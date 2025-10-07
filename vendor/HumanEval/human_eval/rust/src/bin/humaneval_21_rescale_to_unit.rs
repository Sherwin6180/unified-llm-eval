/// Given vector of numbers (of at least two elements), apply a linear transform to that vector,
/// such that the smallest number will become 0 and the largest will become 1
/// >>> rescale_to_unit(vec![1.0, 2.0, 3.0, 4.0, 5.0])
/// vec![0.0, 0.25, 0.5, 0.75, 1.0]
fn rescale_to_unit(numbers: Vec<f64>) -> Vec<f64> {


    let min = *numbers.iter().min().unwrap();
    let max = *numbers.iter().max().unwrap();
    let range = max - min;

    numbers.into_iter()
        .map(|n| (n - min) / range)
        .collect()}

fn main() {
    let candidate = rescale_to_unit;
    assert_eq!(candidate(vec![2.0, 49.9]), vec![0.0, 1.0]);
    assert_eq!(candidate(vec![100.0, 49.9]), vec![1.0, 0.0]);
    assert_eq!(candidate(vec![1.0, 2.0, 3.0, 4.0, 5.0]), vec![0.0, 0.25, 0.5, 0.75, 1.0]);
    assert_eq!(candidate(vec![2.0, 1.0, 5.0, 3.0, 4.0]), vec![0.25, 0.0, 1.0, 0.5, 0.75]);
    assert_eq!(candidate(vec![12.0, 11.0, 15.0, 13.0, 14.0]), vec![0.25, 0.0, 1.0, 0.5, 0.75]);
}

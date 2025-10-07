/// Given a vector of positive integers x. return a sorted vector of all 
/// elements that hasn't any even digit.
/// Note: Returned vector should be sorted in increasing order.
/// For example:
/// >>> unique_digits(vec![15, 33, 1422, 1])
/// vec![1, 15, 33]
/// >>> unique_digits(vec![152, 323, 1422, 10])
/// Vec::<isize>::new()
fn unique_digits(x: Vec<isize>) -> Vec<isize> {


    let mut result = Vec::new();
    for i in x {
        if i.to_string().chars().all(|c| c.to_digit(10).unwrap() % 2 != 0) {
            result.push(i);
        }
    }
    result.sort();
    result}

fn main() {
    let candidate = unique_digits;
    assert_eq!(candidate(vec![15, 33, 1422, 1]), vec![1, 15, 33]);
    assert_eq!(candidate(vec![152, 323, 1422, 10]), Vec::<isize>::new());
    assert_eq!(candidate(vec![12345, 2033, 111, 151]), vec![111, 151]);
    assert_eq!(candidate(vec![135, 103, 31]), vec![31, 135]);
}

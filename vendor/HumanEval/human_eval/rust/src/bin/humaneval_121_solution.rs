/// Given a non-empty vector of integers, return the sum of all of the odd elements that are in even positions.
/// Examples
/// >>> solution(vec![5, 8, 7, 1])
/// 12
/// >>> solution(vec![3, 3, 3, 3, 3])
/// 9
/// >>> solution(vec![30, 13, 24, 321])
/// 0
fn solution(lst: Vec<isize>) -> isize {


    lst.iter()
        .enumerate()
        .filter(|&(i, &n)| i % 2 == 0 && n % 2 != 0)
        .map(|(_, &n)| n)
        .sum()}

fn main() {
    let candidate = solution;
    assert_eq!(candidate(vec![5, 8, 7, 1]), 12);
    assert_eq!(candidate(vec![3, 3, 3, 3, 3]), 9);
    assert_eq!(candidate(vec![30, 13, 24, 321]), 0);
    assert_eq!(candidate(vec![5, 9]), 5);
    assert_eq!(candidate(vec![2, 4, 8]), 0);
    assert_eq!(candidate(vec![30, 13, 23, 32]), 23);
    assert_eq!(candidate(vec![3, 13, 2, 9]), 3);
}

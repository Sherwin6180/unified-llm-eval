/// You are given two intervals,
/// where each interval is a pair of integers. For example, interval = (start, end) = (1, 2).
/// The given intervals are closed which means that the interval (start, end)
/// includes both start and end.
/// For each given interval, it is assumed that its start is less or equal its end.
/// Your task is to determine whether the length of intersection of these two 
/// intervals is a prime number.
/// Example, the intersection of the intervals (1, 3), (2, 4) is (2, 3)
/// which its length is 1, which not a prime number.
/// If the length of the intersection is a prime number, return "YES",
/// otherwise, return "NO".
/// If the two intervals don't intersect, return "NO".
/// [input/output] samples:
/// >>> intersection((1, 2), (2, 3))
/// String::from("NO")
/// >>> intersection((-1, 1), (0, 4))
/// String::from("NO")
/// >>> intersection((-3, -1), (-5, 5))
/// String::from("YES")
fn intersection(interval1: (isize, isize), interval2: (isize, isize)) -> String {


    let (mut start, mut end) = (std::cmp::max(interval1.0, interval2.0), std::cmp::min(interval1.1, interval2.1));
    if start > end {
        return String::from("NO");
    }
    let length = end - start + 1;
    if length < 2 {
        return String::from("NO");
    }
    let mut is_prime = true;
    for i in 2..(length as f64).sqrt() as isize + 1 {
        if length % i == 0 {
            is_prime = false;
            break;
        }
    }
    if is_prime {
        String::from("YES")
    } else {
        String::from("NO")
    }}

fn main() {
    let candidate = intersection;
    assert_eq!(candidate((1, 2), (2, 3)), String::from("NO"));
    assert_eq!(candidate((-1, 1), (0, 4)), String::from("NO"));
    assert_eq!(candidate((-3, -1), (-5, 5)), String::from("YES"));
    assert_eq!(candidate((-2, 2), (-4, 0)), String::from("YES"));
    assert_eq!(candidate((-11, 2), (-1, -1)), String::from("NO"));
    assert_eq!(candidate((1, 2), (3, 5)), String::from("NO"));
    assert_eq!(candidate((1, 2), (1, 2)), String::from("NO"));
    assert_eq!(candidate((-2, -2), (-3, -2)), String::from("NO"));
}

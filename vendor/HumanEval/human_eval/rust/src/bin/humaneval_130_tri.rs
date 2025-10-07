/// Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in 
/// the last couple centuries. However, what people don't know is Tribonacci sequence.
/// Tribonacci sequence is defined by the recurrence:
/// tri(1) = 3
/// tri(n) = 1 + n / 2, if n is even.
/// tri(n) =  tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
/// For example:
/// tri(2) = 1 + (2 / 2) = 2
/// tri(4) = 3
/// tri(3) = tri(2) + tri(1) + tri(4)
/// = 2 + 3 + 3 = 8 
/// You are given a non-negative integer number n, you have to a return a vector of the 
/// first n + 1 numbers of the Tribonacci sequence.
/// Examples:
/// >>> tri(3)
/// vec![1, 3, 2, 8]
fn tri(n: isize) -> Vec<isize> {


    let mut result = vec![0; (n + 1) as usize];
    if n >= 1 {
        result[1] = 3;
    }
    if n >= 2 {
        result[2] = 2;
    }
    if n >= 3 {
        result[3] = 8;
    }
    for i in 4..=n {
        if i % 2 == 0 {
            result[i as usize] = 1 + i / 2;
        } else {
            result[i as usize] = result[(i - 1) as usize] + result[(i - 2) as usize] + result[(i - 3) as usize];
        }
    }
    result.into_iter().skip(1).collect()}

fn main() {
    let candidate = tri;
    assert_eq!(candidate(3), vec![1, 3, 2, 8]);
    assert_eq!(candidate(4), vec![1, 3, 2, 8, 3]);
    assert_eq!(candidate(5), vec![1, 3, 2, 8, 3, 15]);
    assert_eq!(candidate(6), vec![1, 3, 2, 8, 3, 15, 4]);
    assert_eq!(candidate(7), vec![1, 3, 2, 8, 3, 15, 4, 24]);
    assert_eq!(candidate(8), vec![1, 3, 2, 8, 3, 15, 4, 24, 5]);
    assert_eq!(candidate(9), vec![1, 3, 2, 8, 3, 15, 4, 24, 5, 35]);
    assert_eq!(candidate(20), vec![1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6, 48, 7, 63, 8, 80, 9, 99, 10, 120, 11]);
    assert_eq!(candidate(0), vec![1]);
    assert_eq!(candidate(1), vec![1, 3]);
}

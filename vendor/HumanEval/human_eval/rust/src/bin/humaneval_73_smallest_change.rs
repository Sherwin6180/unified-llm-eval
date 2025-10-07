/// Given a vector arr of integers, find the minimum number of elements that
/// need to be changed to make the vector palindromic. A palindromic vector is a vector that
/// is read the same backwards and forwards. In one change, you can change one element to any other element.
/// For example:
/// >>> smallest_change(vec![1, 2, 3, 5, 4, 7, 9, 6])
/// 4
/// >>> smallest_change(vec![1, 2, 3, 4, 3, 2, 2])
/// 1
/// >>> smallest_change(vec![1, 2, 3, 2, 1])
/// 0
fn smallest_change(arr: Vec<isize>) -> isize {


    let n = arr.len();
    let mut dp = vec![vec![0; n]; n];
    for i in 0..n {
        dp[i][i] = 0;
    }
    for len in 2..=n {
        for i in 0..=n - len {
            let j = i + len - 1;
            if arr[i] == arr[j] {
                dp[i][j] = dp[i + 1][j - 1];
            } else {
                dp[i][j] = 1 + std::cmp::min(dp[i + 1][j], dp[i][j - 1]);
            }
        }
    }
    dp[0][n - 1]}

fn main() {
    let candidate = smallest_change;
    assert_eq!(candidate(vec![1, 2, 3, 5, 4, 7, 9, 6]), 4);
    assert_eq!(candidate(vec![1, 2, 3, 4, 3, 2, 2]), 1);
    assert_eq!(candidate(vec![1, 4, 2]), 1);
    assert_eq!(candidate(vec![1, 4, 4, 2]), 1);
    assert_eq!(candidate(vec![1, 2, 3, 2, 1]), 0);
    assert_eq!(candidate(vec![3, 1, 1, 3]), 0);
    assert_eq!(candidate(vec![1]), 0);
    assert_eq!(candidate(vec![0, 1]), 1);
}

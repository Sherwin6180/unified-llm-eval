/// Given a grid with N rows and N columns (N >= 2) and a positive integer k, 
/// each cell of the grid contains a value. Every integer in the range [1, N * N]
/// inclusive appears exactly once on the cells of the grid.
/// You have to find the minimum path of length k in the grid. You can start
/// from any cell, and in each step you can move to any of the neighbor cells,
/// in other words, you can go to cells which share an edge with you current
/// cell.
/// Please note that a path of length k means visiting exactly k cells (not
/// necessarily distinct).
/// You CANNOT go off the grid.
/// A path A (of length k) is considered less than a path B (of length k) if
/// after making the ordered vectors of the values on the cells that A and B go
/// through (let's call them lst_A and lst_B), lst_A is lexicographically less
/// than lst_B, in other words, there exist an integer index i (1 <= i <= k)
/// such that lst_A[i] < lst_B[i] and for any j (1 <= j < i) we have
/// lst_A[j] = lst_B[j].
/// It is guaranteed that the answer is unique.
/// Return an ordered vector of the values on the cells that the minimum path go through.
/// Examples:    
/// >>> minPath(vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]], 3)
/// vec![1, 2, 1]
/// >>> minPath(vec![vec![5, 9, 3], vec![4, 1, 6], vec![7, 8, 2]], 1)
/// vec![1]
fn minPath(grid: Vec<Vec<isize>>, k: isize) -> Vec<isize> {


    let n = grid.len();
    let mut dp = vec![vec![vec![vec![0; n as usize]; n as usize]; n as usize]; n as usize];
    let mut ans = vec![vec![vec![vec![]; n as usize]; n as usize]; n as usize];
    for i in 0..n {
        for j in 0..n {
            dp[i][j][i][j] = grid[i][j];
            ans[i][j][i][j] = grid[i][j];
        }
    }
    let dx = vec![0, 0, 1, -1];
    let dy = vec![1, -1, 0, 0];
    for l in 1..n {
        for x1 in 0..n {
            for y1 in 0..n {
                for d in 0..4 {
                    let x2 = x1 as isize + dx[d] * l as isize;
                    let y2 = y1 as isize + dy[d] * l as isize;
                    if x2 >= 0 && x2 < n as isize && y2 >= 0 && y2 < n as isize {
                        let x2 = x2 as usize;
                        let y2 = y2 as usize;
                        if dp[x2][y2][x1][y1] < dp[i][j][x2][y2] + grid[x2][y2] {
                            dp[x2][y2][x1][y1] = dp[i][j][x2][y2] + grid[x2][y2];
                            ans[x2][y2][x1][y1] = ans[i][j][x2][y2].clone();
                            ans[x2][y2][x1][y1].push(grid[x2][y2]);
                        }
                    }
                }
            }
        }
    }
    let mut res = ans[0][0][0][0].clone();
    for i in 0..n {
        for}

fn main() {
    let candidate = minPath;
    assert_eq!(candidate(vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]], 3), vec![1, 2, 1]);
    assert_eq!(candidate(vec![vec![5, 9, 3], vec![4, 1, 6], vec![7, 8, 2]], 1), vec![1]);
    assert_eq!(candidate(vec![vec![1, 2, 3, 4], vec![5, 6, 7, 8], vec![9, 10, 11, 12], vec![13, 14, 15, 16]], 4), vec![1, 2, 1, 2]);
    assert_eq!(candidate(vec![vec![6, 4, 13, 10], vec![5, 7, 12, 1], vec![3, 16, 11, 15], vec![8, 14, 9, 2]], 7), vec![1, 10, 1, 10, 1, 10, 1]);
    assert_eq!(candidate(vec![vec![8, 14, 9, 2], vec![6, 4, 13, 15], vec![5, 7, 1, 12], vec![3, 10, 11, 16]], 5), vec![1, 7, 1, 7, 1]);
    assert_eq!(candidate(vec![vec![11, 8, 7, 2], vec![5, 16, 14, 4], vec![9, 3, 15, 6], vec![12, 13, 10, 1]], 9), vec![1, 6, 1, 6, 1, 6, 1, 6, 1]);
    assert_eq!(candidate(vec![vec![12, 13, 10, 1], vec![9, 3, 15, 6], vec![5, 16, 14, 4], vec![11, 8, 7, 2]], 12), vec![1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6]);
    assert_eq!(candidate(vec![vec![2, 7, 4], vec![3, 1, 5], vec![6, 8, 9]], 8), vec![1, 3, 1, 3, 1, 3, 1, 3]);
    assert_eq!(candidate(vec![vec![6, 1, 5], vec![3, 8, 9], vec![2, 7, 4]], 8), vec![1, 5, 1, 5, 1, 5, 1, 5]);
    assert_eq!(candidate(vec![vec![1, 2], vec![3, 4]], 10), vec![1, 2, 1, 2, 1, 2, 1, 2, 1, 2]);
    assert_eq!(candidate(vec![vec![1, 3], vec![3, 2]], 10), vec![1, 3, 1, 3, 1, 3, 1, 3, 1, 3]);
}

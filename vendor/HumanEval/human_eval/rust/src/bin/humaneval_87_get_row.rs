/// You are given a 2 dimensional data, as a nested vectors,
/// which is similar to matrix, however, unlike matrices,
/// each row may contain a different number of columns.
/// Given lst, and integer x, find integers x in the vector,
/// and return vector of tuples, [(x1, y1), (x2, y2) ...] such that
/// each tuple is a coordinate - (row, columns), starting with 0.
/// Sort coordinates initially by rows in ascending order.
/// Also, sort coordinates of the row by columns in descending order.
/// Examples:
/// >>> get_row(vec![vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 1, 6], vec![1, 2, 3, 4, 5, 1]], 1)
/// vec![(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
/// >>> get_row(vec![], 1)
/// Vec::<(isize, isize)>::new()
/// >>> get_row(vec![vec![], vec![1], vec![1, 2, 3]], 3)
/// vec![(2, 2)]
fn get_row(lst: Vec<Vec<isize>>, x: isize) -> Vec<(isize, isize)> {


    let mut result = Vec::<(isize, isize)>::new();
    for (i, row) in lst.iter().enumerate() {
        for (j, &item) in row.iter().enumerate().rev() {
            if item == x {
                result.push((i as isize, j as isize));
            }
        }
    }
    result.sort_by(|a, b| a.cmp(&b).then(b.1.cmp(&a.1)));
    result}

fn main() {
    let candidate = get_row;
    assert_eq!(candidate(vec![vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 1, 6], vec![1, 2, 3, 4, 5, 1]], 1), vec![(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]);
    assert_eq!(candidate(vec![vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6]], 2), vec![(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]);
    assert_eq!(candidate(vec![vec![1, 2, 3, 4, 5, 6], vec![1, 2, 3, 4, 5, 6], vec![1, 1, 3, 4, 5, 6], vec![1, 2, 1, 4, 5, 6], vec![1, 2, 3, 1, 5, 6], vec![1, 2, 3, 4, 1, 6], vec![1, 2, 3, 4, 5, 1]], 1), vec![(0, 0), (1, 0), (2, 1), (2, 0), (3, 2), (3, 0), (4, 3), (4, 0), (5, 4), (5, 0), (6, 5), (6, 0)]);
    assert_eq!(candidate(Vec::<Vec<isize>>::new(), 1), Vec::<(isize, isize)>::new());
    assert_eq!(candidate(vec![vec![1]], 2), Vec::<(isize, isize)>::new());
    assert_eq!(candidate(vec![vec![], vec![1], vec![1, 2, 3]], 3), vec![(2, 2)]);
}

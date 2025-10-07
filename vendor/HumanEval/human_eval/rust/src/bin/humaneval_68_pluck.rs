/// "Given a vector representing a branch of a tree that has non-negative integer nodes
/// your task is to pluck one of the nodes and return it.
/// The plucked node should be the node with the smallest even value.
/// If multiple nodes with the same smallest even value are found return the node that has smallest index.
/// The plucked node should be returned in a vector, [ smalest_value, its index ],
/// If there are no even values or the given vector is empty, return [].
/// Example 1:
/// >>> pluck(vec![4, 2, 3])
/// vec![2, 1]
/// Explanation: 2 has the smallest even value, and 2 has the smallest index.
/// Example 2:
/// >>> pluck(vec![1, 2, 3])
/// vec![2, 1]
/// Explanation: 2 has the smallest even value, and 2 has the smallest index.
/// Example 3:
/// >>> pluck(vec![])
/// Vec::<isize>::new()
/// Example 4:
/// >>> pluck(vec![5, 0, 3, 0, 4, 2])
/// vec![0, 1]
/// Explanation: 0 is the smallest value, but  there are two zeros,
/// so we will choose the first zero, which has the smallest index.
/// Constraints:
/// * 1 <= nodes.length <= 10000
/// * 0 <= node.value
fn pluck(arr: Vec<isize>) -> Vec<isize> {


    let mut min_val = i64::MAX;
    let mut min_idx = -1;
    for (i, &x) in arr.iter().enumerate() {
        if x % 2 == 0 && x < min_val {
            min_val = x;
            min_idx = i;
        }
    }
    if min_idx == -1 {
        return vec![];
    }
    vec![min_val as isize, min_idx as isize]}

fn main() {
    let candidate = pluck;
    assert_eq!(candidate(vec![4, 2, 3]), vec![2, 1]);
    assert_eq!(candidate(vec![1, 2, 3]), vec![2, 1]);
    assert_eq!(candidate(Vec::<isize>::new()), Vec::<isize>::new());
    assert_eq!(candidate(vec![5, 0, 3, 0, 4, 2]), vec![0, 1]);
    assert_eq!(candidate(vec![1, 2, 3, 0, 5, 3]), vec![0, 3]);
    assert_eq!(candidate(vec![5, 4, 8, 4, 8]), vec![4, 1]);
    assert_eq!(candidate(vec![7, 6, 7, 1]), vec![6, 1]);
    assert_eq!(candidate(vec![7, 9, 7, 1]), Vec::<isize>::new());
}

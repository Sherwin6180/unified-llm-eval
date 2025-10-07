/// We have a vector 'arr' of N integers arr[1], arr[2], ..., arr[N].The
/// numbers in the vector will be randomly ordered. Your task is to determine if
/// it is possible to get a vector sorted in non-decreasing order by performing 
/// the following operation on the given vector:
/// You are allowed to perform right shift operation any number of times.
/// One right shift operation means shifting all elements of the vector by one
/// position in the right direction. The last element of the vector will be moved to
/// the starting position in the vector i.e. 0th index. 
/// If it is possible to obtain the sorted vector by performing the above operation
/// then return true else return false.
/// If the given vector is empty then return true.
/// Note: The given vector is guaranteed to have unique elements.
/// For Example:
/// >>> move_one_ball(vec![3, 4, 5, 1, 2])
/// true
/// Explanation: By performin 2 right shift operations, non-decreasing order can
/// be achieved for the given vector.
/// >>> move_one_ball(vec![3, 5, 4, 1, 2])
/// false
/// Explanation:It is not possible to get non-decreasing order for the given
/// vector by performing any number of right shift operations.
fn move_one_ball(arr: Vec<isize>) -> bool {


    let mut arr = arr;
    let n = arr.len();
    let mut min_val = arr[0];
    for i in 1..n {
        if arr[i] < min_val {
            return false;
        }
        min_val = arr[i];
    }
    return true;}

fn main() {
    let candidate = move_one_ball;
    assert_eq!(candidate(vec![3, 4, 5, 1, 2]), true);
    assert_eq!(candidate(vec![3, 5, 10, 1, 2]), true);
    assert_eq!(candidate(vec![4, 3, 1, 2]), false);
    assert_eq!(candidate(vec![3, 5, 4, 1, 2]), false);
    assert_eq!(candidate(Vec::<isize>::new()), true);
}

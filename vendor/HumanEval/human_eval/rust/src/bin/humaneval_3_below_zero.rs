/// You're given a vector of deposit and withdrawal operations on a bank account that starts with
/// zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
/// at that point function should return true. Otherwise it should return false.
/// >>> below_zero(vec![1, 2, 3])
/// false
/// >>> below_zero(vec![1, 2, -4, 5])
/// true
fn below_zero(operations: Vec<isize>) -> bool {


    let mut balance = 0;
    for operation in operations {
        balance += operation;
        if balance < 0 {
            return true;
        }
    }
    false}

fn main() {
    let candidate = below_zero;
    assert_eq!(candidate(Vec::<isize>::new()), false);
    assert_eq!(candidate(vec![1, 2, -3, 1, 2, -3]), false);
    assert_eq!(candidate(vec![1, 2, -4, 5, 6]), true);
    assert_eq!(candidate(vec![1, -1, 2, -2, 5, -5, 4, -4]), false);
    assert_eq!(candidate(vec![1, -1, 2, -2, 5, -5, 4, -5]), true);
    assert_eq!(candidate(vec![1, -2, 2, -2, 5, -5, 4, -4]), true);
}

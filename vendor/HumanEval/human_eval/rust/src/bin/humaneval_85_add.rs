/// Given a non-empty vector of integers lst. add the even elements that are at odd indices..
/// Examples:
/// >>> add(vec![4, 2, 6, 7])
/// 2
fn add(lst: Vec<isize>) -> isize {


    let mut sum = 0;
    for i in 1..lst.len() {
        if i % 2 != 0 && lst[i] % 2 == 0 {
            sum += lst[i];
        }
    }
    sum}

fn main() {
    let candidate = add;
    assert_eq!(candidate(vec![4, 88]), 88);
    assert_eq!(candidate(vec![4, 5, 6, 7, 2, 122]), 122);
    assert_eq!(candidate(vec![4, 0, 6, 7]), 0);
    assert_eq!(candidate(vec![4, 4, 6, 8]), 12);
}

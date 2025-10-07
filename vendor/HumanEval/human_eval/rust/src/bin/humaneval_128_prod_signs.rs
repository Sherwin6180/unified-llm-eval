/// You are given a vector arr of integers and you need to return
/// sum of magnitudes of integers multiplied by product of all signs
/// of each number in the vector, represented by 1, -1 or 0.
/// Note: return None for empty arr.
/// Example:
/// >>> prod_signs(vec![1, 2, 2, -4])
/// Some(9)
/// >>> prod_signs(vec![0, 1])
/// Some(0)
/// >>> prod_signs(vec![])
/// None
fn prod_signs(arr: Vec<isize>) -> Option<isize> {


    if arr.is_empty() {
        return None;
    }
    let mut sign = 1;
    let mut sum = 0;
    for &num in arr.iter() {
        if num == 0 {
            return Some(0);
        } else if num < 0 {
            sign *= -1;
        }
        sum += num.abs();
    }
    Some(sum * sign)}

fn main() {
    let candidate = prod_signs;
    assert_eq!(candidate(vec![1, 2, 2, -4]), Some(-9));
    assert_eq!(candidate(vec![0, 1]), Some(0));
    assert_eq!(candidate(vec![1, 1, 1, 2, 3, -1, 1]), Some(-10));
    assert_eq!(candidate(Vec::<isize>::new()), None);
    assert_eq!(candidate(vec![2, 4, 1, 2, -1, -1, 9]), Some(20));
    assert_eq!(candidate(vec![-1, 1, -1, 1]), Some(4));
    assert_eq!(candidate(vec![-1, 1, 1, 1]), Some(-4));
    assert_eq!(candidate(vec![-1, 1, 1, 0]), Some(0));
}

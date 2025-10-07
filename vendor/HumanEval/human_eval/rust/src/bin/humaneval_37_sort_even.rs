/// This function takes a vector l and returns a vector l' such that
/// l' is identical to l in the odd indicies, while its values at the even indicies are equal
/// to the values of the even indicies of l, but sorted.
/// >>> sort_even(vec![1, 2, 3])
/// vec![1, 2, 3]
/// >>> sort_even(vec![5, 6, 3, 4])
/// vec![3, 6, 5, 4]
fn sort_even(l: Vec<isize>) -> Vec<isize> {


    let mut even_indices: Vec<isize> = l.iter().enumerate()
        .filter(|&(i, _)| i % 2 == 0)
        .map(|(_, &val)| val)
        .collect();
    even_indices.sort();
    l.iter().enumerate()
        .map(|(i, val)| if i % 2 == 0 { even_indices.remove(0) } else { *val })
        .collect()}

fn main() {
    let candidate = sort_even;
    assert_eq!(candidate(vec![1, 2, 3]), vec![1, 2, 3]);
    assert_eq!(candidate(vec![5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]), vec![-10, 3, -5, 2, -3, 3, 5, 0, 9, 1, 123]);
    assert_eq!(candidate(vec![5, 8, -12, 4, 23, 2, 3, 11, 12, -10]), vec![-12, 8, 3, 4, 5, 2, 12, 11, 23, -10]);
}

/// Return sorted unique common elements for two vectors.
/// >>> common(vec![1, 4, 3, 34, 653, 2, 5], vec![5, 7, 1, 5, 9, 653, 121])
/// vec![1, 5, 653]
/// >>> common(vec![5, 3, 2, 8], vec![3, 2])
/// vec![2, 3]
fn common(l1: Vec<isize>, l2: Vec<isize>) -> Vec<isize> {


    let mut l1 = l1;
    let mut l2 = l2;
    l1.sort_unstable();
    l2.sort_unstable();
    let mut result = vec![];
    let mut i = 0;
    let mut j = 0;
    while i < l1.len() && j < l2.len() {
        if l1[i] == l2[j] {
            if result.is_empty() || result.last().unwrap() != &l1[i] {
                result.push(l1[i]);
            }
            i += 1;
            j += 1;
        } else if l1[i] < l2[j] {
            i += 1;
        } else {
            j += 1;
        }
    }
    result}

fn main() {
    let candidate = common;
    assert_eq!(candidate(vec![1, 4, 3, 34, 653, 2, 5], vec![5, 7, 1, 5, 9, 653, 121]), vec![1, 5, 653]);
    assert_eq!(candidate(vec![5, 3, 2, 8], vec![3, 2]), vec![2, 3]);
    assert_eq!(candidate(vec![4, 3, 2, 8], vec![3, 2, 4]), vec![2, 3, 4]);
    assert_eq!(candidate(vec![4, 3, 2, 8], Vec::<isize>::new()), Vec::<isize>::new());
}

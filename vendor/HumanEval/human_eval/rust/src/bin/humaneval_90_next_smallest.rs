/// You are given a vector of integers.
/// Write a function next_smallest() that returns the 2nd smallest element of the vector.
/// Return None if there is no such element.
/// >>> next_smallest(vec![1, 2, 3, 4, 5])
/// Some(2)
/// >>> next_smallest(vec![5, 1, 4, 3, 2])
/// Some(2)
/// >>> next_smallest(vec![])
/// None
/// >>> next_smallest(vec![1, 1])
/// None
fn next_smallest(lst: Vec<isize>) -> Option<isize> {


    let mut lst = lst;
    lst.sort_unstable();
    let mut smallest = lst.get(0)?;
    for &num in lst.iter().skip(1) {
        if num < smallest {
            return Some(num);
        }
    }
    None}

fn main() {
    let candidate = next_smallest;
    assert_eq!(candidate(vec![1, 2, 3, 4, 5]), Some(2));
    assert_eq!(candidate(vec![5, 1, 4, 3, 2]), Some(2));
    assert_eq!(candidate(Vec::<isize>::new()), None);
    assert_eq!(candidate(vec![1, 1]), None);
    assert_eq!(candidate(vec![1, 1, 1, 1, 0]), Some(1));
    assert_eq!(candidate(vec![1, 1]), None);
    assert_eq!(candidate(vec![-35, 34, 12, -45]), Some(-35));
}

/// In this problem, you will implement a function that takes two vectors of numbers,
/// and determines whether it is possible to perform an exchange of elements
/// between them to make lst1 a vector of only even numbers.
/// There is no limit on the number of exchanged elements between lst1 and lst2.
/// If it is possible to exchange elements between the lst1 and lst2 to make
/// all the elements of lst1 to be even, return "YES".
/// Otherwise, return "NO".
/// For example:
/// >>> exchange(vec![1, 2, 3, 4], vec![1, 2, 3, 4])
/// String::from("YES")
/// >>> exchange(vec![1, 2, 3, 4], vec![1, 5, 3, 4])
/// String::from("NO")
/// It is assumed that the input vectors will be non-empty.
fn exchange(lst1: Vec<isize>, lst2: Vec<isize>) -> String {


    let mut lst1 = lst1;
    let mut lst2 = lst2;
    let mut odd_lst1 = 0;
    let mut even_lst2 = 0;

    for i in lst1.iter() {
        if *i % 2 != 0 {
            odd_lst1 += 1;
        }
    }

    for i in lst2.iter() {
        if *i % 2 == 0 {
            even_lst2 += 1;
        }
    }

    if odd_lst1 <= even_lst2 {
        return String::from("YES");
    }

    String::from("NO")}

fn main() {
    let candidate = exchange;
    assert_eq!(candidate(vec![1, 2, 3, 4], vec![1, 2, 3, 4]), String::from("YES"));
    assert_eq!(candidate(vec![1, 2, 3, 4], vec![1, 5, 3, 4]), String::from("NO"));
    assert_eq!(candidate(vec![1, 2, 3, 4], vec![2, 1, 4, 3]), String::from("YES"));
    assert_eq!(candidate(vec![5, 7, 3], vec![2, 6, 4]), String::from("YES"));
    assert_eq!(candidate(vec![5, 7, 3], vec![2, 6, 3]), String::from("NO"));
    assert_eq!(candidate(vec![3, 2, 6, 1, 8, 9], vec![3, 5, 5, 1, 1, 1]), String::from("NO"));
    assert_eq!(candidate(vec![100, 200], vec![200, 200]), String::from("YES"));
}

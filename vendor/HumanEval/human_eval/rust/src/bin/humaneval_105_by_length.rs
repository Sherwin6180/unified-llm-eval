/// Given a vector of integers, sort the integers that are between 1 and 9 inclusive,
/// reverse the resulting vector, and then replace each digit by its corresponding name from
/// "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine".
/// For example:
/// >>> by_length(vec![2, 1, 1, 4, 5, 8, 2, 3])
/// vec![String::from("Eight"), String::from("Five"), String::from("Four"), String::from("Three"), String::from("Two"), String::from("Two"), String::from("One"), String::from("One")]
/// If the vector is empty, return an empty vector:
/// >>> by_length(vec![])
/// Vec::<String>::new()
/// If the vector has any strange number ignore it:
/// >>> by_length(vec![1, -1, 55])
/// vec![String::from("One")]
fn by_length(arr: Vec<isize>) -> Vec<String> {


    let mut result: Vec<String> = vec![];
    let num_names = vec![
        String::from("One"),
        String::from("Two"),
        String::from("Three"),
        String::from("Four"),
        String::from("Five"),
        String::from("Six"),
        String::from("Seven"),
        String::from("Eight"),
        String::from("Nine"),
    ];

    for &num in arr.iter() {
        if num > 0 && num < 10 {
            result.push(num_names[num as usize - 1].clone());
        }
    }

    result.sort_unstable_by_key(|s| s.len());
    result.reverse();
    result}

fn main() {
    let candidate = by_length;
    assert_eq!(candidate(vec![2, 1, 1, 4, 5, 8, 2, 3]), vec![String::from("Eight"), String::from("Five"), String::from("Four"), String::from("Three"), String::from("Two"), String::from("Two"), String::from("One"), String::from("One")]);
    assert_eq!(candidate(Vec::<isize>::new()), Vec::<String>::new());
    assert_eq!(candidate(vec![1, -1, 55]), vec![String::from("One")]);
    assert_eq!(candidate(vec![1, -1, 3, 2]), vec![String::from("Three"), String::from("Two"), String::from("One")]);
    assert_eq!(candidate(vec![9, 4, 8]), vec![String::from("Nine"), String::from("Eight"), String::from("Four")]);
}

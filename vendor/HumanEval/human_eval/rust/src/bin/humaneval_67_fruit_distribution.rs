/// In this task, you will be given a string that represents a number of apples and oranges 
/// that are distributed in a basket of fruit this basket contains 
/// apples, oranges, and mango fruits. Given the string that represents the total number of 
/// the oranges and apples and an integer that represent the total number of the fruits 
/// in the basket return the number of the mango fruits in the basket.
/// for examble:
/// >>> fruit_distribution(String::from("5 apples and 6 oranges"), 19)
/// 8
/// >>> fruit_distribution(String::from("0 apples and 1 oranges"), 3)
/// 2
/// >>> fruit_distribution(String::from("2 apples and 3 oranges"), 100)
/// 95
/// >>> fruit_distribution(String::from("100 apples and 1 oranges"), 120)
/// 19
fn fruit_distribution(s: String, n: isize) -> isize {


    let mut words = s.split_whitespace();
    let mut apples = 0;
    let mut oranges = 0;
    while let Some(word) = words.next() {
        match word.parse::<isize>() {
            Ok(num) => {
                if word.contains('a') {
                    apples = num;
                } else if word.contains('o') {
                    oranges = num;
                }
            }
            Err(_) => (),
        }
    }
    n - apples - oranges}

fn main() {
    let candidate = fruit_distribution;
    assert_eq!(candidate(String::from("5 apples and 6 oranges"), 19), 8);
    assert_eq!(candidate(String::from("5 apples and 6 oranges"), 21), 10);
    assert_eq!(candidate(String::from("0 apples and 1 oranges"), 3), 2);
    assert_eq!(candidate(String::from("1 apples and 0 oranges"), 3), 2);
    assert_eq!(candidate(String::from("2 apples and 3 oranges"), 100), 95);
    assert_eq!(candidate(String::from("2 apples and 3 oranges"), 5), 0);
    assert_eq!(candidate(String::from("1 apples and 100 oranges"), 120), 19);
}

/// Given a vector of strings, where each string consists of only digits, return a vector.
/// Each element i of the output should be "the number of odd elements in the
/// string i of the input." where all the i's should be replaced by the number
/// of odd digits in the i'th string of the input.
/// >>> odd_count(vec![String::from("1234567")])
/// vec![String::from("the number of odd elements 4n the str4ng 4 of the 4nput.")]
/// >>> odd_count(vec![String::from("3"), String::from("11111111")])
/// vec![String::from("the number of odd elements 1n the str1ng 1 of the 1nput."), String::from("the number of odd elements 8n the str8ng 8 of the 8nput.")]
fn odd_count(lst: Vec<String>) -> Vec<String> {


    let mut result = vec![];
    for s in lst {
        let mut count = 0;
        for c in s.chars() {
            if c.to_digit(10).unwrap() % 2 == 1 {
                count += 1;
            }
        }
        let mut new_s = s.clone();
        for (i, c) in new_s.chars().enumerate() {
            if c.is_digit(10) && c.to_digit(10).unwrap() % 2 == 1 {
                new_s.replace_range(i..i+1, &count.to_string());
            }
        }
        result.push(new_s);
    }
    result}

fn main() {
    let candidate = odd_count;
    assert_eq!(candidate(vec![String::from("1234567")]), vec![String::from("the number of odd elements 4n the str4ng 4 of the 4nput.")]);
    assert_eq!(candidate(vec![String::from("3"), String::from("11111111")]), vec![String::from("the number of odd elements 1n the str1ng 1 of the 1nput."), String::from("the number of odd elements 8n the str8ng 8 of the 8nput.")]);
    assert_eq!(candidate(vec![String::from("271"), String::from("137"), String::from("314")]), vec![String::from("the number of odd elements 2n the str2ng 2 of the 2nput."), String::from("the number of odd elements 3n the str3ng 3 of the 3nput."), String::from("the number of odd elements 2n the str2ng 2 of the 2nput.")]);
}

/// Input is a space-delimited string of numberals from 'zero' to 'nine'.
/// Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
/// Return the string with numbers sorted from smallest to largest
/// >>> sort_numbers(String::from("three one five"))
/// String::from("one three five")
fn sort_numbers(numbers: String) -> String {


    let mut num_vec: Vec<&str> = numbers.split_whitespace().collect();
    num_vec.sort_by_key(|k| {
        match k {
            "zero" => 0,
            "one" => 1,
            "two" => 2,
            "three" => 3,
            "four" => 4,
            "five" => 5,
            "six" => 6,
            "seven" => 7,
            "eight" => 8,
            "nine" => 9,
            _ => panic!("Invalid number"),
        }
    });
    num_vec.join(" ")}

fn main() {
    let candidate = sort_numbers;
    assert_eq!(candidate(String::from("")), String::from(""));
    assert_eq!(candidate(String::from("three")), String::from("three"));
    assert_eq!(candidate(String::from("three five nine")), String::from("three five nine"));
    assert_eq!(candidate(String::from("five zero four seven nine eight")), String::from("zero four five seven eight nine"));
    assert_eq!(candidate(String::from("six five four three two one zero")), String::from("zero one two three four five six"));
}

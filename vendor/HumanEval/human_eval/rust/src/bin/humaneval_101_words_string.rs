/// You will be given a string of words separated by commas or spaces. Your task is
/// to split the string into words and return a vector of the words.
/// For example:
/// >>> words_string(String::from("Hi, my name is John"))
/// vec![String::from("Hi"), String::from("my"), String::from("name"), String::from("is"), String::from("John")]
/// >>> words_string(String::from("One, two, three, four, five, six"))
/// vec![String::from("One"), String::from("two"), String::from("three"), String::from("four"), String::from("five"), String::from("six")]
fn words_string(s: String) -> Vec<String> {


    let mut words = s.split(|c: char| c == ' ' || c == ',');
    words.filter(|word| !word.is_empty()).collect()}

fn main() {
    let candidate = words_string;
    assert_eq!(candidate(String::from("Hi, my name is John")), vec![String::from("Hi"), String::from("my"), String::from("name"), String::from("is"), String::from("John")]);
    assert_eq!(candidate(String::from("One, two, three, four, five, six")), vec![String::from("One"), String::from("two"), String::from("three"), String::from("four"), String::from("five"), String::from("six")]);
    assert_eq!(candidate(String::from("Hi, my name")), vec![String::from("Hi"), String::from("my"), String::from("name")]);
    assert_eq!(candidate(String::from("One,, two, three, four, five, six,")), vec![String::from("One"), String::from("two"), String::from("three"), String::from("four"), String::from("five"), String::from("six")]);
    assert_eq!(candidate(String::from("")), Vec::<String>::new());
    assert_eq!(candidate(String::from("ahmed     , gamal")), vec![String::from("ahmed"), String::from("gamal")]);
}

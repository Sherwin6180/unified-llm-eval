use std::collections::HashMap;

/// Given a HashMap, return true if all keys are strings in lower 
/// case or all keys are strings in upper case, else return false.
/// The function should return false is the given HashMap is empty.
/// Examples:
/// >>> check_dict_case(HashMap::from([(String::from("a"), String::from("apple")), (String::from("b"), String::from("banana"))]))
/// true
/// >>> check_dict_case(HashMap::from([(String::from("a"), String::from("apple")), (String::from("A"), String::from("banana")), (String::from("B"), String::from("banana"))]))
/// false
/// >>> check_dict_case(HashMap::from([(String::from("a"), String::from("apple")), (8, String::from("banana")), (String::from("a"), String::from("apple"))]))
/// false
/// >>> check_dict_case(HashMap::from([(String::from("Name"), String::from("John")), (String::from("Age"), String::from("36")), (String::from("City"), String::from("Houston"))]))
/// false
/// >>> check_dict_case(HashMap::from([(String::from("STATE"), String::from("NC")), (String::from("ZIP"), String::from("12345"))]))
/// true
fn check_dict_case(dict: HashMap<String, String>) -> bool {


    if dict.is_empty() {
        return false;
    }

    let first_key_case = dict.keys().next().unwrap().chars().nth(0).unwrap().is_lowercase();

    for key in dict.keys() {
        if (key.chars().nth(0).unwrap().is_lowercase()) != first_key_case {
            return false;
        }
    }

    true}

fn main() {
    let candidate = check_dict_case;
    assert_eq!(candidate(HashMap::from([(String::from("p"), String::from("pineapple")), (String::from("b"), String::from("banana"))])), true);
    assert_eq!(candidate(HashMap::from([(String::from("p"), String::from("pineapple")), (String::from("A"), String::from("banana")), (String::from("B"), String::from("banana"))])), false);
    assert_eq!(candidate(HashMap::from([(String::from("p"), String::from("pineapple")), (String::from("5"), String::from("banana")), (String::from("a"), String::from("apple"))])), false);
    assert_eq!(candidate(HashMap::from([(String::from("Name"), String::from("John")), (String::from("Age"), String::from("36")), (String::from("City"), String::from("Houston"))])), false);
    assert_eq!(candidate(HashMap::from([(String::from("STATE"), String::from("NC")), (String::from("ZIP"), String::from("12345"))])), true);
    assert_eq!(candidate(HashMap::from([(String::from("fruit"), String::from("Orange")), (String::from("taste"), String::from("Sweet"))])), true);
    assert_eq!(candidate(HashMap::from([])), false);
}

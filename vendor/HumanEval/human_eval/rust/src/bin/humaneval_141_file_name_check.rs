/// Create a function which takes a string representing a file's name, and returns
/// 'Yes' if the the file's name is valid, and returns 'No' otherwise.
/// A file's name is considered to be valid if and only if all the following conditions 
/// are met:
/// - There should not be more than three digits ('0'-'9') in the file's name.
/// - The file's name contains exactly one dot '.'
/// - The substring before the dot should not be empty, and it starts with a letter from 
/// the latin alphapet ('a'-'z' and 'A'-'Z').
/// - The substring after the dot should be one of these: ['txt', 'exe', 'dll']
/// Examples:
/// >>> file_name_check(String::from("example.txt"))
/// String::from("Yes")
/// >>> file_name_check(String::from("1example.dll"))
/// String::from("No")
fn file_name_check(file_name: String) -> String {


    let mut count = 0;
    let mut before_dot = false;
    let mut after_dot = false;
    let mut has_letter = false;
    let mut has_digits = false;
    let mut has_valid_extension = false;

    for c in file_name.chars() {
        if c.is_digit(10) {
            has_digits = true;
            count += 1;
            if count > 3 {
                return String::from("No");
            }
        } else if c.is_alphabetic() {
            has_letter = true;
            if !before_dot {
                before_dot = true;
            }
        } else if c == '.' {
            if before_dot && !after_dot {
                after_dot = true;
            } else {
                return String::from("No");
            }
        } else if c.is_ascii_alphabetic() {
            if after_dot {
                return String::from("No");
            }
        }
    }

    if !after_dot || !has_letter || !has_digits {
        return String::from("No");
    }

    let extension = file_name.split('.').last().unwrap();
    if extension == "txt" || extension == "exe" || extension == "dll" {
        has_valid_extension = true;
    }

    if has_valid_extension {
        String::from("Yes")
    } else {
        String::from("No")
    }}

fn main() {
    let candidate = file_name_check;
    assert_eq!(candidate(String::from("example.txt")), String::from("Yes"));
    assert_eq!(candidate(String::from("1example.dll")), String::from("No"));
    assert_eq!(candidate(String::from("s1sdf3.asd")), String::from("No"));
    assert_eq!(candidate(String::from("K.dll")), String::from("Yes"));
    assert_eq!(candidate(String::from("MY16FILE3.exe")), String::from("Yes"));
    assert_eq!(candidate(String::from("His12FILE94.exe")), String::from("No"));
    assert_eq!(candidate(String::from("_Y.txt")), String::from("No"));
    assert_eq!(candidate(String::from("?aREYA.exe")), String::from("No"));
    assert_eq!(candidate(String::from("/this_is_valid.dll")), String::from("No"));
    assert_eq!(candidate(String::from("this_is_valid.wow")), String::from("No"));
    assert_eq!(candidate(String::from("this_is_valid.txt")), String::from("Yes"));
    assert_eq!(candidate(String::from("this_is_valid.txtexe")), String::from("No"));
    assert_eq!(candidate(String::from("#this2_i4s_5valid.ten")), String::from("No"));
    assert_eq!(candidate(String::from("@this1_is6_valid.exe")), String::from("No"));
    assert_eq!(candidate(String::from("this_is_12valid.6exe4.txt")), String::from("No"));
    assert_eq!(candidate(String::from("all.exe.txt")), String::from("No"));
    assert_eq!(candidate(String::from("I563_No.exe")), String::from("Yes"));
    assert_eq!(candidate(String::from("Is3youfault.txt")), String::from("Yes"));
    assert_eq!(candidate(String::from("no_one#knows.dll")), String::from("Yes"));
    assert_eq!(candidate(String::from("1I563_Yes3.exe")), String::from("No"));
    assert_eq!(candidate(String::from("I563_Yes3.txtt")), String::from("No"));
    assert_eq!(candidate(String::from("final..txt")), String::from("No"));
    assert_eq!(candidate(String::from("final132")), String::from("No"));
    assert_eq!(candidate(String::from("_f4indsartal132.")), String::from("No"));
    assert_eq!(candidate(String::from(".txt")), String::from("No"));
    assert_eq!(candidate(String::from("s.")), String::from("No"));
}

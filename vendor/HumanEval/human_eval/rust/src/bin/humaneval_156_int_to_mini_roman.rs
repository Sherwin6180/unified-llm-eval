/// Given a positive integer, obtain its roman numeral equivalent as a string,
/// and return it in lowercase.
/// Restrictions: 1 <= num <= 1000
/// Examples:
/// >>> int_to_mini_roman(19)
/// String::from("xix")
/// >>> int_to_mini_roman(152)
/// String::from("clii")
/// >>> int_to_mini_roman(426)
/// String::from("cdxxvi")
fn int_to_mini_roman(number: isize) -> String {


    let mut num = number;
    let mut result = String::new();
    let mut roman_numerals = [
        (1000, "m"),
        (900, "cm"),
        (500, "d"),
        (400, "cd"),
        (100, "c"),
        (90, "xc"),
        (50, "l"),
        (40, "xl"),
        (10, "x"),
        (9, "ix"),
        (5, "v"),
        (4, "iv"),
        (1, "i"),
    ];

    for (value, symbol) in roman_numerals.iter() {
        while num >= *value {
            num -= value;
            result.push_str(symbol);
        }
    }

    result}

fn main() {
    let candidate = int_to_mini_roman;
    assert_eq!(candidate(19), String::from("xix"));
    assert_eq!(candidate(152), String::from("clii"));
    assert_eq!(candidate(251), String::from("ccli"));
    assert_eq!(candidate(426), String::from("cdxxvi"));
    assert_eq!(candidate(500), String::from("d"));
    assert_eq!(candidate(1), String::from("i"));
    assert_eq!(candidate(4), String::from("iv"));
    assert_eq!(candidate(43), String::from("xliii"));
    assert_eq!(candidate(90), String::from("xc"));
    assert_eq!(candidate(94), String::from("xciv"));
    assert_eq!(candidate(532), String::from("dxxxii"));
    assert_eq!(candidate(900), String::from("cm"));
    assert_eq!(candidate(994), String::from("cmxciv"));
    assert_eq!(candidate(1000), String::from("m"));
}

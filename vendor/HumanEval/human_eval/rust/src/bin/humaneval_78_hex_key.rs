/// You have been tasked to write a function that receives 
/// a hexadecimal number as a string and counts the number of hexadecimal 
/// digits that are primes (prime number, or a prime, is a natural number 
/// greater than 1 that is not a product of two smaller natural numbers).
/// Hexadecimal digits are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.
/// Prime numbers are 2, 3, 5, 7, 11, 13, 17,...
/// So you have to determine a number of the following digits: 2, 3, 5, 7, 
/// B (=decimal 11), D (=decimal 13).
/// Note: you may assume the input is always correct or empty string, 
/// and symbols A,B,C,D,E,F are always uppercase.
/// Examples:
/// >>> hex_key(String::from("AB"))
/// 1
/// >>> hex_key(String::from("1077E"))
/// 2
/// >>> hex_key(String::from("ABED1A33"))
/// 4
/// >>> hex_key(String::from("123456789ABCDEF0"))
/// 6
/// >>> hex_key(String::from("2020"))
/// 2
fn hex_key(num: String) -> isize {


    let primes = vec!['2', '3', '5', '7', 'B', 'D'];
    let mut count = 0;
    for c in num.chars() {
        if primes.contains(&c) {
            count += 1;
        }
    }
    count}

fn main() {
    let candidate = hex_key;
    assert_eq!(candidate(String::from("AB")), 1);
    assert_eq!(candidate(String::from("1077E")), 2);
    assert_eq!(candidate(String::from("ABED1A33")), 4);
    assert_eq!(candidate(String::from("2020")), 2);
    assert_eq!(candidate(String::from("123456789ABCDEF0")), 6);
    assert_eq!(candidate(String::from("112233445566778899AABBCCDDEEFF00")), 12);
}

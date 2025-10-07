/// Given two vectors operator, and operand. The first vector has basic algebra operations, and 
/// the second vector is a vector of integers. Use the two given vectors to build the algebric 
/// expression and return the evaluation of this expression.
/// The basic algebra operations:
/// Addition ( + ) 
/// Subtraction ( - ) 
/// Multiplication ( * ) 
/// Floor division ( // ) 
/// Exponentiation ( ** ) 
/// Example:
/// operator['+', '*', '-']
/// vector = [2, 3, 4, 5]
/// result = 2 + 3 * 4 - 5
/// => result = 9
/// Note:
/// The length of operator vector is equal to the length of operand vector minus one.
/// Operand is a vector of of non-negative integers.
/// Operator vector has at least one operator, and operand vector has at least two operands.
fn do_algebra(operator: Vec<String>, operand: Vec<isize>) -> isize {


    let mut result = operand[0];
    for i in 1..operand.len() {
        match operator[i - 1].as_str() {
            "+" => result += operand[i],
            "-" => result -= operand[i],
            "*" => result *= operand[i],
            "//" => result /= operand[i],
            "**" => result = result.pow(operand[i] as u32),
            _ => (),
        }
    }
    result}

fn main() {
    let candidate = do_algebra;
    assert_eq!(candidate(vec![String::from("**"), String::from("*"), String::from("+")], vec![2, 3, 4, 5]), 37);
    assert_eq!(candidate(vec![String::from("+"), String::from("*"), String::from("-")], vec![2, 3, 4, 5]), 9);
    assert_eq!(candidate(vec![String::from("//"), String::from("*")], vec![7, 3, 4]), 8);
}

/// Write a function that returns true if the given number is the multiplication of 3 prime numbers
/// and false otherwise.
/// Knowing that (a) is less then 100. 
/// Example:
/// >>> is_multiply_prime(30)
/// true
/// 30 = 2 * 3 * 5
fn is_multiply_prime(a: isize) -> bool {


    let mut count = 0;
    let mut n = a;
    let primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97];
    for prime in primes.iter() {
        while n % prime == 0 {
            n /= prime;
            count += 1;
        }
    }
    count == 3 && n == 1}

fn main() {
    let candidate = is_multiply_prime;
    assert_eq!(candidate(5), false);
    assert_eq!(candidate(30), true);
    assert_eq!(candidate(8), true);
    assert_eq!(candidate(10), false);
    assert_eq!(candidate(125), true);
    assert_eq!(candidate(105), true);
    assert_eq!(candidate(126), false);
    assert_eq!(candidate(729), false);
    assert_eq!(candidate(891), false);
    assert_eq!(candidate(1001), true);
}

/// Return n-th Fibonacci number.
/// >>> fib(10)
/// 55
/// >>> fib(1)
/// 1
/// >>> fib(8)
/// 21
fn fib(n: isize) -> isize {


    match n {
        0 => 0,
        1 => 1,
        _ => fib(n - 1) + fib(n - 2),
    }}

fn main() {
    let candidate = fib;
    assert_eq!(candidate(10), 55);
    assert_eq!(candidate(1), 1);
    assert_eq!(candidate(8), 21);
    assert_eq!(candidate(11), 89);
    assert_eq!(candidate(12), 144);
}

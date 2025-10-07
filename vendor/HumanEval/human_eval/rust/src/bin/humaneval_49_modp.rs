/// Return 2^n modulo p (be aware of numerics).
/// >>> modp(3, 5)
/// 3
/// >>> modp(1101, 101)
/// 2
/// >>> modp(0, 101)
/// 1
/// >>> modp(3, 11)
/// 8
/// >>> modp(100, 101)
/// 1
fn modp(n: isize, p: isize) -> isize {


    if n == 0 {
        return 1;
    }
    if n == 1 {
        return 2;
    }
    if n % 2 == 0 {
        let half_n = n / 2;
        let half_pow = modp(half_n, p);
        return (half_pow * half_pow) % p;
    } else {
        return (2 * modp(n - 1, p)) % p;
    }}

fn main() {
    let candidate = modp;
    assert_eq!(candidate(3, 5), 3);
    assert_eq!(candidate(1101, 101), 2);
    assert_eq!(candidate(0, 101), 1);
    assert_eq!(candidate(3, 11), 8);
    assert_eq!(candidate(100, 101), 1);
    assert_eq!(candidate(30, 5), 4);
    assert_eq!(candidate(31, 5), 3);
}

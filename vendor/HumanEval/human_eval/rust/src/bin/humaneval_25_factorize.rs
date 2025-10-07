/// Return vector of prime factors of given integer in the order from smallest to largest.
/// Each of the factors should be vectored number of times corresponding to how many times it appeares in factorization.
/// Input number should be equal to the product of all factors
/// >>> factorize(8)
/// vec![2, 2, 2]
/// >>> factorize(25)
/// vec![5, 5]
/// >>> factorize(70)
/// vec![2, 5, 7]
fn factorize(n: isize) -> Vec<isize> {


    let mut factors = vec![];
    let mut d = 2;
    let mut n = n;
    while d * d <= n {
        while (n % d) == 0 {
            factors.push(d);
            n /= d;
        }
        d += 1;
    }
    if n > 1 {
        factors.push(n);
    }
    factors}

fn main() {
    let candidate = factorize;
    assert_eq!(candidate(2), vec![2]);
    assert_eq!(candidate(4), vec![2, 2]);
    assert_eq!(candidate(8), vec![2, 2, 2]);
    assert_eq!(candidate(57), vec![3, 19]);
    assert_eq!(candidate(3249), vec![3, 3, 19, 19]);
    assert_eq!(candidate(185193), vec![3, 3, 3, 19, 19, 19]);
    assert_eq!(candidate(20577), vec![3, 19, 19, 19]);
    assert_eq!(candidate(18), vec![2, 3, 3]);
}

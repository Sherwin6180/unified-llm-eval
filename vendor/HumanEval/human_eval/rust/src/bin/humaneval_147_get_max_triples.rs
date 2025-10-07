/// You are given a positive integer n. You have to create an integer vector a of length n.
/// For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
/// Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
/// and a[i] + a[j] + a[k] is a multiple of 3.
/// Example :
/// >>> get_max_triples(5)
/// 1
/// Explanation: 
/// a = [1, 3, 7, 13, 21]
/// The only valid triple is (1, 7, 13).
fn get_max_triples(n: isize) -> isize {


    let mut a = vec![0; n as usize];
    for i in 0..n {
        a[i as usize] = i * i - i + 1;
    }
    let mut count = 0;
    for i in 0..n {
        for j in (i + 1)..n {
            for k in (j + 1)..n {
                if (a[i as usize] + a[j as usize] + a[k as usize]) % 3 == 0 {
                    count += 1;
                }
            }
        }
    }
    count}

fn main() {
    let candidate = get_max_triples;
    assert_eq!(candidate(5), 1);
    assert_eq!(candidate(6), 4);
    assert_eq!(candidate(10), 36);
    assert_eq!(candidate(100), 53361);
}

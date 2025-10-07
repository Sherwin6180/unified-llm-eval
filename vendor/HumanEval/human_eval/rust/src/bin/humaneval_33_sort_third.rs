/// This function takes a vector l and returns a vector l' such that
/// l' is identical to l in the indicies that are not divisible by three, while its values at the indicies that are divisible by three are equal
/// to the values of the corresponding indicies of l, but sorted.
/// >>> sort_third(vec![1, 2, 3])
/// vec![1, 2, 3]
/// >>> sort_third(vec![5, 6, 3, 4, 8, 9, 2])
/// vec![2, 6, 3, 4, 8, 9, 5]
fn sort_third(l: Vec<isize>) -> Vec<isize> {


    let mut l_prime = l.clone();
    let mut third_indices: Vec<usize> = Vec::new();
    for (i, &x) in l.iter().enumerate() {
        if x % 3 == 0 {
            third_indices.push(i);
        }
    }
    third_indices.sort();
    let mut j = 0;
    for i in 0..l.len() {
        if l[i] % 3 == 0 {
            l_prime[i] = l[third_indices[j]];
            j += 1;
        }
    }
    l_prime}

fn main() {
    let candidate = sort_third;
    assert_eq!(candidate(vec![5, 6, 3, 4, 8, 9, 2]), vec![2, 6, 3, 4, 8, 9, 5]);
    assert_eq!(candidate(vec![5, 8, 3, 4, 6, 9, 2]), vec![2, 8, 3, 4, 6, 9, 5]);
    assert_eq!(candidate(vec![5, 6, 9, 4, 8, 3, 2]), vec![2, 6, 9, 4, 8, 3, 5]);
    assert_eq!(candidate(vec![5, 6, 3, 4, 8, 9, 2, 1]), vec![2, 6, 3, 4, 8, 9, 5, 1]);
}

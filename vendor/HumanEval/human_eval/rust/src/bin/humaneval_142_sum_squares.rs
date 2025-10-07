/// "
/// This function will take a vector of integers. For all entries in the vector, the function shall square the integer entry if its index is a 
/// multiple of 3 and will cube the integer entry if its index is a multiple of 4 and not a multiple of 3. The function will not 
/// change the entries in the vector whose indexes are not a multiple of 3 or 4. The function shall then return the sum of all entries. 
/// Examples:
/// >>> lst
/// vec![1, 2, 3]
/// >>> lst
/// vec![]
/// >>> lst
/// vec![-1, -5, 2, -1, -5]
fn sum_squares(lst: Vec<isize>) -> isize {


    let mut sum = 0;
    for (i, &num) in lst.iter().enumerate() {
        if i % 3 == 0 {
            sum += num * num;
        } else if i % 4 == 0 {
            sum += num * num * num;
        }
    }
    sum}

fn main() {
    let candidate = sum_squares;
    assert_eq!(candidate(vec![1, 2, 3]), 6);
    assert_eq!(candidate(vec![1, 4, 9]), 14);
    assert_eq!(candidate(Vec::<isize>::new()), 0);
    assert_eq!(candidate(vec![1, 1, 1, 1, 1, 1, 1, 1, 1]), 9);
    assert_eq!(candidate(vec![-1, -1, -1, -1, -1, -1, -1, -1, -1]), -3);
    assert_eq!(candidate(vec![0]), 0);
    assert_eq!(candidate(vec![-1, -5, 2, -1, -5]), -126);
    assert_eq!(candidate(vec![-56, -99, 1, 0, -2]), 3030);
    assert_eq!(candidate(vec![-1, 0, 0, 0, 0, 0, 0, 0, -1]), 0);
    assert_eq!(candidate(vec![-16, -9, -2, 36, 36, 26, -20, 25, -40, 20, -4, 12, -26, 35, 37]), -14196);
    assert_eq!(candidate(vec![-1, -3, 17, -1, -15, 13, -1, 14, -14, -12, -5, 14, -14, 6, 13, 11, 16, 16, 4, 10]), -1448);
}

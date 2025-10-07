/// Create a function that takes 3 numbers.
/// Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
/// Returns false in any other cases.
/// Examples
/// >>> any_int(5, 2, 7)
/// true
/// >>> any_int(3, 2, 2)
/// false
/// >>> any_int(3, -2, 1)
/// true
/// >>> any_int(3.6, -2.2, 2)
/// false
fn any_int(x: f64, y: f64, z: f64) -> bool {


    let x = x as i64;
    let y = y as i64;
    let z = z as i64;
    x == y + z || y == x + z || z == x + y}

fn main() {
    let candidate = any_int;
    assert_eq!(candidate(2.0, 3.0, 1.0), true);
    assert_eq!(candidate(2.5, 2.0, 3.0), false);
    assert_eq!(candidate(1.5, 5.0, 3.5), false);
    assert_eq!(candidate(2.0, 6.0, 2.0), false);
    assert_eq!(candidate(4.0, 2.0, 2.0), true);
    assert_eq!(candidate(2.2, 2.2, 2.2), false);
    assert_eq!(candidate(-4.0, 6.0, 2.0), true);
    assert_eq!(candidate(2.0, 1.0, 1.0), true);
    assert_eq!(candidate(3.0, 4.0, 7.0), true);
    assert_eq!(candidate(3.0, 4.0, 7.0), false);
}

/// Write a function that takes an integer a and returns true 
/// if this ingeger is a cube of some integer number.
/// Note: you may assume the input is always valid.
/// Examples:
/// >>> iscube(1)
/// true
/// >>> iscube(2)
/// false
/// >>> iscube(-1)
/// true
/// >>> iscube(64)
/// true
/// >>> iscube(0)
/// true
/// >>> iscube(180)
/// false
fn iscube(a: isize) -> bool {


    let c = a.cbrt();
    c * c * c == a}

fn main() {
    let candidate = iscube;
    assert_eq!(candidate(1), true);
    assert_eq!(candidate(2), false);
    assert_eq!(candidate(-1), true);
    assert_eq!(candidate(64), true);
    assert_eq!(candidate(180), false);
    assert_eq!(candidate(1000), true);
    assert_eq!(candidate(0), true);
    assert_eq!(candidate(1729), false);
}

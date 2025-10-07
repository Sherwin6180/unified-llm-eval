/// Given the lengths of the three sides of a triangle. Return true if the three
/// sides form a right-angled triangle, false otherwise.
/// A right-angled triangle is a triangle in which one angle is right angle or 
/// 90 degree.
/// Example:
/// >>> right_angle_triangle(3, 4, 5)
/// true
/// >>> right_angle_triangle(1, 2, 3)
/// false
fn right_angle_triangle(a: isize, b: isize, c: isize) -> bool {


    let sides = [a, b, c];
    let mut sorted_sides = sides.clone();
    sorted_sides.sort_unstable();
    sorted_sides[0].pow(2) + sorted_sides[1].pow(2) == sorted_sides[2].pow(2)}

fn main() {
    let candidate = right_angle_triangle;
    assert_eq!(candidate(3, 4, 5), true);
    assert_eq!(candidate(1, 2, 3), false);
    assert_eq!(candidate(10, 6, 8), true);
    assert_eq!(candidate(2, 2, 2), false);
    assert_eq!(candidate(7, 24, 25), true);
    assert_eq!(candidate(10, 5, 7), false);
    assert_eq!(candidate(5, 12, 13), true);
    assert_eq!(candidate(15, 8, 17), true);
    assert_eq!(candidate(48, 55, 73), true);
    assert_eq!(candidate(1, 1, 1), false);
    assert_eq!(candidate(2, 2, 10), false);
}

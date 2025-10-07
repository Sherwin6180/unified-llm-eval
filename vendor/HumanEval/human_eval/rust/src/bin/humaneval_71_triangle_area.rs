/// Given the lengths of the three sides of a triangle. Return the area of
/// the triangle rounded to 2 decimal points if the three sides form a valid triangle. 
/// Otherwise return -1
/// Three sides make a valid triangle when the sum of any two sides is greater 
/// than the third side.
/// Example:
/// >>> triangle_area(3, 4, 5)
/// 6.0
/// >>> triangle_area(1, 2, 10)
/// -1.0
fn triangle_area(a: isize, b: isize, c: isize) -> f64 {


    if a + b > c && a + c > b && b + c > a {
        let semi_perimeter = (a + b + c) as f64 / 2.0;
        let area = (semi_perimeter * (semi_perimeter - a as f64) * (semi_perimeter - b as f64) * (semi_perimeter - c as f64)).sqrt();
        (area * 100.0).round() / 100.0
    } else {
        -1.0
    }}

fn main() {
    let candidate = triangle_area;
    assert_eq!(candidate(3, 4, 5), 6.0);
    assert_eq!(candidate(1, 2, 10), -1.0);
    assert_eq!(candidate(4, 8, 5), 8.18);
    assert_eq!(candidate(2, 2, 2), 1.73);
    assert_eq!(candidate(1, 2, 3), -1.0);
    assert_eq!(candidate(10, 5, 7), 16.25);
    assert_eq!(candidate(2, 6, 3), -1.0);
    assert_eq!(candidate(1, 1, 1), 0.43);
    assert_eq!(candidate(2, 2, 10), -1.0);
}

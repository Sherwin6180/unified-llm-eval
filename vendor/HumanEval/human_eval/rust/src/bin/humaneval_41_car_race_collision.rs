/// Imagine a road that's a perfectly straight infinitely long line.
/// n cars are driving left to right;  simultaneously, a different set of n cars
/// are driving right to left.   The two sets of cars start out being very far from
/// each other.  All cars move in the same speed.  Two cars are said to collide
/// when a car that's moving left to right hits a car that's moving right to left.
/// However, the cars are infinitely sturdy and strong; as a result, they continue moving
/// in their trajectory as if they did not collide.
/// This function outputs the number of such collisions.
fn car_race_collision(n: isize) -> isize {


    n * (n - 1) / 2}

fn main() {
    let candidate = car_race_collision;
    assert_eq!(candidate(2), 4);
    assert_eq!(candidate(3), 9);
    assert_eq!(candidate(4), 16);
    assert_eq!(candidate(8), 64);
    assert_eq!(candidate(10), 100);
}

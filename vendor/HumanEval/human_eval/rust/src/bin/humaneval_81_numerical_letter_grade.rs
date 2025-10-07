/// It is the last week of the semester and the teacher has to give the grades
/// to students. The teacher has been making her own algorithm for grading.
/// The only problem is, she has lost the code she used for grading.
/// She has given you a vector of GPAs for some students and you have to write 
/// a function that can output a vector of letter grades using the following table:
/// GPA       |    Letter grade
/// 4.0                A+
/// > 3.7                A 
/// > 3.3                A- 
/// > 3.0                B+
/// > 2.7                B 
/// > 2.3                B-
/// > 2.0                C+
/// > 1.7                C
/// > 1.3                C-
/// > 1.0                D+ 
/// > 0.7                D 
/// > 0.0                D-
/// 0.0                E
/// Example:
/// >>> grade_equation(vec![4.0, 3, 1.7, 2, 3.5])
/// vec![String::from("A+"), String::from("B"), String::from("C-"), String::from("C"), String::from("A-")]
fn numerical_letter_grade(grades: Vec<f64>) -> Vec<String> {


    let mut letter_grades: Vec<String> = grades.iter().map(|grade| {
        if *grade == 4.0 {
            "A+".to_string()
        } else if *grade > 3.7 {
            "A".to_string()
        } else if *grade > 3.3 {
            "A-".to_string()
        } else if *grade > 3.0 {
            "B+".to_string()
        } else if *grade > 2.7 {
            "B".to_string()
        } else if *grade > 2.3 {
            "B-".to_string()
        } else if *grade > 2.0 {
            "C+".to_string()
        } else if *grade > 1.7 {
            "C".to_string()
        } else if *grade > 1.3 {
            "C-".to_string()
        } else if *grade > 1.0 {
            "D+".to_string()
        } else if *grade > 0.7 {
            "D".to_string()
        } else if *grade > 0.0 {
            "D-".to_string()
        } else {
            "E".to_string()
        }
    }).collect();
    letter_grades}

fn main() {
    let candidate = numerical_letter_grade;
    assert_eq!(candidate(vec![4.0, 3.0, 1.7, 2.0, 3.5]), vec![String::from("A+"), String::from("B"), String::from("C-"), String::from("C"), String::from("A-")]);
    assert_eq!(candidate(vec![1.2]), vec![String::from("D+")]);
    assert_eq!(candidate(vec![0.5]), vec![String::from("D-")]);
    assert_eq!(candidate(vec![0.0]), vec![String::from("E")]);
    assert_eq!(candidate(vec![1.0, 0.3, 1.5, 2.8, 3.3]), vec![String::from("D"), String::from("D-"), String::from("C-"), String::from("B"), String::from("B+")]);
    assert_eq!(candidate(vec![0.0, 0.7]), vec![String::from("E"), String::from("D-")]);
}

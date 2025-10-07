/// You have to write a function which validates a given date string and
/// returns true if the date is valid otherwise false.
/// The date is valid if all of the following rules are satisfied:
/// 1. The date string is not empty.
/// 2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12. And the number of days is not less than 1 or higher than 30 days for months 4,6,9,11. And, the number of days is not less than 1 or higher than 29 for the month 2.
/// 3. The months should not be less than 1 or higher than 12.
/// 4. The date should be in the format: mm-dd-yyyy
/// >>> valid_date(String::from("03-11-2000"))
/// true
/// >>> valid_date(String::from("15-01-2012"))
/// false
/// >>> valid_date(String::from("04-0-2040"))
/// false
/// >>> valid_date(String::from("06-04-2020"))
/// true
/// >>> valid_date(String::from("06/04/2020"))
/// false
fn valid_date(date: String) -> bool {


    let re = regex::Regex::new(r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-\d{4}$").unwrap();
    re.is_match(&date)}

fn main() {
    let candidate = valid_date;
    assert_eq!(candidate(String::from("03-11-2000")), true);
    assert_eq!(candidate(String::from("15-01-2012")), false);
    assert_eq!(candidate(String::from("04-0-2040")), false);
    assert_eq!(candidate(String::from("06-04-2020")), true);
    assert_eq!(candidate(String::from("01-01-2007")), true);
    assert_eq!(candidate(String::from("03-32-2011")), false);
    assert_eq!(candidate(String::from("")), false);
    assert_eq!(candidate(String::from("04-31-3000")), false);
    assert_eq!(candidate(String::from("06-06-2005")), true);
    assert_eq!(candidate(String::from("21-31-2000")), false);
    assert_eq!(candidate(String::from("04-12-2003")), true);
    assert_eq!(candidate(String::from("04122003")), false);
    assert_eq!(candidate(String::from("20030412")), false);
    assert_eq!(candidate(String::from("2003-04")), false);
    assert_eq!(candidate(String::from("2003-04-12")), false);
    assert_eq!(candidate(String::from("04-2003")), false);
}

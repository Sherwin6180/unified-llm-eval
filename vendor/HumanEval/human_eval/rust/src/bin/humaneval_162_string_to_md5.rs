/// Given a string 'text', return its md5 hash equivalent string.
/// If 'text' is an empty string, return None.
/// >>> string_to_md5(String::from("Hello world"))
/// Some(String::from("3e25960a79dbc69b674cd4ec67a72c62"))
fn string_to_md5(text: String) -> Option<String> {


    if text.is_empty() {
        return None;
    }
    let mut hasher = md5::compute(text);
    Some(format!("{:x}", hasher))}

fn main() {
    let candidate = string_to_md5;
    assert_eq!(candidate(String::from("Hello world")), Some(String::from("3e25960a79dbc69b674cd4ec67a72c62")));
    assert_eq!(candidate(String::from("")), None);
    assert_eq!(candidate(String::from("A B C")), Some(String::from("0ef78513b0cb8cef12743f5aeb35f888")));
    assert_eq!(candidate(String::from("password")), Some(String::from("5f4dcc3b5aa765d61d8327deb882cf99")));
}

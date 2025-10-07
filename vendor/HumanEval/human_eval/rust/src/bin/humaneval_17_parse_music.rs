/// Input to this function is a string representing musical notes in a special ASCII format.
/// Your task is to parse this string and return vector of integers corresponding to how many beats does each
/// not last.
/// Here is a legend:
/// 'o' - whole note, lasts four beats
/// 'o|' - half note, lasts two beats
/// '.|' - quater note, lasts one beat
/// >>> parse_music(String::from("o o| .| o| o| .| .| .| .| o o"))
/// vec![4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
fn parse_music(music_string: String) -> Vec<isize> {


    let mut result = vec![];
    let mut current_note = String::new();
    for c in music_string.chars() {
        if c == ' ' {
            if current_note == "o" {
                result.push(4);
            } else if current_note == "o|" {
                result.push(2);
            } else if current_note == ".|" {
                result.push(1);
            }
            current_note.clear();
        } else {
            current_note.push(c);
        }
    }
    if !current_note.is_empty() {
        if current_note == "o" {
            result.push(4);
        } else if current_note == "o|" {
            result.push(2);
        } else if current_note == ".|" {
            result.push(1);
        }
    }
    result}

fn main() {
    let candidate = parse_music;
    assert_eq!(candidate(String::from("")), Vec::<isize>::new());
    assert_eq!(candidate(String::from("o o o o")), vec![4, 4, 4, 4]);
    assert_eq!(candidate(String::from(".| .| .| .|")), vec![1, 1, 1, 1]);
    assert_eq!(candidate(String::from("o| o| .| .| o o o o")), vec![2, 2, 1, 1, 4, 4, 4, 4]);
    assert_eq!(candidate(String::from("o| .| o| .| o o| o o|")), vec![2, 1, 2, 1, 4, 2, 4, 2]);
}

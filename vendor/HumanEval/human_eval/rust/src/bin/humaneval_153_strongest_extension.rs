/// You will be given the name of a class (a string) and a vector of extensions.
/// The extensions are to be used to load additional classes to the class. The
/// strength of the extension is as follows: Let CAP be the number of the uppercase
/// letters in the extension's name, and let SM be the number of lowercase letters 
/// in the extension's name, the strength is given by the fraction CAP - SM. 
/// You should find the strongest extension and return a string in this 
/// format: ClassName.StrongestExtensionName.
/// If there are two or more extensions with the same strength, you should
/// choose the one that comes first in the vector.
/// For example, if you are given "Slices" as the class and a vector of the
/// extensions: ['SErviNGSliCes', 'Cheese', 'StuFfed'] then you should
/// return 'Slices.SErviNGSliCes' since 'SErviNGSliCes' is the strongest extension 
/// (its strength is -1).
/// Example:
/// >>> Strongest_Extension(String::from("my_class"), vec![String::from("AA"), String::from("Be"), String::from("CC")])
/// String::from("my_class.AA")
fn Strongest_Extension(class_name: String, extensions: Vec<String>) -> String {


    let mut max_strength = i32::MIN;
    let mut strongest_extension = String::new();

    for extension in extensions {
        let mut strength = 0;
        for c in extension.chars() {
            if c.is_lowercase() {
                strength += 1;
            } else if c.is_uppercase() {
                strength -= 1;
            }
        }

        if strength > max_strength {
            max_strength = strength;
            strongest_extension = extension;
        }
    }

    format!("{}.{}", class_name, strongest_extension)}

fn main() {
    let candidate = Strongest_Extension;
    assert_eq!(candidate(String::from("Watashi"), vec![String::from("tEN"), String::from("niNE"), String::from("eIGHt8OKe")]), String::from("Watashi.eIGHt8OKe"));
    assert_eq!(candidate(String::from("Boku123"), vec![String::from("nani"), String::from("NazeDa"), String::from("YEs.WeCaNe"), String::from("32145tggg")]), String::from("Boku123.YEs.WeCaNe"));
    assert_eq!(candidate(String::from("__YESIMHERE"), vec![String::from("t"), String::from("eMptY"), String::from("nothing"), String::from("zeR00"), String::from("NuLl__"), String::from("123NoooneB321")]), String::from("__YESIMHERE.NuLl__"));
    assert_eq!(candidate(String::from("K"), vec![String::from("Ta"), String::from("TAR"), String::from("t234An"), String::from("cosSo")]), String::from("K.TAR"));
    assert_eq!(candidate(String::from("__HAHA"), vec![String::from("Tab"), String::from("123"), String::from("781345"), String::from("-_-")]), String::from("__HAHA.123"));
    assert_eq!(candidate(String::from("YameRore"), vec![String::from("HhAas"), String::from("okIWILL123"), String::from("WorkOut"), String::from("Fails"), String::from("-_-")]), String::from("YameRore.okIWILL123"));
    assert_eq!(candidate(String::from("finNNalLLly"), vec![String::from("Die"), String::from("NowW"), String::from("Wow"), String::from("WoW")]), String::from("finNNalLLly.WoW"));
    assert_eq!(candidate(String::from("_"), vec![String::from("Bb"), String::from("91245")]), String::from("_.Bb"));
    assert_eq!(candidate(String::from("Sp"), vec![String::from("671235"), String::from("Bb")]), String::from("Sp.671235"));
}

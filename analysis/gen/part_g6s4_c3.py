DATA_C3 = {
"R8c49ec85d8": r"""
public void filter (String [] words, String text) {
    String lowerText = text.toLowerCase ();
    for (String word : words) {
        if (lowerText.contains (word.toLowerCase ())) {
            System.out.println (text);
            return;
        }
    }
}
""",
"R2710a37612": r"""
public static final void main (String...aArgs) {
    log ("Generating 10 random integers in range 1..10.");
    final int START = 1;
    final int END = 10;
    Random randomGenerator = new Random ();
    IntStream.rangeClosed (1, 10).forEach (idx -> showRandomInteger (START, END, randomGenerator));
    log ("Done");
}
""",
"Rf6f525dc34": r"""
static void Main (string [] args) {
    Process process = new Process () {StartInfo = MakeStartInfo(args)};
    ExecuteProcess(process);
    ValidateProcessExitCode(process);
}

private static ProcessStartInfo MakeStartInfo (string [] args) {
    string libreOfficePath = getLibreOfficePath();
    ProcessStartInfo procStartInfo = new ProcessStartInfo (libreOfficePath, string.Format (CreateParamString (args)));
    SetProcessStartInfoProperties(procStartInfo);
    return procStartInfo;
}
"""
}

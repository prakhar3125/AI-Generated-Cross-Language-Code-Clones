DATA_R3 = {
"R7c5881afbf": r'''
public static String Combine (String path1, String path2) {
    if (path1 == null)
        throw new ArgumentNullException ("path1");
    if (path2 == null)
        throw new ArgumentNullException ("path2");
    return CombineNoChecks (path1, path2);
}
''',
"R0f80f0fb62": r'''
public static Double Correlation (Double [] Xs, Double [] Ys) {
    int n = Math.Min (Xs.Length, Ys.Length);
    Double avgX = Xs.Take (n).Average ();
    Double avgY = Ys.Take (n).Average ();
    Double sumX2 = 0, sumY2 = 0, sumXY = 0;
    for (int i = 0; i < n; ++ i) {
        sumX2 += Xs [i] * Xs [i];
        sumY2 += Ys [i] * Ys [i];
        sumXY += Xs [i] * Ys [i];
    }
    Double stdX = Math.Sqrt (sumX2 - n * avgX * avgX);
    Double stdY = Math.Sqrt (sumY2 - n * avgY * avgY);
    Double covariance = (sumXY - n * avgX * avgY);
    return covariance / stdX / stdY;
}
''',
"Rdddd23f55c": r'''
public void SendEmail (MyInternalSystemEmailMessage email) {
    var mailMessage = BuildMailMessage (email);
    var mimeMessage = MimeKit.MimeMessage.CreateFromMailMessage (mailMessage);
    var gmailMessage = new Google.Apis.Gmail.v1.Data.Message {Raw = Encode (mimeMessage.ToString ())};
    service.Users.Messages.Send (gmailMessage, ServiceEmail).Execute ();
}

private static System.Net.Mail.MailMessage BuildMailMessage (MyInternalSystemEmailMessage email) {
    var mailMessage = new System.Net.Mail.MailMessage ();
    mailMessage.From = new System.Net.Mail.MailAddress (email.FromAddress);
    mailMessage.To.Add (email.ToRecipients);
    mailMessage.ReplyToList.Add (email.FromAddress);
    mailMessage.Subject = email.Subject;
    mailMessage.Body = email.Body;
    mailMessage.IsBodyHtml = email.IsHtml;
    foreach (System.Net.Mail.Attachment attachment in email.Attachments) {
        mailMessage.Attachments.Add (attachment);
    }
    return mailMessage;
}
''',
"R6b8d361ee9": r'''
static void Main (string [] args) {
    if (args.Length != 2) {
        Console.WriteLine ("Usage:  repchar {inputfile} {outputfile}");
        return;
    }
    using (StreamReader input = new StreamReader (args [0]))
    using (StreamWriter output = new StreamWriter (args [1])) {
        CopyTransformed (input, output);
    }
}

static void CopyTransformed (StreamReader input, StreamWriter output) {
    int blockSize = 100000;
    char [] inBuffer = new char [blockSize];
    char [] outBuffer = new char [blockSize * 3];
    int readSize;
    while ((readSize = input.ReadBlock (inBuffer, 0, blockSize)) > 0) {
        output.Write (outBuffer, 0, TransformBlock (inBuffer, outBuffer, readSize));
    }
}
''',
"R73c281cc62": r'''
private static IEnumerable < T [] > EnumerateCombos < T > (IEnumerable < T > items, List < T > currentCombo, int startIndex, int threshold) {
    if (currentCombo.Count >= threshold) {
        yield break;
    }
    IList < T > list = items as IList < T > ?? items.ToList ();
    int i = startIndex;
    while (i < list.Count) {
        currentCombo.Add (list [i]);
        yield return currentCombo.ToArray ();
        foreach (var combo in EnumerateCombos (list, currentCombo, i + 1, threshold)) {
            yield return combo;
        }
        currentCombo.RemoveAt (currentCombo.Count - 1);
        i ++;
    }
}
''',
"R8cfbeb65a3": r'''
public static IList < ReportFile > ReadFiles (int year, int month) {
    string [] fileNames = {"{0:YYYYMMDD}----1234D.dat", "{0:YYYYMMDD}----5678D.dat"};
    List < ReportFile > reportList = new List < ReportFile > ();
    DateTime dateStart = new DateTime (year, month, 1);
    int days = DateTime.DaysInMonth (year, month);
    for (int day = 0; day < days; day ++) {
        DateTime date = dateStart.AddDays (day);
        reportList.AddRange (fileNames
            .Where (template => File.Exists (string.Format (template, date)))
            .Select (template => new ReportFile {Date = date, Path = string.Format (template, date), Lines = GetReportLines (string.Format (template, date))}));
    }
    return reportList;
}
''',
"R593eed57e6": r'''
static void Main (string [] args) {
    Console.WriteLine ("Enter A Number :");
    int n = int.Parse (Console.ReadLine ());
    bool by3 = n % 3 == 0;
    bool by5 = n % 5 == 0;
    if (by3 && by5) {
        Console.WriteLine ("This Number is Divisible by 3 and 5!");
    } else if (by3) {
        printf ("\nThe number is divisible by 3 but not by 5");
    } else if (by5) {
        Console.WriteLine ("The number is divisible by 5 but not by 3");
    } else {
        Console.WriteLine ("\nThis Number is Not Divisible by 3 and 5!");
    }
    Console.ReadLine ();
}
''',
"Rc5e1a6cc9a": r'''
void initialize () {
    ConcurrentQueue < string > queue = new ConcurrentQueue < string > ();
    websites.ToList ().ForEach (url => queue.Enqueue (url));
    List < Thread > threads = Enumerable.Range (0, threadCountFromTheUser)
        .Select (_ => new Thread (work))
        .ToList ();
}
''',
"R35e99f1126": r'''
static void Main (string [] args) {
    var EDGES = BuildEdges ();
    var POINTS = new List < double [] > (EDGES.Count * 2);
    FillPoints (EDGES, ref POINTS);
    int i = 0;
    foreach (var point in POINTS) {
        Console.WriteLine ("{0} {1} {2}", i ++, point [0], point [1]);
    }
    Console.WriteLine ();
    var edgeIndices = new int [EDGES.Count, 2];
    FillEdges (EDGES, POINTS, ref edgeIndices);
    for (int e = 0; e < edgeIndices.GetLength (0); e ++) {
        Console.WriteLine ("({0}, {1})", edgeIndices [e, 0], edgeIndices [e, 1]);
    }
    Console.ReadKey (true);
}

static List < Edge > BuildEdges () {
    return new List < Edge > {
        new Edge (new Point (5, 50), new Point (20, 100)),
        new Edge (new Point (20, 100), new Point (30, 50)),
        new Edge (new Point (30, 50), new Point (10, 0)),
        new Edge (new Point (5, 50), new Point (30, 50)),
        new Edge (new Point (5, 50), new Point (10, 0)),
        new Edge (new Point (20, 100), new Point (80, 100)),
        new Edge (new Point (10, 0), new Point (80, 100))
    };
}
''',
"R7fe68d314b": r'''
public static List < string > LoadCitiesByState (string state) {
    List < string > cities = new List < string > ();
    DataTable dt = null;
    try {
        dt = SharedDataAccess.GetCities (state);
    } catch {
    }
    if (dt == null) {
        return cities;
    }
    for (int i = 0; i < dt.Rows.Count; i ++) {
        cities.Add (dt.Rows [i] [0].ToString ());
    }
    return cities;
}
''',
"R08feb9bb95": r'''
public void ResetFields (Control.ControlCollection Controls) {
    foreach (Control control in Controls) {
        ResetControl (control);
    }
}

private void ResetControl (Control control) {
    switch (control) {
        case TextBox txt:
            txt.Text = string.Empty;
            break;
        case NumericUpDown numericUpDown:
            numericUpDown.Value = 3;
            break;
        default:
            if (control.Controls.Count > 0) {
                this.ResetFields (control.Controls);
            }
            break;
    }
}
''',
}

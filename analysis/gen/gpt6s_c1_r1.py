DATA_R1 = {
"Rf3d83a68bd": '''def curry(func) :
    def curried(*args) :
        return lambda *more_args: func(*args, *more_args)
    return curried
''',
"R7c5881afbf": '''public static String Combine (String path1, String path2) {
    if (path1 == null)
        throw new ArgumentNullException ("path1");
    if (path2 == null)
        throw new ArgumentNullException ("path2");
    return CombineNoChecks (path1, path2);
}
''',
"R0f80f0fb62": '''public static Double Correlation (Double [] Xs, Double [] Ys) {
    int n = Xs.Length < Ys.Length ? Xs.Length : Ys.Length;
    Double sumX2 = 0;
    Double sumY2 = 0;
    Double sumXY = 0;
    Double avgX = 0;
    Double avgY = 0;
    for (int i = 0; i < n; ++ i) {
        avgX += Xs [i];
        avgY += Ys [i];
        sumXY += Xs [i] * Ys [i];
    }
    avgX /= n;
    avgY /= n;
    for (int i = 0; i < n; ++ i) {
        sumX2 += Xs [i] * Xs [i];
        sumY2 += Ys [i] * Ys [i];
    }
    Double stdX = Math.Sqrt (sumX2 - n * avgX * avgX);
    Double stdY = Math.Sqrt (sumY2 - n * avgY * avgY);
    Double covariance = (sumXY - n * avgX * avgY);
    return covariance / stdX / stdY;
}
''',
"Recd81e23e8": '''int main (int argc, char **argv) {
    char **ipnport = arguments_handle (argc, argv);
    ret[0] = (char *) calloc (20, 1);
    ret[1] = (char *) calloc (20, 1);
    printf ("IP is :%s port range is %s\\n", ipnport [1], ipnport [0]);
    return 0x0;
}
''',
"Radd810f35f": '''public static String join (String separator, String...values) {
    if (values.length == 0) return "";
    int totalSize = (values.length - 1) * separator.length ();
    for (int i = 0; i < values.length; i ++) {
        if (values [i] == null) values [i] = "";
        else totalSize += values [i].length ();
    }
    StringBuilder sb = new StringBuilder (totalSize);
    for (int i = 0; i < values.length; i ++) {
        if (i > 0) sb.append (separator);
        sb.append (values [i]);
    }
    return sb.toString ();
}
''',
"Ra654f3cacb": '''public static boolean isPalindrome (String str) {
    String upper = str.toUpperCase ();
    int left = 0;
    int right = upper.length () - 1;
    while (left < right) {
        if (upper.charAt (left) != upper.charAt (right)) {
            return false;
        }
        left ++;
        right --;
    }
    return true;
}
''',
"Rc8ce82f32f": '''int main (int argc, char **argv) {
    char c;
    printf ("Press key");
    for (;;) {
        if (kbhit ()) break;
        printf (".");
        fflush (stdout);
        sleep (1);
    }
    c = getchar ();
    printf ("\\nChar received:%c\\n", c);
    printf ("Done.\\n");
    return 0;
}
''',
"Rdddd23f55c": '''public void SendEmail (MyInternalSystemEmailMessage email) {
    var mimeMessage = BuildMailMessage (email);
    Send (mimeMessage);
}

private MimeKit.MimeMessage BuildMailMessage (MyInternalSystemEmailMessage email) {
    var mailMessage = new System.Net.Mail.MailMessage {
        From = new System.Net.Mail.MailAddress (email.FromAddress),
        Subject = email.Subject,
        Body = email.Body,
        IsBodyHtml = email.IsHtml
    };
    mailMessage.To.Add (email.ToRecipients);
    mailMessage.ReplyToList.Add (email.FromAddress);
    foreach (System.Net.Mail.Attachment attachment in email.Attachments) {
        mailMessage.Attachments.Add (attachment);
    }
    return MimeKit.MimeMessage.CreateFromMailMessage (mailMessage);
}

private void Send (MimeKit.MimeMessage mimeMessage) {
    var gmailMessage = new Google.Apis.Gmail.v1.Data.Message {Raw = Encode (mimeMessage.ToString ())};
    Google.Apis.Gmail.v1.UsersResource.MessagesResource.SendRequest request = service.Users.Messages.Send (gmailMessage, ServiceEmail);
    request.Execute ();
}
''',
"Rfa50623d34": '''def upgrade() :
	url = context.config.get_main_option("sqlalchemy.url")
	engine = sa.create_engine(url)
	DBSession.configure(bind = engine)
	op.create_table(
	'client_credential',
	sa.Column('id', sa.Integer(), nullable = False),
	sa.Column('created_at', sa.DateTime(), nullable = False),
	sa.Column('updated_at', sa.DateTime(), nullable = False),
	sa.Column('client_id', sa.Integer(), nullable = False),
	sa.Column('key', sa.String(length = 22), nullable = False),
	sa.Column('secret', sa.String(length = 44), nullable = False),
	sa.Column('is_active', sa.Boolean(), nullable = False),
	sa.ForeignKeyConstraint(['client_id'], ['client.id'],),
	sa.PrimaryKeyConstraint('id'),
	sa.UniqueConstraint('key'))
	op.bulk_insert(ClientCredential, [
	{'secret' : client.secret,
	'key' : client.key,
	'is_active' : True,
	'client_id' : client.id,
	'created_at' : sa.func.now(),
	'updated_at' : sa.func.now()} for client in Client.query.all()])
	for column in (u'key', u'secret'):
		op.drop_column(u'client', column)
''',
"R6977f1c997": '''def scan(sentence) :
	tuples = []
	words = sentence.split()
	for word in words :
		if word in lexicons :
			tuples.append((lexicons [word], word))
		elif word.isdigit() :
			tuples.append(('number', int(word)))
		else :
			tuples.append(('error', word))
	return tuples
''',
"Rbcec8876d4": '''def contains(small, big) :
	n = len(small)
	for i in range(len(big) - n + 1) :
		if big [i:i + n] == small :
			return i, i + n
	return False
''',
"Rab8fdb571d": '''int main () {
    char *token;
    char *str = malloc (100);
    strcpy (str, "test string.");
    token = strtok (str, " ");
    while (token != NULL) {
        printf ("%s\\n", token);
        token = strtok (NULL, " ");
    }
    free (str);
    return 0;
}
''',
"R6b8d361ee9": '''static void Main (string [] args) {
    if (args.Length != 2) {
        Console.WriteLine ("Usage:  repchar {inputfile} {outputfile}");
        return;
    }
    ProcessFiles (args [0], args [1]);
}

static void ProcessFiles (string inputPath, string outputPath) {
    using (StreamReader input = new StreamReader (inputPath))
    using (StreamWriter output = new StreamWriter (outputPath))
    {
        int readSize = 0;
        int blockSize = 100000;
        char [] inBuffer = new char [blockSize];
        char [] outBuffer = new char [blockSize * 3];
        while ((readSize = input.ReadBlock (inBuffer, 0, blockSize)) > 0) {
            int writeSize = TransformBlock (inBuffer, outBuffer, readSize);
            output.Write (outBuffer, 0, writeSize);
        }
    }
}
''',
}

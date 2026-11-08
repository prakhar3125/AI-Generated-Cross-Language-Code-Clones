# gpt-5.4-mini chunk 1 part 3: refactors 1-13
DATA3 = {}

DATA3["Rf3d83a68bd"] = r'''
def curry(func):
    def curried(*args):
        return lambda *more_args: func(*args, *more_args)
    return curried
'''

DATA3["R7c5881afbf"] = r'''
public static String Combine(String path1, String path2) {
    ValidatePaths(path1, path2);
    return CombineNoChecks(path1, path2);
}

private static void ValidatePaths(String path1, String path2) {
    if (path1 == null) {
        throw new ArgumentNullException("path1");
    }
    if (path2 == null) {
        throw new ArgumentNullException("path2");
    }
}
'''

DATA3["R0f80f0fb62"] = r'''
using System;
using System.Collections.Generic;
using System.Linq;

public static Double Correlation(Double[] Xs, Double[] Ys) {
    int n = Math.Min(Xs.Length, Ys.Length);
    var pairs = new List<Double>(n);
    for (int i = 0; i < n; i++) {
        pairs.Add(Xs[i]);
        pairs.Add(Ys[i]);
    }
    Double avgX = 0;
    Double avgY = 0;
    for (int i = 0; i < pairs.Count; i += 2) {
        avgX += pairs[i];
        avgY += pairs[i + 1];
    }
    avgX /= n;
    avgY /= n;
    Double sumX2 = 0;
    Double sumY2 = 0;
    Double sumXY = 0;
    for (int i = 0; i < pairs.Count; i += 2) {
        Double x = pairs[i];
        Double y = pairs[i + 1];
        sumX2 += x * x;
        sumY2 += y * y;
        sumXY += x * y;
    }
    Double stdX = Math.Sqrt(sumX2 - avgX * avgX * n);
    Double stdY = Math.Sqrt(sumY2 - avgY * avgY * n);
    Double covariance = sumXY - avgX * avgY * n;
    return covariance / stdX / stdY;
}
'''

DATA3["Recd81e23e8"] = r'''
#include <stdio.h>
#include <stdlib.h>

static char *new_buffer(size_t size) {
    return (char *)calloc(1, size);
}

int main(int argc, char **argv) {
    char *ret[2];
    ret[0] = new_buffer(20);
    ret[1] = new_buffer(20);
    char **ipnport = arguments_handle(argc, argv);
    printf("IP is :%s port range is %s\n", ipnport[1], ipnport[0]);
    return 0x0;
}
'''

DATA3["Radd810f35f"] = r'''
public static String join(String separator, String...values) {
    if (values.length == 0) return "";
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < values.length; i++) {
        if (i > 0) {
            sb.append(separator);
        }
        sb.append(values[i] == null ? "" : values[i]);
    }
    return sb.toString();
}
'''

DATA3["Ra654f3cacb"] = r'''
public static boolean isPalindrome(String str) {
    String upper = str.toUpperCase();
    int left = 0;
    int right = upper.length() - 1;
    while (left < right) {
        if (upper.charAt(left) != upper.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
'''

DATA3["Rc8ce82f32f"] = r'''
int main(int argc, char **argv) {
    char c;
    printf("Press key");
    while (1) {
        if (kbhit()) {
            break;
        }
        putchar('.');
        fflush(stdout);
        sleep(1);
    }
    c = (char)getchar();
    printf("\nChar received:%c\n", c);
    printf("Done.\n");
    return 0;
}
'''

DATA3["Rdddd23f55c"] = r'''
public void SendEmail(MyInternalSystemEmailMessage email) {
    var mailMessage = new System.Net.Mail.MailMessage {
        From = new System.Net.Mail.MailAddress(email.FromAddress),
        Subject = email.Subject,
        Body = email.Body,
        IsBodyHtml = email.IsHtml
    };
    mailMessage.To.Add(email.ToRecipients);
    mailMessage.ReplyToList.Add(email.FromAddress);
    foreach (System.Net.Mail.Attachment attachment in email.Attachments) {
        mailMessage.Attachments.Add(attachment);
    }
    var mimeMessage = MimeKit.MimeMessage.CreateFromMailMessage(mailMessage);
    SendGmailMessage(Encode(mimeMessage.ToString()));
}

private void SendGmailMessage(string raw) {
    var gmailMessage = new Google.Apis.Gmail.v1.Data.Message { Raw = raw };
    Google.Apis.Gmail.v1.UsersResource.MessagesResource.SendRequest request = service.Users.Messages.Send(gmailMessage, ServiceEmail);
    request.Execute();
}
'''

DATA3["Rfa50623d34"] = r'''
def _client_credential_columns():
    return [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=22), nullable=False),
        sa.Column('secret', sa.String(length=44), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client.id'],),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key'),
    ]

def upgrade():
    url = context.config.get_main_option("sqlalchemy.url")
    engine = sa.create_engine(url)
    DBSession.configure(bind=engine)
    op.create_table('client_credential', *_client_credential_columns())
    now = sa.func.now()
    clients = [
        {
            'secret': client.secret,
            'key': client.key,
            'is_active': True,
            'client_id': client.id,
            'created_at': now,
            'updated_at': now,
        }
        for client in Client.query.all()
    ]
    op.bulk_insert(ClientCredential, clients)
    for column in ('secret', 'key'):
        op.drop_column(u'client', column)
'''

DATA3["R6977f1c997"] = r'''
def scan(sentence):
    tuples = []
    for word in sentence.split():
        if word in lexicons:
            tuples.append((lexicons[word], word))
        elif word.isdigit():
            tuples.append(('number', int(word)))
        else:
            tuples.append(('error', word))
    return tuples
'''

DATA3["Rbcec8876d4"] = r'''
def contains(small, big):
    limit = len(big) - len(small) + 1
    i = 0
    while i < limit:
        if big[i:i + len(small)] == small:
            return i, i + len(small)
        i += 1
    return False
'''

DATA3["Rab8fdb571d"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char *str = malloc(100);
    strcpy(str, "test string.");
    char *token = strtok(str, " ");
    while (token != NULL) {
        printf("%s\n", token);
        token = strtok(NULL, " ");
    }
    free(str);
    return 0;
}
'''

DATA3["R6b8d361ee9"] = r'''
using System;
using System.IO;

static void Main(string[] args) {
    if (args.Length != 2) {
        Console.WriteLine("Usage:  repchar {inputfile} {outputfile}");
        return;
    }
    TransformFiles(args[0], args[1]);
}

static void TransformFiles(string inputFile, string outputFile) {
    using (StreamReader input = new StreamReader(inputFile))
    using (StreamWriter output = new StreamWriter(outputFile)) {
        int blockSize = 100000;
        char[] inBuffer = new char[blockSize];
        char[] outBuffer = new char[blockSize * 3];
        int readSize;
        while ((readSize = input.ReadBlock(inBuffer, 0, blockSize)) > 0) {
            int writeSize = TransformBlock(inBuffer, outBuffer, readSize);
            output.Write(outBuffer, 0, writeSize);
        }
    }
}
'''

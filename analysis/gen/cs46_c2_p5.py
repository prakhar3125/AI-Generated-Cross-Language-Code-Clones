DATA5 = {}

DATA5["Rb3104c30c4"] = r"""
[Route("Login")]
public HttpResponseMessage GetLogin()
{
    string scope = HttpUtility.UrlEncode("Space Seperated list of scopes");
    string redirectUri = HttpUtility.UrlEncode("http://YourWebsiteURL/api/Account/OAuthCallback");
    string accessType = "Either online or offline";
    string requestUri = $"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={_clientId}&redirect_uri={redirectUri}&scope={scope}&access_type={accessType}&approval_prompt=auto&include_granted_scopes=true";
    HttpResponseMessage response = Request.CreateResponse(HttpStatusCode.MovedPermanently);
    response.Headers.Location = new Uri(requestUri);
    return response;
}
"""

DATA5["R7ec3eaaa23"] = r"""
#include <stdio.h>

static void demo_1d(void) {
    int i, n = 6;
    arr m = makearr(1, (int[]) {n});
    for (i = 0; i < n; i++)
        *elem(m, i) = i;
    for (i = 0; i < n; i++, printf(" "))
        printf("%d", *elem(m, i));
}

static void demo_2d(void) {
    int i, j, n = 4;
    arr m = makearr(2, (int[]) {n, n});
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            *elem(m, i, j) = i * n + j;
    for (i = 0; i < n; i++, printf("\n"))
        for (j = 0; j < n; j++, printf(" "))
            printf("%d", *elem(m, i, j));
}

static void demo_3d(void) {
    int i, j, k, n = 3;
    arr m = makearr(3, (int[]) {n, n, n});
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            for (k = 0; k < n; k++)
                *elem(m, i, j, k) = (i * n + j) * n + k;
    for (i = 0; i < n; i++, printf("\n"))
        for (j = 0; j < n; j++, printf("\n"))
            for (k = 0; k < n; k++, printf(" "))
                printf("%d", *elem(m, i, j, k));
}

int main(void) {
    demo_1d();
    puts("\n");
    demo_2d();
    puts("\n");
    demo_3d();
    return 0;
}
"""

DATA5["Rf2339edd09"] = r"""
def check_len():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        position = days.index("Monday")
    except ValueError:
        return
    print("found")
    print(position)
"""

DATA5["R4dea8b0dc2"] = r"""
def graph_writer():
    data = {file: np.fromregex(file, r"\d*\.\d*", dtype=[("1", float), ("2", float), ("3", float), ("4", float)])
            for file in glob.glob("*.TXT")}
    fig, ax = plt.subplots()
    for d in data.values():
        ax.plot(d["3"], d["4"])
    plt.show()
    plt.close(fig)
"""

DATA5["Rd85db6db53"] = r"""
def unique(x):
    seen = set(x)
    return [item for item in x if item in seen]
"""

DATA5["Rbc3ee3aa80"] = r"""
boolean isPalindrome(String s) {
    if (s.length() <= 1) {
        return true;
    }
    if (s.charAt(0) != s.charAt(s.length() - 1)) {
        return false;
    }
    return isPalindrome(s.substring(1, s.length() - 1));
}
"""

DATA5["R429c244914"] = r"""
#include <stdio.h>

static double read_positive(void) {
    double num = -1.0;
    int ret;
    for (;;) {
        ret = scanf("%lf", &num);
        if (ret == 1 && num >= 0) {
            return num;
        }
        if (ret != 1) {
            while (getchar() != '\n')
                ;
            printf("Error! Please enter a number: ");
        } else {
            printf("Error! Please enter a positive number: ");
        }
    }
}

int main(void) {
    printf("Enter a positive number:");
    double num = read_positive();
    printf("Your number is %.2lf", num);
    return 0;
}
"""

DATA5["Rd469f2767c"] = r"""
#include <stdio.h>
#include <string.h>

static void slice_str(const char *str, char *buffer, size_t start, size_t end) {
    size_t j = 0;
    for (size_t i = start; i <= end && str[i] != '\0'; i++) {
        buffer[j++] = str[i];
    }
    buffer[j] = '\0';
}

int main(void) {
    const char *str = "Polly";
    size_t len = strlen(str);
    char buffer[64];
    for (int end = (int)len - 1; end >= 0; end--) {
        for (size_t start = 0; start < len; start++) {
            slice_str(str, buffer, start, (size_t)end);
            printf("%s\n", buffer);
        }
    }
    return 0;
}
"""

DATA5["R8fb5cc8c61"] = r"""
def rev(test):
    print(list(test))
    return "".join(reversed(test))
"""

DATA5["R1016fe8c54"] = r"""
#include <stdio.h>

int main(void) {
    char c;
    while (scanf("%c", &c) == 1) {
        switch (c) {
            case 'q':
            case 'Q':
                continue;
            default:
                putchar(c);
                break;
        }
    }
    return 0;
}
"""

DATA5["R7847bddc00"] = r"""
#include <stdio.h>

#define TABLES 2
#define ROWS 5
#define COLS 2

int main(void) {
    int array[TABLES][ROWS][COLS] = {
        {{10, 20}, {30, 40}, {50, 60}, {70, 80}, {90, 100}},
        {{18, 21}, {3, 4}, {5, 6}, {7, 81}, {9, 11}}
    };
    for (int i = 0; i < TABLES; ++i) {
        for (int j = 0; j < ROWS; ++j) {
            for (int k = 0; k < COLS; ++k) {
                printf("(%lu, %lu, %lu): %u\n",
                       (unsigned long)i, (unsigned long)j, (unsigned long)k,
                       (unsigned)array[i][j][k]);
            }
        }
    }
    return 0;
}
"""

DATA5["R209b6aeaa2"] = r"""
def __init__(self):
    wx.Frame.__init__(self, None, -1, "Test", size=(500, 270))
    panel = wx.Panel(self, -1)
    buttons = [("buttonStart", "Start thread", (0, 0), self.startThread),
               ("buttonChange", "Change var", (0, 30), self.changeVar)]
    for attr, label, pos, handler in buttons:
        button = wx.Button(panel, -1, label=label, pos=pos)
        setattr(self, attr, button)
        panel.Bind(wx.EVT_BUTTON, handler, id=button.GetId())
"""

DATA6 = {}

DATA6["T347"] = {"outputs": {
"python": r"""
SEPARATOR = " "
EXPONENT = 2


def _unit_get_name(number):
    return "" if number == 0 else str(number)


def _tens_get_name(number):
    return "" if number == 0 else str(number)


def _scale_get_name(exponent):
    return "hundred" if exponent == 2 else ""


def get_name(value):
    buffer = []
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[len(value) - 4:])
    else:
        number = int(value)
    number %= 1000
    if number >= 100:
        buffer.append(_unit_get_name(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(_scale_get_name(EXPONENT))
    tens_name = _tens_get_name(number % 100)
    if tens_name != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tens_name)
    return "".join(buffer)
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SEPARATOR " "

static const char *unit_get_name(int number) {
    static char buf[16];
    if (number == 0) {
        return "";
    }
    sprintf(buf, "%d", number);
    return buf;
}

static const char *tens_get_name(int number) {
    static char buf[16];
    if (number == 0) {
        return "";
    }
    sprintf(buf, "%d", number);
    return buf;
}

static const char *scale_get_name(int exponent) {
    return exponent == 2 ? "hundred" : "";
}

void get_name(const char *value, char *out, size_t outSize) {
    char buffer[128] = "";
    int number;
    size_t len = strlen(value);
    if (len == 0) {
        number = 0;
    } else if (len > 4) {
        number = atoi(value + len - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        strcat(buffer, unit_get_name(number / 100));
        strcat(buffer, SEPARATOR);
        strcat(buffer, scale_get_name(2));
    }
    const char *tensName = tens_get_name(number % 100);
    if (tensName[0] != '\0' && number >= 100) {
        strcat(buffer, SEPARATOR);
    }
    strcat(buffer, tensName);
    snprintf(out, outSize, "%s", buffer);
}
""",
"csharp": r"""
using System;
using System.Text;

public class HundredsNameProcessor
{
    private const string Separator = " ";
    private const int Exponent = 2;

    private string UnitGetName(int number)
    {
        return number == 0 ? "" : number.ToString();
    }

    private string TensGetName(int number)
    {
        return number == 0 ? "" : number.ToString();
    }

    private string ScaleGetName(int exponent)
    {
        return exponent == 2 ? "hundred" : "";
    }

    public string GetName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        int number;
        if ("".Equals(value))
        {
            number = 0;
        }
        else if (value.Length > 4)
        {
            number = int.Parse(value.Substring(value.Length - 4));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 1000;
        if (number >= 100)
        {
            buffer.Append(UnitGetName(number / 100));
            buffer.Append(Separator);
            buffer.Append(ScaleGetName(Exponent));
        }
        string tensName = TensGetName(number % 100);
        if (!"".Equals(tensName) && number >= 100)
        {
            buffer.Append(Separator);
        }
        buffer.Append(tensName);
        return buffer.ToString();
    }
}
"""
}}

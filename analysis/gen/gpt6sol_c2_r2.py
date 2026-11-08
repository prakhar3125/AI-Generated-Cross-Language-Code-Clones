DATA_R2 = {}

DATA_R2["Rb3104c30c4"] = r'''[Route ("Login")] public HttpResponseMessage GetLogin () {
    string requestUri = BuildAuthUri ();
    HttpResponseMessage response = Request.CreateResponse (HttpStatusCode.MovedPermanently);
    response.Headers.Location = new Uri (requestUri);
    return response;
}

private string BuildAuthUri () {
    string scope = HttpUtility.UrlEncode ("Space Seperated list of scopes");
    string redirectUri = HttpUtility.UrlEncode ("http://YourWebsiteURL/api/Account/OAuthCallback");
    string accessType = "Either online or offline";
    return string.Format ("https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={0}&redirect_uri={1}&scope={2}&access_type={3}&approval_prompt=auto&include_granted_scopes=true", _clientId, redirectUri, scope, accessType);
}'''

DATA_R2["R7ec3eaaa23"] = r'''typedef int *arr;

extern arr makearr (int dims, int *dims_sizes);
extern int *elem (arr a, ...);

static void demo1 () {
    int i, n = 6;
    arr m = makearr (1, (int []) {n});
    for (i = 0; i < n; i++)
        *elem (m, i) = i;
    for (i = 0; i < n; i++, printf (" "))
        printf ("%d", *elem (m, i));
}

static void demo2 () {
    int i, j, n = 4;
    arr m = makearr (2, (int []) {n, n});
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            *elem (m, i, j) = i * n + j;
    for (i = 0; i < n; i++, printf ("\n"))
        for (j = 0; j < n; j++, printf (" "))
            printf ("%d", *elem (m, i, j));
}

static void demo3 () {
    int i, j, k, n = 3;
    arr m = makearr (3, (int []) {n, n, n});
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            for (k = 0; k < n; k++)
                *elem (m, i, j, k) = (i * n + j) * n + k;
    for (i = 0; i < n; i++, printf ("\n"))
        for (j = 0; j < n; j++, printf ("\n"))
            for (k = 0; k < n; k++, printf (" "))
                printf ("%d", *elem (m, i, j, k));
}

int main () {
    demo1 ();
    puts ("\n");
    demo2 ();
    puts ("\n");
    demo3 ();
    return 0;
}'''

DATA_R2["Rf2339edd09"] = r'''DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def checkLen():
    if "Monday" not in DAYS:
        return
    print("found")
    print(DAYS.index("Monday"))'''

DATA_R2["R4dea8b0dc2"] = r'''def loadData():
    data = {}
    for file in g.glob('*.TXT'):
        data[file] = np.fromregex(file, r'\d*\.\d*',
            dtype=[('1', float), ('2', float),
            ('3', float), ('4', float)])
    return data

def graphWriter():
    data = loadData()
    fig, ax = plt.subplots()
    for d in data.values():
        ax.plot(d['3'], d['4'])
    plt.show()
    plt.close(fig)'''

DATA_R2["Rd85db6db53"] = r'''def unique(x):
    y = {item: "" for item in x}
    return [item for item in x if item in y]'''

DATA_R2["Rbc3ee3aa80"] = r'''boolean isPalindrome (String s) {
    return checkRange (s, 0, s.length () / 2);
}

boolean checkRange (String s, int i, int limit) {
    if (i >= limit) return true;
    if (s.charAt (i) != s.charAt (s.length () - i - 1)) return false;
    return checkRange (s, i + 1, limit);
}'''

DATA_R2["R429c244914"] = r'''#include <stdio.h>

static double readPositive () {
    double num;
    int ret;
    do {
        ret = scanf ("%lf", & num);
        if (ret != 1) {
            while (getchar () != '\n')
                ;
            printf ("Error! Please enter a number: ");
        } else if (num < 0) {
            printf ("Error! Please enter a positive number: ");
        }
    } while (ret != 1 || num < 0);
    return num;
}

int main () {
    printf ("Enter a positive number:");
    double num = readPositive ();
    printf ("Your number is %.2lf", num);
    return 0;
}'''

DATA_R2["Rd469f2767c"] = r'''extern void slice_str (const char *str, char *buffer, size_t start, size_t end);

int main (void) {
    const char *str = "Polly";
    unsigned int len = strlen (str);
    char buffer [len + 1];
    for (int end = (int) len - 1; end >= 0; end --) {
        for (size_t start = 0; start < len; start ++) {
            slice_str (str, buffer, start, end);
            printf ("%s\n", buffer);
        }
    }
    return 0;
}'''

DATA_R2["R8fb5cc8c61"] = r'''def rev(test):
    chars = list(test)
    result = []
    print(chars)
    while chars:
        result.append(chars.pop())
    return "".join(result)'''

DATA_R2["R1016fe8c54"] = r'''#include <stdio.h>
#include <stdbool.h>

static bool shouldPrint (char c) {
    return c != 'q' && c != 'Q';
}

int main () {
    char c;
    while (scanf ("%c", &c) > 0) {
        if (! shouldPrint (c)) {
            continue;
        }
        printf ("%c", c);
    }
    return 0;
}'''

DATA_R2["R7847bddc00"] = r'''#include <stdio.h>

#define TABLES 2
#define ROWS 5
#define COLS 2

int main () {
    int array [TABLES] [ROWS] [COLS] = {{{10, 20}, {30, 40}, {50, 60}, {70, 80}, {90, 100}}, {{18, 21}, {3, 4}, {5, 6}, {7, 81}, {9, 11}}};
    for (int i = 0; i < TABLES; i ++) {
        for (int j = 0; j < ROWS; j ++) {
            for (int k = 0; k < COLS; k ++) {
                printf ("(%lu, %lu, %lu): %u\n", (unsigned long) i, (unsigned long) j, (unsigned long) k, array [i] [j] [k]);
            }
        }
    }
    return 0;
}'''

DATA_R2["R209b6aeaa2"] = r'''def __init__(self):
    super().__init__(None, -1, "Test", size=(500, 270))
    panel = wx.Panel(self, -1)
    self.buttonStart = self._makeButton(panel, "Start thread", self.startThread, 0)
    self.buttonChange = self._makeButton(panel, "Change var", self.changeVar, 30)

def _makeButton(self, panel, label, handler, yPos):
    button = wx.Button(panel, -1, label=label, pos=(0, yPos))
    panel.Bind(wx.EVT_BUTTON, handler, id=button.GetId())
    return button'''

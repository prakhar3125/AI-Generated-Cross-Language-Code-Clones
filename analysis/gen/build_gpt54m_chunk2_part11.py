DATA_R2 = {
    "R1ff2f32faf": r'''def update(self, instance, validated_data) :
	user_data = validated_data.pop('user', {})
	self._update_nested_user(instance, user_data)
	super(ProfileSerializer, self).update(instance, validated_data)
	return instance

def _update_nested_user(self, instance, user_data) :
	user_serializer = UserSerializer(instance.user, data = user_data, partial = True)
	user_serializer.is_valid(raise_exception = True)
	user_serializer.update(instance.user, user_data)''',
    "Rb3104c30c4": r'''[Route ("Login")] public HttpResponseMessage GetLogin () {
    var queryParams = new Dictionary < string, string >
    {
        { "response_type", "code" },
        { "client_id", _clientId },
        { "redirect_uri", HttpUtility.UrlEncode ("http://YourWebsiteURL/api/Account/OAuthCallback") },
        { "scope", HttpUtility.UrlEncode ("Space Seperated list of scopes") },
        { "access_type", "Either online or offline" },
        { "approval_prompt", "auto" },
        { "include_granted_scopes", "true" }
    };
    string requestUri = "https://accounts.google.com/o/oauth2/auth?" + string.Join ("&",
        queryParams.Select (pair => pair.Key + "=" + pair.Value));
    HttpResponseMessage response = Request.CreateResponse (HttpStatusCode.MovedPermanently);
    response.Headers.Location = new Uri (requestUri);
    return response;
}''',
    "R7ec3eaaa23": r'''int main () {
    {
        int i, n = 6;
        arr m = makearr (1, (int []) {n});
        for (i = 0; i < n; i++)
            *elem (m, i) = i;
        i = 0;
        while (i < n) {
            printf ("%d", *elem (m, i));
            printf (" ");
            i++;
        }
    }
    puts ("\n");
    {
        int i, j, n = 4;
        arr m = makearr (2, (int []) {n, n});
        for (i = 0; i < n; i++)
            for (j = 0; j < n; j++)
                *elem (m, i, j) = i * n + j;
        for (i = 0; i < n; i++) {
            j = 0;
            while (j < n) {
                printf ("%d ", *elem (m, i, j));
                j++;
            }
            printf ("\n");
        }
    }
    puts ("\n");
    {
        int i, j, k, n = 3;
        arr m = makearr (3, (int []) {n, n, n});
        for (i = 0; i < n; i++)
            for (j = 0; j < n; j++)
                for (k = 0; k < n; k++)
                    *elem (m, i, j, k) = (i * n + j) * n + k;
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                k = 0;
                while (k < n) {
                    printf ("%d ", *elem (m, i, j, k));
                    k++;
                }
            }
            printf ("\n");
        }
    }
    puts ("\n");
    return 0;
}''',
    "Rf2339edd09": r'''def checkLen() :
	days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
	position = days.index("Monday") if "Monday" in days else None
	if position is not None :
		print("found")
		print(position)''',
    "R4dea8b0dc2": r'''def graphWriter() :
	data = {file : np.fromregex(file, r'\d*\.\d*',
	dtype = [('1', float), ('2', float),
	('3', float), ('4', float)])
	for file in g.glob('*.TXT')}
	fig, ax = plt.subplots()
	for d in data.values() :
		ax.plot(d ['3'], d ['4'])
	plt.show()
	plt.close(fig)''',
    "Rd85db6db53": r'''def unique(x) :
	y = dict.fromkeys(x, "")
	return [item for item in x if item in y]''',
    "Rbc3ee3aa80": r'''boolean isPalindrome (String s) {
    return checkRange (s, 0, s.length () - 1);
}

private boolean checkRange (String s, int lo, int hi) {
    if (lo >= hi) {
        return true;
    }
    if (s.charAt (lo) != s.charAt (hi)) {
        return false;
    }
    return checkRange (s, lo + 1, hi - 1);
}''',
    "R429c244914": r'''#include <stdio.h>

static double readPositiveNumber (void) {
    double num = -1;
    int ret;
    do {
        ret = scanf ("%lf", &num);
        if (num >= 0) break;
        if (ret != 1) {
            while (getchar () != '\n')
                ;
            printf ("Error! Please enter a number: ");
        }
        else {
            printf ("Error! Please enter a positive number: ");
        }
    } while (num < 0);
    return num;
}

int main () {
    printf ("Enter a positive number:");
    double num = readPositiveNumber ();
    printf ("Your number is %.2lf", num);
    return 0;
}''',
    "Rd469f2767c": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    const char *str = "Polly";
    unsigned int len = strlen (str);
    char buffer [len + 1];
    for (int end = (int) len - 1; end >= 0; end--) {
        for (unsigned int start = 0; start < len; start++) {
            slice_str (str, buffer, start, (unsigned int) end);
            printf ("%s\n", buffer);
        }
    }
    return 0;
}''',
    "R8fb5cc8c61": r'''def rev(test) :
	print(test)
	return test[::-1]''',
    "R1016fe8c54": r'''#include <stdio.h>

int main () {
    char c;
    while (scanf ("%c", &c) == 1) {
        switch (c) {
            case 'q':
            case 'Q':
                continue;
            default:
                putchar (c);
        }
    }
    return 0;
}''',
    "R7847bddc00": r'''#include <stdio.h>

int main () {
    int array [TABLES] [ROWS] [COLS] = {{{10, 20}, {30, 40}, {50, 60}, {70, 80}, {90, 100}}, {{18, 21}, {3, 4}, {5, 6}, {7, 81}, {9, 11}}};
    for (int i = 0; i < TABLES; i++) {
        for (int j = 0; j < ROWS; j++) {
            for (int k = 0; k < COLS; k++) {
                printf ("(%lu, %lu, %lu): %u\n", (unsigned long) i, (unsigned long) j, (unsigned long) k, (unsigned int) array [i] [j] [k]);
            }
        }
    }
    return 0;
}''',
    "R209b6aeaa2": r'''def __init__(self) :
	wx.Frame.__init__(self, None, - 1, "Test", size = (500, 270))
	panel = wx.Panel(self, - 1)
	self.buttonStart = self._make_button(panel, "Start thread", 0)
	self.buttonChange = self._make_button(panel, "Change var", 30)
	panel.Bind(wx.EVT_BUTTON, self.startThread, id = self.buttonStart.GetId())
	panel.Bind(wx.EVT_BUTTON, self.changeVar, id = self.buttonChange.GetId())

def _make_button(self, panel, label, y) :
	return wx.Button(panel, - 1, label = label, pos = (0, y))'''
}

# -*- coding: utf-8 -*-
DATA7 = {
"R876047a76c": r'''
def is_prime(x):
    if x < 2:
        return False
    n = 2
    while n < x - 1:
        if x % n == 0:
            return False
        n = n + 1
    return True
''',
"R61361acd54": r'''
public FileVisitResult visitFile (Path file, BasicFileAttributes attrs) throws IOException {
    printPath (file);
    return FileVisitResult.CONTINUE;
}

private void printPath (Path file) {
    System.out.println (file);
}
''',
"R8cedc05d13": r'''
public int readNumber () {
    int x;
    do {
        System.out.println ("Please enter a positive number.");
        try {
            x = keyboard.nextInt ();
        } catch (java.util.InputMismatchException e) {
            x = - 1;
        }
    } while (x < 0);
    return x;
}
''',
"Re5e59b66ff": r'''
def find_nth(string, substring, n):
    index = -1
    for _ in range(n):
        index = string.find(substring, index + 1)
    return index
''',
"R6073c71857": r'''
static void print_readings (void) {
    printf ("Temperature\t%0.1f *F\n", ((double) temperature) / 10 * 1.8 + 32);
    printf ("Pressure\t%0.2f hPa\n", ((double) pressure) / 100);
    printf ("Altitude\t%0.1f Feet\n", ((double) altitude) * 3.280839895);
}

int main (int argc, char **argv) {
    bmp085_Calibration ();
    int count = 0;
    while (count < 49) {
        temperature = bmp085_GetTemperature (bmp085_ReadUT ());
        pressure = bmp085_GetPressure (bmp085_ReadUP ());
        altitude = bmp085_Altitude (pressure);
        print_readings ();
        sleep (1800);
        count++;
    }
    return 0;
}
''',
"R271e84529a": r'''
int main (void) {
    unsigned int i;
    unsigned int x;
    scanf ("%u %u", & i, & x);
    int output = 0;
    while (x > 0) {
        if (x % 10 == x) {
            output++;
        }
        x = x / 10;
    }
    printf ("%d", output);
    return 0;
}
''',
"Re0be2a9253": r'''
def collatz(number):
    if number % 2 == 0:
        result = number // 2
    else:
        result = 3 * number + 1
    print(result)
    return result
''',
"R79546e7246": r'''
int main (void) {
    int var1 = 1048575;
    int var2 = 1048575;
    char buffer [17];
    char zeros [] = "0000000000000000";
    int len = sprintf (buffer, "%x%x", var1, var2);
    int padIndex = len < 16 ? 16 - len : 0;
    zeros [padIndex] = 0x0;
    printf ("%s%s\n", zeros, buffer);
    return 0;
}
''',
"R9936309be3": r'''
public void mouseReleased (int mod, Point loc) {
    pressLocation = null;
    dragLocation = null;
}
''',
"R8caade20c5": r'''
static void Main (string [] args) {
    Dictionary < string, string [] > skins = new Dictionary < string, string [] > ();
    skins ["ahri"] = new string [] {"Academy", "Challenger", "Dynasty", "Foxfire", "Midnight", "Popstar"};
    skins ["leesin"] = new string [] {"Traditional", "Acolyte", "Dragon Fist", "Musy Thai", "Pool Party", "SKT T1", "Knockout"};
    Console.WriteLine ("Conor's Random League of Legends Skin Selector v0.1");
    Console.WriteLine (" ");
    Console.WriteLine (" ");
    Random rnd = new Random ();
    Console.ForegroundColor = ConsoleColor.Gray;
    Console.WriteLine ("What champion would you like to select a skin for?..    ");
    string champion = Console.ReadLine ();
    Console.Write ("Press the 'enter' key for a random champion..     ");
    string question = Console.ReadLine ();
    if (! skins.TryGetValue (champion, out string [] championSkins)) {
        championSkins = skins ["leesin"];
    }
    int randomNumber = rnd.Next (championSkins.Length - 1);
    Console.WriteLine (championSkins [randomNumber]);
}
''',
"Re2915c15ad": r'''
def dashboard(request):
    form = FilterForm()
    if request.POST:
        form = FilterForm(request.POST)
        valid = form.is_valid()
    else:
        valid = False
    if valid:
        selectedplant = form.cleaned_data['selectedplant']
        sightings = Sighting.objects.filter(IMS_plant=selectedplant)
    else:
        sightings = Sighting.objects.all().order_by('date')
    context = {'sightings': sightings, 'form': form}
    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))
''',
"Re8e5ba0337": r'''
def get_info(session, title, url):
    r = session.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    phone = "N/A"
    for items in soup.select("ul.list-unstyled"):
        if len(items.select("a[href^='tel:']")):
            phone = items.select("a[href^='tel:']")[0].text
            break
    print(title, phone)
'''
}

DATA_P7 = {}

DATA_P7["R876047a76c"] = r'''
def is_prime(x) :
	return all(x % n != 0 for n in range(2, (x) - 1)) if x >= 2 else False
'''

DATA_P7["R61361acd54"] = r'''
private void logVisited (Path file) {
    System.out.println (file);
}

public FileVisitResult visitFile (Path file, BasicFileAttributes attrs) throws IOException {
    logVisited (file);
    return FileVisitResult.CONTINUE;
}
'''

DATA_P7["R8cedc05d13"] = r'''
public int readNumber () {
    System.out.println ("Please enter a positive number.");
    int x;
    try {
        x = keyboard.nextInt ();
    } catch (java.util.InputMismatchException e) {
        return readNumber ();
    }
    if (x < 0) {
        return readNumber ();
    }
    return x;
}
'''

DATA_P7["Re5e59b66ff"] = r'''
def find_nth(string, substring, n) :
	index = - 1
	for _ in range(n) :
		index = string.find(substring, index + 1)
		if index == - 1 :
			return - 1
	return index
'''

DATA_P7["R6073c71857"] = r'''
static void sampleOnce (void) {
    temperature = bmp085_GetTemperature (bmp085_ReadUT ());
    pressure = bmp085_GetPressure (bmp085_ReadUP ());
    altitude = bmp085_Altitude (pressure);
    printf ("Temperature\t%0.1f *F\n", ((double) temperature) / 10 * 1.8 + 32);
    printf ("Pressure\t%0.2f hPa\n", ((double) pressure) / 100);
    printf ("Altitude\t%0.1f Feet\n", ((double) altitude) * 3.280839895);
}

int main (int argc, char **argv) {
    bmp085_Calibration ();
    int count = 0;
    while (count < 49) {
        sampleOnce ();
        sleep (1800);
        count++;
    }
    return 0;
}
'''

DATA_P7["R271e84529a"] = r'''
int main (void) {
    unsigned int i;
    if (scanf ("%u", & i) != 1) return 0;
    unsigned int x;
    if (scanf ("%u", & x) != 1) return 0;
    int output = 0;
    for (; x > 0; x /= 10) {
        unsigned int t = x % 10;
        if (t == x) {
            output++;
        }
    }
    printf ("%d", output);
    return 0;
}
'''

DATA_P7["Re0be2a9253"] = r'''
def collatz(number) :
	result = 3 * number + 1 if number % 2 else number // 2
	print((result))
	return result
'''

DATA_P7["R79546e7246"] = r'''
static void printHexPair (int var1, int var2) {
    char buffer [17];
    char zeros [17] = "0000000000000000";
    sprintf (buffer, "%x%x", var1, var2);
    int len = (int) strlen (buffer);
    zeros[len < 16 ? 16 - len : 0] = 0x0;
    printf ("%s%s\n", zeros, buffer);
}

int main () {
    printHexPair (1048575, 1048575);
    return 0;
}
'''

DATA_P7["R9936309be3"] = r'''
public void mouseReleased (int mod, Point loc) {
    pressLocation = null;
    dragLocation = null;
}
'''

DATA_P7["R8caade20c5"] = r'''
using System;
using System.Collections.Generic;

static class SkinSelector
{
    static void Main (string [] args) {
        var skins = new Dictionary < string, string [] >
        {
            ["ahri"] = new[] {"Academy", "Challenger", "Dynasty", "Foxfire", "Midnight", "Popstar"},
            ["leeSin"] = new[] {"Traditional", "Acolyte", "Dragon Fist", "Musy Thai", "Pool Party", "SKT T1", "Knockout"}
        };
        Console.WriteLine ("Conor's Random League of Legends Skin Selector v0.1");
        Console.WriteLine (" ");
        Console.WriteLine (" ");
        Random rnd = new Random ();
        Console.ForegroundColor = ConsoleColor.Gray;
        Console.WriteLine ("What champion would you like to select a skin for?..    ");
        string champion = Console.ReadLine ();
        Console.Write ("Press the 'enter' key for a random champion..     ");
        string question = Console.ReadLine ();
        string [] pool = skins.ContainsKey (champion) ? skins [champion] : skins ["leeSin"];
        Console.WriteLine (pool [rnd.Next (pool.Length - 1)]);
    }
}
'''

DATA_P7["Re2915c15ad"] = r'''
def dashboard(request) :
	form = FilterForm(request.POST or None)
	if form.is_bound and form.is_valid() :
		sightings = Sighting.objects.filter(IMS_plant = form.cleaned_data ['selectedplant'])
	else :
		sightings = Sighting.objects.all().order_by('date')
	context = {'sightings' : sightings, 'form' : form}
	return render_to_response('dashboard.html', context, context_instance = RequestContext(request))
'''

DATA_P7["Re8e5ba0337"] = r'''
def get_info(session, title, url) :
	r = session.get(url)
	soup = BeautifulSoup(r.text, "lxml")
	for items in soup.select("ul.list-unstyled") :
		phones = items.select("a[href^='tel:']")
		if phones :
			phone = phones [0].text
			break
		phone = "N/A"
	print (title, phone)
'''

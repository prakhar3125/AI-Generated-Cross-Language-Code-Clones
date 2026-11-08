DATA7 = {
    "T430": {"outputs": {
        "python": '''import time


class ButtonPanel:
    def __init__(self, clr, init_margin):
        self.clr = clr
        self.init_margin = init_margin
        self.no_color = 0
        self.count = 0
        self.running = False

    def change_btn_foreground(self, color):
        pass

    def change_btn_margin(self, margin):
        pass

    def change_pnl_border(self, border):
        pass

    def run(self):
        try:
            self.running = True
            steps = [
                ((self.init_margin[0], self.init_margin[1] + 10, self.init_margin[2], self.init_margin[3] - 10), (0, 5, 10, 5)),
                ((self.init_margin[0], self.init_margin[1] - 10, self.init_margin[2], self.init_margin[3] + 10), (0, 0, 10, 10)),
                ((self.init_margin[0], self.init_margin[1] + 10, self.init_margin[2], self.init_margin[3] - 10), (5, 10, 5, 0)),
                ((self.init_margin[0], self.init_margin[1] - 10, self.init_margin[2], self.init_margin[3] + 10), (10, 10, 0, 0)),
                (self.init_margin, (5, 5, 5, 5)),
            ]
            self.no_color = (self.no_color + 1) % 3 if self.no_color < 2 else 0
            self.change_btn_foreground(self.clr[self.no_color])
            for margin, border in steps:
                self.change_btn_margin(margin)
                self.change_pnl_border(border)
                time.sleep(0.1)
            self.count += 1
        except Exception as e:
            print(e)''',
        "c": r'''#include <stdio.h>
#include <unistd.h>

typedef struct { int top, left, bottom, right; } Insets;

typedef struct {
    int clr[3];
    Insets init_margin;
    int no_color;
    int count;
} ButtonPanel;

static void change_btn_foreground(int color) { (void) color; }
static void change_btn_margin(Insets m) { (void) m; }
static void change_pnl_border(Insets b) { (void) b; }

static const int border_steps[5][4] = {
    { 0, 5, 10, 5 },
    { 0, 0, 10, 10 },
    { 5, 10, 5, 0 },
    { 10, 10, 0, 0 },
    { 5, 5, 5, 5 }
};

void run(ButtonPanel *panel) {
    Insets margin = panel->init_margin;
    int left_deltas[5] = { 10, -10, 10, -10, 0 };
    int right_deltas[5] = { -10, 10, -10, 10, 0 };
    for (int step = 0; step < 5; step++) {
        panel->no_color = panel->no_color < 2 ? panel->no_color + 1 : 0;
        change_btn_foreground(panel->clr[panel->no_color]);
        Insets m = margin;
        m.left += left_deltas[step];
        m.right += right_deltas[step];
        change_btn_margin(m);
        Insets border = { border_steps[step][0], border_steps[step][1], border_steps[step][2], border_steps[step][3] };
        change_pnl_border(border);
        sleep(1);
    }
    panel->count++;
}''',
        "csharp": '''using System;
using System.Threading;
using System.Windows.Forms;

public class AnimationButton : Button
{
    private readonly Color[] clr;
    private readonly Insets initMargin;
    private int noColor;
    private int count;
    private bool running;

    public AnimationButton(Color[] clr, Insets initMargin)
    {
        this.clr = clr;
        this.initMargin = initMargin;
    }

    public void Run()
    {
        try
        {
            running = true;
            noColor = noColor < 2 ? noColor + 1 : 0;
            ForeColor = clr[noColor];
            var steps = new[]
            {
                new { Border = new[] { 0, 5, 10, 5 }, Left = 10, Right = -10 },
                new { Border = new[] { 0, 0, 10, 10 }, Left = -10, Right = 10 },
                new { Border = new[] { 5, 10, 5, 0 }, Left = 10, Right = -10 },
                new { Border = new[] { 10, 10, 0, 0 }, Left = -10, Right = 10 },
                new { Border = new[] { 5, 5, 5, 5 }, Left = 0, Right = 0 }
            };
            foreach (var step in steps)
            {
                Margin = new Padding(initMargin.Left + step.Left, initMargin.Top, initMargin.Bottom, initMargin.Right + step.Right);
                Thread.Sleep(100);
            }
            count++;
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
}'''
    }},
    "R3b3bb0bfa8": {"output": '''int main(void) {
    thread_data tdata;
    pthread_t tid;
    tdata.a = 10;
    tdata.b = 32;
    if (pthread_create(&tid, NULL, myThread, (void *) &tdata) != 0) {
        fprintf(stderr, "thread creation failed\\n");
        return 1;
    }
    pthread_join(tid, NULL);
    printf("%d + %d = %d\\n", tdata.a, tdata.b, tdata.result);
    return 0;
}'''},
    "R70b5cc83a3": {"output": '''public void draw(Graphics2D g) {
    final float arrowRatio = 0.5f;
    final float arrowLength = 80.0f;
    BasicStroke stroke = (BasicStroke) g.getStroke();
    final float endX = 350.0f;
    final float veeX = endX - stroke.getLineWidth() * 0.5f / arrowRatio;

    Path2D.Float path = new Path2D.Float();
    final float waisting = 0.5f;
    final float waistX = endX - arrowLength * 0.5f;
    final float waistY = arrowRatio * arrowLength * 0.5f * waisting;
    final float arrowWidth = arrowRatio * arrowLength;

    path.moveTo(veeX - arrowLength, -arrowWidth);
    path.quadTo(waistX, -waistY, endX, 0.0f);
    path.quadTo(waistX, waistY, veeX - arrowLength, arrowWidth);
    path.lineTo(veeX - arrowLength * 0.75f, 0.0f);
    path.closePath();

    g.setColor(Color.BLUE);
    g.fill(path);
    g.setColor(Color.RED);
    g.draw(new Line2D.Float(50.0f, 0.0f, veeX - arrowLength * 0.5f, 0.0f));
}'''},
    "R9d7d058df5": {"output": '''public static void MoveDown(this TreeNode node)
{
    TreeNodeContainer container = node.Parent ?? (TreeNodeContainer)node.TreeView;
    if (container == null || !container.Nodes.Contains(node))
    {
        return;
    }
    int index = container.Nodes.IndexOf(node);
    if (index >= container.Nodes.Count - 1)
    {
        return;
    }
    container.Nodes.RemoveAt(index);
    container.Nodes.Insert(index + 1, node);
}'''},
    "R59af819289": {"output": '''def all_pairs(lst):
    pairs = []
    n = len(lst)
    if n == 0:
        return [()]
    if n == 1:
        return [tuple(lst)]
    pad = None
    if n % 2 != 0:
        for candidate in (None, True):
            if candidate not in lst:
                pad = candidate
                break
        if pad is None:
            code = 0
            while chr(code) in lst:
                code += 1
            pad = chr(code)
        lst.append(pad)
        n += 1
    for i in range(1, n):
        pair = (lst[0], lst[i])
        rest = lst[1:i] + lst[i + 1:]
        for tail in all_pairs(rest):
            group = [pair] + tail
            if pad is not None:
                for j, tu in enumerate(group):
                    if pad in tu:
                        group[j] = (tu[0],)
                        break
            pairs.append(group)
    return pairs'''},
    "Rf952aa3c99": {"output": '''public int solution(int X, int[] A) {
    int sumV = X * (X + 1) / 2;
    int sum = 0;
    Set<Integer> seen = new HashSet<>();
    for (int i = 0; i < A.length; i++) {
        if (A[i] > X || !seen.add(A[i])) continue;
        sum += A[i];
        if (sum == sumV) return i;
    }
    return -1;
}'''},
    "Rd199c3fba9": {"output": '''import re

IP_PATTERN = re.compile(
    r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}"
    r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
)


def validate_ip(ip_str):
    return bool(IP_PATTERN.match(ip_str))'''},
    "Rce31c46bb8": {"output": '''int main(void) {
    int numberOfInputs;
    if (scanf("%d", &numberOfInputs) != 1) {
        return 1;
    }
    for (int i = 0; i < numberOfInputs; i++) {
        int inputNumber;
        scanf("%d", &inputNumber);
        int prod = 1;
        int j = 1;
        while (j < inputNumber) {
            if (inputNumber % j == 0) {
                prod *= j;
            }
            j++;
        }
        printf("%04d\\n", prod % 10000);
    }
    return 0;
}'''},
    "R8655349b09": {"output": '''public static void CountbyChar(String s) {
    Map<Character, Integer> letterCountMap = new HashMap<>();
    for (char c : s.toCharArray()) {
        letterCountMap.merge(c, 1, Integer::sum);
    }
    letterCountMap.forEach((key, count) ->
        System.out.println(count + "( for" + key + " )"));
}'''},
    "R6ec2173375": {"output": '''def tree_to_list(node, order=Order.INORDER):
    if node is None:
        return []
    right = tree_to_list(node.right, order)
    down = tree_to_list(node.down, order)
    current = [node.data]
    orders = {
        Order.PREORDER: lambda: current + right + down,
        Order.INORDER: lambda: right + current + down,
        Order.POSTORDER: lambda: right + down + current,
    }
    return orders[order]()'''},
    "R998677b1ab": {"output": '''int main(void) {
    FILE *fp = fopen(FILE_NAME, "r");
    if (fp == NULL) {
        perror("fopen failed");
        exit(EXIT_FAILURE);
    }
    int i = 0;
    while (fgets(words[i], MAX_COLUMNS, fp) != NULL) {
        words[i][strlen(words[i]) - 1] = '\\0';
        i++;
    }
    fclose(fp);
    bubbleSortWordsArray(i);
    printWordsArray(i);
    return 0;
}'''},
    "Rbef72fa071": {"output": '''public static int score(final String gene1, final String gene2) {
    return score(gene1.toCharArray(), gene2.toCharArray(), 0, 0);
}'''},
    "Rc80ff5796f": {"output": '''public static boolean twoDuplicates(int[] values) {
    for (int i = 0; i < values.length; i++) {
        int counter = 0;
        for (int z = i + 1; z < values.length; z++) {
            if (values[i] == values[z] && ++counter == 2) {
                return true;
            }
        }
    }
    return false;
}'''},
    "Re56d31c78d": {"output": '''public static void Dispose(this MethodBuilder mb)
{
    if (mb == null)
    {
        return;
    }
    Type mbType = typeof(MethodBuilder);
    var fields = new[]
    {
        (Name: "m_ilGenerator", Type: typeof(ILGenerator)),
        (Name: "m_module", Type: typeof(ModuleBuilder)),
        (Name: "m_containingType", Type: (Type) null),
        (Name: "m_localSignature", Type: typeof(SignatureHelper)),
        (Name: "m_signature", Type: typeof(SignatureHelper))
    };
    foreach (var field in fields)
    {
        FieldInfo fi = mbType.GetField(field.Name, BindingFlags.Instance | BindingFlags.NonPublic);
        object value = fi.GetValue(mb);
        (value as IDisposable)?.Dispose();
        fi.SetValue(mb, null);
    }
}'''},
    "R876047a76c": {"output": '''def is_prime(x):
    if x < 2:
        return False
    if x == 2 or x == 3:
        return True
    return all(x % n for n in range(2, x - 1))'''},
    "R61361acd54": {"output": '''public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
    Path target = file;
    System.out.println(target);
    return FileVisitResult.CONTINUE;
}'''},
    "R8cedc05d13": {"output": '''public int readNumber() {
    int x = -1;
    do {
        System.out.println("Please enter a positive number.");
        try {
            x = keyboard.nextInt();
        } catch (java.util.InputMismatchException e) {
            keyboard.nextLine();
        }
    } while (x < 0);
    return x;
}'''},
    "Re5e59b66ff": {"output": '''def find_nth(string, substring, n):
    position = -1
    for _ in range(n):
        position = string.find(substring, position + 1)
        if position == -1:
            return -1
    return position'''},
    "R6073c71857": {"output": '''int main(int argc, char **argv) {
    bmp085_Calibration();
    for (int count = 0; count < 49; ++count) {
        temperature = bmp085_GetTemperature(bmp085_ReadUT());
        pressure = bmp085_GetPressure(bmp085_ReadUP());
        altitude = bmp085_Altitude(pressure);
        printf("Temperature\\t%0.1f *F\\n", ((double) temperature) / 10 * 1.8 + 32);
        printf("Pressure\\t%0.2f hPa\\n", ((double) pressure) / 100);
        printf("Altitude\\t%0.1f Feet\\n", ((double) altitude) * 3.280839895);
        sleep(1800);
    }
    return 0;
}'''},
    "R271e84529a": {"output": '''int main(void) {
    unsigned int i, x;
    if (scanf("%u", &i) != 1 || scanf("%u", &x) != 1) {
        return 1;
    }
    int output = 0;
    while (x > 0) {
        if (x % 10 == x) {
            output++;
        }
        x /= 10;
    }
    printf("%d", output);
    return 0;
}'''},
    "Re0be2a9253": {"output": '''def collatz(number):
    if number % 2:
        result = 3 * number + 1
    else:
        result = number // 2
    print(result)
    return result'''},
    "R79546e7246": {"output": '''int main(void) {
    int var1 = 1048575;
    int var2 = 1048575;
    char buffer[17];
    char zeros[17];
    sprintf(buffer, "%x%x", var1, var2);
    int len = strlen(buffer);
    memset(zeros, '0', 16);
    zeros[16] = '\\0';
    if (len < 16) {
        zeros[16 - len] = '\\0';
    } else {
        zeros[0] = '\\0';
    }
    printf("%s%s\\n", zeros, buffer);
    return 0;
}'''},
    "R9936309be3": {"output": '''public void mouseReleased(int mod, Point loc) {
    boolean wasDragging = dragLocation != null;
    if (wasDragging && pressLocation != null) {
        pressLocation = null;
    }
    pressLocation = null;
    dragLocation = null;
}'''},
    "R8caade20c5": {"output": '''static void Main(string[] args)
{
    var skins = new Dictionary<string, string[]>
    {
        ["ahri"] = new[] { "Academy", "Challenger", "Dynasty", "Foxfire", "Midnight", "Popstar" },
        ["leesin"] = new[] { "Traditional", "Acolyte", "Dragon Fist", "Musy Thai", "Pool Party", "SKT T1", "Knockout" }
    };
    Random rnd = new Random();
    Console.WriteLine("Conor's Random League of Legends Skin Selector v0.1");
    Console.WriteLine(" ");
    Console.WriteLine(" ");
    Console.ForegroundColor = ConsoleColor.Gray;
    Console.WriteLine("What champion would you like to select a skin for?..    ");
    string champion = Console.ReadLine().ToLower();
    Console.Write("Press the 'enter' key for a random champion..     ");
    Console.ReadLine();
    if (skins.TryGetValue(champion, out string[] pool))
    {
        Console.WriteLine(pool[rnd.Next(pool.Length - 1)]);
    }
    else
    {
        Console.WriteLine(skins["leesin"][rnd.Next(skins["leesin"].Length - 1)]);
    }
}'''},
    "Re2915c15ad": {"output": '''def dashboard(request):
    form = FilterForm(request.POST if request.POST else None)
    if request.POST and form.is_valid():
        selectedplant = form.cleaned_data['selectedplant']
        sightings = Sighting.objects.filter(IMS_plant=selectedplant)
    else:
        sightings = Sighting.objects.all().order_by('date')
    context = {'sightings': sightings, 'form': form}
    return render_to_response('dashboard.html', context, context_instance=RequestContext(request))'''},
    "Re8e5ba0337": {"output": '''def get_info(session, title, url):
    r = session.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    phone = "N/A"
    for items in soup.select("ul.list-unstyled"):
        phones = items.select("a[href^='tel:']")
        if phones:
            phone = phones[0].text
            break
    print(title, phone)'''},
}

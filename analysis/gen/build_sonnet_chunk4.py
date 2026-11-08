import json
T = {}
R = {}

T["T297"] = (r'''def switch_pairs(self):
    if self is None or self.next is None:
        return self
    top = self.next
    first = self
    second = first.next
    while True:
        third = second.next
        second.next = first
        first.next = third
        first = third
        print("@@@ " + str(self))
        if first is not None:
            second.next.next = first.next
            second = first.next
        if not (first is not None and second is not None):
            break
    return top''', r'''ListNode *switchPairs(ListNode *self) {
    if (self == NULL || self->next == NULL) return self;
    ListNode *top = self->next;
    ListNode *first = self;
    ListNode *second = first->next;
    do {
        ListNode *third = second->next;
        second->next = first;
        first->next = third;
        first = third;
        printf("@@@ %s\n", listNodeToString(self));
        if (first != NULL) {
            second->next->next = first->next;
            second = first->next;
        }
    } while (first != NULL && second != NULL);
    return top;
}''', r'''public ListNode SwitchPairs()
{
    if (this == null || this.next == null) return this;
    ListNode top = this.next;
    ListNode first = this;
    ListNode second = first.next;
    do
    {
        ListNode third = second.next;
        second.next = first;
        first.next = third;
        first = third;
        Console.WriteLine("@@@ " + this.ToString());
        if (first != null)
        {
            second.next.next = first.next;
            second = first.next;
        }
    } while (first != null && second != null);
    return top;
}''')

T["T252"] = (r'''def action_performed(self, e):
    try:
        with open(self.file, "rb") as is_:
            self.model = pickle.load(is_)
            self.table.set_model(self.model)
    except IOError as ex:
        traceback.print_exc()''', r'''void actionPerformed(void *e) {
    FILE *is = fopen(file, "rb");
    if (is == NULL) {
        perror("fopen");
        return;
    }
    model = readTableModel(is);
    if (model == NULL) {
        perror("read");
        fclose(is);
        return;
    }
    tableSetModel(table, model);
    fclose(is);
}''', r'''public void ActionPerformed(object sender, EventArgs e)
{
    try
    {
        using (Stream input = new BufferedStream(new FileStream(file, FileMode.Open)))
        {
            var serializer = new XmlSerializer(typeof(DataTable));
            model = (DataTable)serializer.Deserialize(input);
            table.DataSource = model;
        }
    }
    catch (IOException ex)
    {
        Console.WriteLine(ex);
    }
}''')

T["T10"] = (r'''def reverse(self, n, p):
    if n is None:
        return None
    if n.next is None:
        n.next = p
        return n
    r = self.reverse(n.next, n)
    n.next = p
    return r''', r'''Node *reverse(Node *n, Node *p) {
    if (n == NULL) return NULL;
    if (n->next == NULL) {
        n->next = p;
        return n;
    }
    Node *r = reverse(n->next, n);
    n->next = p;
    return r;
}''', r'''Node Reverse(Node n, Node p)
{
    if (n == null) return null;
    if (n.next == null)
    {
        n.next = p;
        return n;
    }
    Node r = Reverse(n.next, n);
    n.next = p;
    return r;
}''')

T["T146"] = (r'''def solution(X, A):
    hset = set()
    for i in range(len(A)):
        if A[i] <= X:
            hset.add(A[i])
        if len(hset) == X:
            return i
    return -1''', r'''int solution(int X, int A[], int n) {
    int *seen = (int *)malloc(sizeof(int) * (n > 0 ? n : 1));
    int size = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] <= X) {
            int found = 0;
            for (int j = 0; j < size; j++) {
                if (seen[j] == A[i]) { found = 1; break; }
            }
            if (!found) seen[size++] = A[i];
        }
        if (size == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}''', r'''public int Solution(int X, int[] A)
{
    HashSet<int> hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}''')

T["T110"] = (r'''def main():
    throw_catch_time = 0
    new_exception_time = 0
    new_object_time = 0
    no_stack_exception_time = 0
    for i in range(30):
        throw_catch_time += throw_catch_loop()
        new_exception_time += new_exception_loop()
        new_object_time += new_object_loop()
        no_stack_exception_time += new_no_stack_exception_loop()
    print("throwCatchTime = " + str(throw_catch_time // 30))
    print("newExceptionTime = " + str(new_exception_time // 30))
    print("newStringTime = " + str(new_object_time // 30))
    print("noStackExceptionTime = " + str(no_stack_exception_time // 30))''', r'''int main(void) {
    long long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++) {
        throwCatchTime += throwCatchLoop();
        newExceptionTime += newExceptionLoop();
        newObjectTime += newObjectLoop();
        noStackExceptionTime += newNoStackExceptionLoop();
    }
    printf("throwCatchTime = %lld\n", throwCatchTime / 30);
    printf("newExceptionTime = %lld\n", newExceptionTime / 30);
    printf("newStringTime = %lld\n", newObjectTime / 30);
    printf("noStackExceptionTime = %lld\n", noStackExceptionTime / 30);
    return 0;
}''', r'''public static void Main(string[] args)
{
    long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++)
    {
        throwCatchTime += ThrowCatchLoop();
        newExceptionTime += NewExceptionLoop();
        newObjectTime += NewObjectLoop();
        noStackExceptionTime += NewNoStackExceptionLoop();
    }
    Console.WriteLine("throwCatchTime = " + throwCatchTime / 30);
    Console.WriteLine("newExceptionTime = " + newExceptionTime / 30);
    Console.WriteLine("newStringTime = " + newObjectTime / 30);
    Console.WriteLine("noStackExceptionTime = " + noStackExceptionTime / 30);
}''')

T["T34"] = (r'''def on_activity_result(self, request_code, result_code, data):
    super().on_activity_result(request_code, result_code, data)
    if request_code == IMAGE_CAPTURE and result_code == Activity.RESULT_OK:
        db_helper = DBHelper(self)
        sql = db_helper.get_writable_database()
        sql.exec_sql("insert statement for inserting path to database")
        sql.close()
        db_helper.close()''', r'''void onActivityResult(Activity *self, int requestCode, int resultCode, Intent *data) {
    superOnActivityResult(self, requestCode, resultCode, data);
    if (requestCode == IMAGE_CAPTURE && resultCode == RESULT_OK) {
        DBHelper *dbHelper = newDBHelper(self);
        SQLiteDatabase *sql = getWritableDatabase(dbHelper);
        execSQL(sql, "insert statement for inserting path to database");
        closeDatabase(sql);
        closeDBHelper(dbHelper);
    }
}''', r'''protected override void OnActivityResult(int requestCode, Result resultCode, Intent data)
{
    base.OnActivityResult(requestCode, resultCode, data);
    if (requestCode == IMAGE_CAPTURE && resultCode == Result.Ok)
    {
        DBHelper dbHelper = new DBHelper(this);
        SQLiteDatabase sql = dbHelper.WritableDatabase;
        sql.ExecSQL("insert statement for inserting path to database");
        sql.Close();
        dbHelper.Close();
    }
}''')

T["T314"] = (r'''def get_name(self, value):
    buffer = []
    if len(value) < self.get_part_divider():
        high = ""
        low = value
    else:
        index = len(value) - self.get_part_divider()
        high = value[:index]
        low = value[index:]
    high_name = self.get_high_processor().get_name(high)
    low_name = self.get_low_processor().get_name(low)
    if high_name != "":
        buffer.append(high_name)
        buffer.append(SEPARATOR)
        buffer.append(self.get_token())
        if low_name != "":
            buffer.append(SEPARATOR)
    if low_name != "":
        buffer.append(low_name)
    return "".join(buffer)''', r'''char *getName(const char *value) {
    char *buffer = (char *)calloc(1024, 1);
    const char *high, *low;
    char *highAlloc = NULL;
    size_t len = strlen(value);
    int divider = getPartDivider();
    if ((int)len < divider) {
        highAlloc = strdup("");
        low = value;
    } else {
        int index = (int)len - divider;
        highAlloc = (char *)malloc(index + 1);
        memcpy(highAlloc, value, index);
        highAlloc[index] = '\0';
        low = value + index;
    }
    high = highAlloc;
    char *highName = getHighProcessor()->getName(high);
    char *lowName = getLowProcessor()->getName(low);
    if (strlen(highName) != 0) {
        strcat(buffer, highName);
        strcat(buffer, SEPARATOR);
        strcat(buffer, getToken());
        if (strlen(lowName) != 0) {
            strcat(buffer, SEPARATOR);
        }
    }
    if (strlen(lowName) != 0) {
        strcat(buffer, lowName);
    }
    free(highAlloc);
    return buffer;
}''', r'''public string GetName(string value)
{
    StringBuilder buffer = new StringBuilder();
    string high, low;
    if (value.Length < GetPartDivider())
    {
        high = "";
        low = value;
    }
    else
    {
        int index = value.Length - GetPartDivider();
        high = value.Substring(0, index);
        low = value.Substring(index);
    }
    string highName = GetHighProcessor().GetName(high);
    string lowName = GetLowProcessor().GetName(low);
    if (highName.Length != 0)
    {
        buffer.Append(highName);
        buffer.Append(SEPARATOR);
        buffer.Append(GetToken());
        if (lowName.Length != 0)
        {
            buffer.Append(SEPARATOR);
        }
    }
    if (lowName.Length != 0)
    {
        buffer.Append(lowName);
    }
    return buffer.ToString();
}''')

T["T22"] = (r'''def main():
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            k = 0
            while k < 9:
                if condition1:
                    print("Breaking from Loop K and J")
                    k = 9
                    j = 9
                if condition2:
                    print("Breaking from Loop K, J and I")
                    k = 9
                    j = 9
                    i = 9
                k += 1
            j += 1
        i += 1
    print("End of I , J , K")''', r'''int main(void) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            for (int k = 0; k < 9; k++) {
                if (condition1) {
                    printf("Breaking from Loop K and J\n");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    printf("Breaking from Loop K, J and I\n");
                    k = 9;
                    j = 9;
                    i = 9;
                }
            }
        }
    }
    printf("End of I , J , K\n");
    return 0;
}''', r'''public static void Main(string[] args)
{
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            for (int k = 0; k < 9; k++)
            {
                if (condition1)
                {
                    Console.WriteLine("Breaking from Loop K and J");
                    k = 9;
                    j = 9;
                }
                if (condition2)
                {
                    Console.WriteLine("Breaking from Loop K, J and I");
                    k = 9;
                    j = 9;
                    i = 9;
                }
            }
        }
    }
    Console.WriteLine("End of I , J , K");
}''')

T["T543"] = (r'''def action_performed(self, e):
    duration = int(time.time() * 1000) - self.start_time
    progress = float(duration) / float(RUN_TIME)
    self.line_point = Point()
    self.line_point.x = self.get_width() // 2
    if progress < 0.5:
        self.line_point.y = int(math.floor(self.get_height() * (progress * 2) + 0.5))
    else:
        if progress > 1.0:
            progress = 1.0
            e.get_source().stop()
            self.line_point = None
            self.ball_point = None
        else:
            self.line_point.y = int(math.floor(self.get_height() * (progress * 2) + 0.5))
            self.line_point.y = self.get_height() - (self.line_point.y - self.get_height())
            self.ball_point.y = self.line_point.y
    self.repaint()''', r'''void actionPerformed(Panel *self, ActionEvent *e) {
    long long duration = currentTimeMillis() - self->startTime;
    float progress = (float)duration / (float)RUN_TIME;
    self->linePoint = (Point *)malloc(sizeof(Point));
    self->linePoint->x = getWidth(self) / 2;
    self->linePoint->y = 0;
    if (progress < 0.5f) {
        self->linePoint->y = (int)floorf(getHeight(self) * (progress * 2) + 0.5f);
    } else {
        if (progress > 1.0f) {
            progress = 1.0f;
            stopTimer((Timer *)e->source);
            free(self->linePoint);
            self->linePoint = NULL;
            self->ballPoint = NULL;
        } else {
            self->linePoint->y = (int)floorf(getHeight(self) * (progress * 2) + 0.5f);
            self->linePoint->y = getHeight(self) - (self->linePoint->y - getHeight(self));
            self->ballPoint->y = self->linePoint->y;
        }
    }
    repaint(self);
}''', r'''public void ActionPerformed(object sender, EventArgs e)
{
    long duration = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - startTime;
    float progress = (float)duration / (float)RUN_TIME;
    linePoint = new Point();
    linePoint.X = Width / 2;
    if (progress < 0.5f)
    {
        linePoint.Y = (int)Math.Floor(Height * (progress * 2) + 0.5f);
    }
    else
    {
        if (progress > 1f)
        {
            progress = 1f;
            ((Timer)sender).Stop();
            linePoint = null;
            ballPoint = null;
        }
        else
        {
            linePoint.Y = (int)Math.Floor(Height * (progress * 2) + 0.5f);
            linePoint.Y = Height - (linePoint.Y - Height);
            ballPoint.Y = linePoint.Y;
        }
    }
    Invalidate();
}''')

T["T653"] = (r'''def action_performed(self, e):
    width_icon = ImageIcon("LR-arrows.png")
    scale_width = show_input_dialog(None, "What should the new width be?", "", QUESTION_MESSAGE, width_icon, None, None)
    height_icon = ImageIcon("UD-arrows.png")
    scale_height = show_input_dialog(None, "What should the new height be?", "", QUESTION_MESSAGE, width_icon, None, None)
    x = float(scale_width)
    y = float(scale_height)
    new_width = int(x)
    new_height = int(y)
    self.frame.set_size(new_width, new_height)
    self.scale(new_width, new_height)''', r'''void actionPerformed(void *e) {
    char scaleWidth[64], scaleHeight[64];
    ImageIcon *widthIcon = newImageIcon("LR-arrows.png");
    showInputDialog("What should the new width be?", "", widthIcon, scaleWidth, sizeof(scaleWidth));
    ImageIcon *heightIcon = newImageIcon("UD-arrows.png");
    showInputDialog("What should the new height be?", "", widthIcon, scaleHeight, sizeof(scaleHeight));
    double x = strtod(scaleWidth, NULL);
    double y = strtod(scaleHeight, NULL);
    int newWidth = (int)x;
    int newHeight = (int)y;
    frameSetSize(frame, newWidth, newHeight);
    scale(newWidth, newHeight);
}''', r'''public void ActionPerformed(object sender, EventArgs e)
{
    Image widthIcon = Image.FromFile("LR-arrows.png");
    string scaleWidth = ShowInputDialog("What should the new width be?", "", widthIcon);
    Image heightIcon = Image.FromFile("UD-arrows.png");
    string scaleHeight = ShowInputDialog("What should the new height be?", "", widthIcon);
    double x = double.Parse(scaleWidth);
    double y = double.Parse(scaleHeight);
    int newWidth = (int)x;
    int newHeight = (int)y;
    frame.Size = new Size(newWidth, newHeight);
    Scale(newWidth, newHeight);
}''')

T["T229"] = (r'''def run(self):
    try:
        with self.lock:
            for i in range(5):
                while self.id != self.token % N:
                    self.lock.wait()
                print(str(self.id) + " " + str(i))
                self.token += 1
                self.lock.notify_all()
    except KeyboardInterrupt:
        traceback.print_exc()''', r'''void *run(void *arg) {
    pthread_mutex_lock(&lock);
    for (int i = 0; i < 5; i++) {
        while (id != token % N) {
            pthread_cond_wait(&cond, &lock);
        }
        printf("%d %d\n", id, i);
        token++;
        pthread_cond_broadcast(&cond);
    }
    pthread_mutex_unlock(&lock);
    return NULL;
}''', r'''public void Run()
{
    try
    {
        lock (lockObj)
        {
            for (int i = 0; i < 5; i++)
            {
                while (id != token % N) Monitor.Wait(lockObj);
                Console.WriteLine(id + " " + i);
                token++;
                Monitor.PulseAll(lockObj);
            }
        }
    }
    catch (ThreadInterruptedException e)
    {
        Console.WriteLine(e);
    }
}''')

T["T147"] = (r'''def solution(X, A):
    empty_position = set()
    for i in range(1, X + 1):
        empty_position.add(i)
    for i in range(len(A)):
        empty_position.discard(A[i])
        if len(empty_position) == 0:
            return i
    return -1''', r'''int solution(int X, int A[], int n) {
    int size = X > 0 ? X : 0;
    char *present = (char *)malloc(size + 1);
    for (int i = 1; i <= size; i++) present[i] = 1;
    int count = size;
    for (int i = 0; i < n; i++) {
        if (A[i] >= 1 && A[i] <= size && present[A[i]]) {
            present[A[i]] = 0;
            count--;
        }
        if (count == 0) {
            free(present);
            return i;
        }
    }
    free(present);
    return -1;
}''', r'''public int Solution(int X, int[] A)
{
    ISet<int> emptyPosition = new HashSet<int>();
    for (int i = 1; i <= X; i++)
    {
        emptyPosition.Add(i);
    }
    for (int i = 0; i < A.Length; i++)
    {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0)
        {
            return i;
        }
    }
    return -1;
}''')

T["T124"] = (r'''def solution(X, A):
    length = len(A)
    if X > length:
        return -1
    is_filled = [0] * X
    jumped = 0
    for i in range(length):
        x = A[i]
        if x <= X:
            if is_filled[x - 1] == 0:
                is_filled[x - 1] = 1
                jumped += 1
                if jumped == X:
                    return i
    return -1''', r'''int solution(int X, int A[], int len) {
    if (X > len) {
        return -1;
    }
    int *isFilled = (int *)calloc(X > 0 ? X : 1, sizeof(int));
    int jumped = 0;
    for (int i = 0; i < len; i++) {
        int x = A[i];
        if (x <= X) {
            if (isFilled[x - 1] == 0) {
                isFilled[x - 1] = 1;
                jumped += 1;
                if (jumped == X) {
                    free(isFilled);
                    return i;
                }
            }
        }
    }
    free(isFilled);
    return -1;
}''', r'''public int Solution(int X, int[] A)
{
    int len = A.Length;
    if (X > len)
    {
        return -1;
    }
    int[] isFilled = new int[X];
    int jumped = 0;
    Array.Fill(isFilled, 0);
    for (int i = 0; i < len; i++)
    {
        int x = A[i];
        if (x <= X)
        {
            if (isFilled[x - 1] == 0)
            {
                isFilled[x - 1] = 1;
                jumped += 1;
                if (jumped == X)
                {
                    return i;
                }
            }
        }
    }
    return -1;
}''')

T["T614"] = (r'''def filter(self, source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    log_d("debug", str(self.mo_pattern))
    log_d("debug", "source: " + str(source) + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + str(dest) + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = str(dest)
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        log_d("debug", "lsStart : " + ls_start)
        if source is not "":
            ls_insert = str(source)
            log_d("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        log_d("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        log_d("debug", "lsText  : " + ls_text)
    lo_matcher = self.mo_pattern.fullmatch(ls_text)
    log_d("debug", "loMatcher.matches(): " + str(lo_matcher is not None) + ", lsText: " + ls_text)
    if lo_matcher is None:
        return ""
    return None''', r'''const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    char lsStart[1024] = "";
    char lsInsert[1024] = "";
    char lsEnd[1024] = "";
    char lsText[3072] = "";
    logD("debug", moPatternSource);
    logD("debug", "source/dest logged");
    strncpy(lsText, dest, sizeof(lsText) - 1);
    if (strlen(lsText) > 0) {
        strncpy(lsStart, lsText, dstart);
        lsStart[dstart] = '\0';
        logD("debug", lsStart);
        if (strcmp(source, "") != 0) {
            strncpy(lsInsert, source, sizeof(lsInsert) - 1);
            logD("debug", lsInsert);
        }
        strncpy(lsEnd, lsText + dend, sizeof(lsEnd) - 1);
        logD("debug", lsEnd);
        snprintf(lsText, sizeof(lsText), "%s%s%s", lsStart, lsInsert, lsEnd);
        logD("debug", lsText);
    }
    regmatch_t m;
    int matches = (regexec(&moPattern, lsText, 1, &m, 0) == 0
                   && m.rm_so == 0 && m.rm_eo == (regoff_t)strlen(lsText));
    logD("debug", matches ? "matches: true" : "matches: false");
    if (!matches) {
        return "";
    }
    return NULL;
}''', r'''public ICharSequence Filter(ICharSequence source, int start, int end, ISpanned dest, int dstart, int dend)
{
    string lsStart = "";
    string lsInsert = "";
    string lsEnd = "";
    string lsText = "";
    Log.D("debug", moPattern.ToString());
    Log.D("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
    lsText = dest.ToString();
    if (lsText.Length > 0)
    {
        lsStart = lsText.Substring(0, dstart);
        Log.D("debug", "lsStart : " + lsStart);
        if (!ReferenceEquals(source.ToString(), ""))
        {
            lsInsert = source.ToString();
            Log.D("debug", "lsInsert: " + lsInsert);
        }
        lsEnd = lsText.Substring(dend);
        Log.D("debug", "lsEnd   : " + lsEnd);
        lsText = lsStart + lsInsert + lsEnd;
        Log.D("debug", "lsText  : " + lsText);
    }
    Match loMatcher = moPattern.Match(lsText);
    bool matches = loMatcher.Success && loMatcher.Index == 0 && loMatcher.Length == lsText.Length;
    Log.D("debug", "loMatcher.matches(): " + matches + ", lsText: " + lsText);
    if (!matches)
    {
        return new Java.Lang.String("");
    }
    return null;
}''')

T["T592"] = (r'''def rand_nums(self, total, n):
    results = [0] * n
    if total == 0:
        return results
    total_plus1 = total + 1
    while True:
        rs = [random.getrandbits(256) for _ in range(n)]
        s = 0
        for r in rs:
            s += r
        if s == 0:
            continue
        for i in range(n):
            results[i] = (s % rs[i]) % total_plus1
        return results''', r'''int *randNums(int total, int n) {
    int *results = (int *)calloc(n, sizeof(int));
    if (total == 0) {
        return results;
    }
    mpz_t *rs = (mpz_t *)malloc(sizeof(mpz_t) * n);
    mpz_t totalPlus1, sum, tmp;
    mpz_init_set_si(totalPlus1, (long)total + 1L);
    mpz_init(sum);
    mpz_init(tmp);
    for (int i = 0; i < n; i++) mpz_init(rs[i]);
    while (1) {
        for (int i = 0; i < n; ++i) {
            mpz_urandomb(rs[i], randState, 256);
        }
        mpz_set_ui(sum, 0);
        for (int i = 0; i < n; i++) {
            mpz_add(sum, sum, rs[i]);
        }
        if (mpz_cmp_ui(sum, 0) == 0) {
            continue;
        }
        for (int i = 0; i < n; ++i) {
            mpz_mod(tmp, sum, rs[i]);
            mpz_mod(tmp, tmp, totalPlus1);
            results[i] = (int)mpz_get_si(tmp);
        }
        break;
    }
    for (int i = 0; i < n; i++) mpz_clear(rs[i]);
    free(rs);
    mpz_clear(totalPlus1);
    mpz_clear(sum);
    mpz_clear(tmp);
    return results;
}''', r'''private int[] RandNums(int total, int n)
{
    int[] results = new int[n];
    if (total == 0)
    {
        Array.Fill(results, 0);
        return results;
    }
    BigInteger[] rs = new BigInteger[n];
    BigInteger totalPlus1 = new BigInteger(total + 1L);
    while (true)
    {
        for (int i = 0; i < n; ++i)
        {
            byte[] bytes = new byte[33];
            rand.NextBytes(bytes);
            bytes[32] = 0;
            rs[i] = new BigInteger(bytes);
        }
        BigInteger sum = BigInteger.Zero;
        foreach (BigInteger r in rs)
        {
            sum = BigInteger.Add(sum, r);
        }
        if (sum.CompareTo(BigInteger.Zero) == 0)
        {
            continue;
        }
        for (int i = 0; i < n; ++i)
        {
            results[i] = (int)BigInteger.Remainder(BigInteger.Remainder(sum, rs[i]), totalPlus1);
        }
        return results;
    }
}''')

T["T633"] = (r'''def unzip(self):
    try:
        with zipfile.ZipFile(self._zip_file, "r") as zin:
            for ze in zin.infolist():
                print("Decompress: Unzipping " + ze.filename)
                if ze.is_dir():
                    self._dir_checker(ze.filename)
                else:
                    with open(self._location + ze.filename, "wb") as bufout:
                        with zin.open(ze) as entry:
                            while True:
                                buffer = entry.read(1024)
                                if not buffer:
                                    break
                                bufout.write(buffer)
        print("Unzip: Unzipping complete. path :  " + self._location)
    except Exception as e:
        print("Decompress: unzip", e)
        print("Unzip: Unzipping failed")''', r'''void unzip(void) {
    unzFile zin = unzOpen(_zipFile);
    if (zin == NULL) {
        fprintf(stderr, "Decompress: unzip failed\n");
        printf("Unzip: Unzipping failed\n");
        return;
    }
    int ok = 1;
    int rc = unzGoToFirstFile(zin);
    while (rc == UNZ_OK) {
        char name[512];
        unz_file_info info;
        unzGetCurrentFileInfo(zin, &info, name, sizeof(name), NULL, 0, NULL, 0);
        printf("Decompress: Unzipping %s\n", name);
        size_t nlen = strlen(name);
        if (nlen > 0 && name[nlen - 1] == '/') {
            _dirChecker(name);
        } else {
            char path[1024];
            snprintf(path, sizeof(path), "%s%s", _location, name);
            FILE *fout = fopen(path, "wb");
            if (fout == NULL || unzOpenCurrentFile(zin) != UNZ_OK) {
                ok = 0;
                break;
            }
            unsigned char buffer[1024];
            int read;
            while ((read = unzReadCurrentFile(zin, buffer, sizeof(buffer))) > 0) {
                fwrite(buffer, 1, read, fout);
            }
            fclose(fout);
            unzCloseCurrentFile(zin);
        }
        rc = unzGoToNextFile(zin);
    }
    unzClose(zin);
    if (ok) {
        printf("Unzip: Unzipping complete. path :  %s\n", _location);
    } else {
        printf("Unzip: Unzipping failed\n");
    }
}''', r'''public void Unzip()
{
    try
    {
        using (FileStream fin = new FileStream(_zipFile, FileMode.Open))
        using (ZipArchive zin = new ZipArchive(fin, ZipArchiveMode.Read))
        {
            foreach (ZipArchiveEntry ze in zin.Entries)
            {
                Console.WriteLine("Decompress: Unzipping " + ze.FullName);
                if (ze.FullName.EndsWith("/"))
                {
                    _dirChecker(ze.FullName);
                }
                else
                {
                    using (FileStream fout = new FileStream(_location + ze.FullName, FileMode.Create))
                    using (BufferedStream bufout = new BufferedStream(fout))
                    using (Stream entry = ze.Open())
                    {
                        byte[] buffer = new byte[1024];
                        int read = 0;
                        while ((read = entry.Read(buffer, 0, buffer.Length)) > 0)
                        {
                            bufout.Write(buffer, 0, read);
                        }
                    }
                }
            }
        }
        Console.WriteLine("Unzip: Unzipping complete. path :  " + _location);
    }
    catch (Exception e)
    {
        Console.WriteLine("Decompress: unzip " + e);
        Console.WriteLine("Unzip: Unzipping failed");
    }
}''')

T["T837"] = (r'''def run(self):
    with self.cond:
        for i in range(10):
            while len(self.list) == 0:
                print("Consumer is waiting")
                try:
                    self.cond.wait()
                except KeyboardInterrupt:
                    traceback.print_exc()
            k = self.list.pop(0)
            print("consume=" + str(k))
            self.cond.notify_all()
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                traceback.print_exc()''', r'''void *run(void *arg) {
    pthread_mutex_lock(&listLock);
    for (int i = 0; i < 10; i++) {
        while (listSize == 0) {
            printf("Consumer is waiting\n");
            pthread_cond_wait(&listCond, &listLock);
        }
        int k = listData[0];
        for (int j = 1; j < listSize; j++) {
            listData[j - 1] = listData[j];
        }
        listSize--;
        printf("consume=%d\n", k);
        pthread_cond_broadcast(&listCond);
        usleep(500 * 1000);
    }
    pthread_mutex_unlock(&listLock);
    return NULL;
}''', r'''public void Run()
{
    lock (list)
    {
        for (int i = 0; i < 10; i++)
        {
            while (list.Count == 0)
            {
                Console.WriteLine("Consumer is waiting");
                try
                {
                    Monitor.Wait(list);
                }
                catch (ThreadInterruptedException ex)
                {
                    Console.WriteLine(ex);
                }
            }
            int k = list[0];
            list.RemoveAt(0);
            Console.WriteLine("consume=" + k);
            Monitor.PulseAll(list);
            try
            {
                Thread.Sleep(500);
            }
            catch (ThreadInterruptedException ex)
            {
                Console.WriteLine(ex);
            }
        }
    }
}''')

T["T692"] = (r'''def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    elif amount < 0 or len(coins) == check_from_index:
        return 0
    else:
        with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
        without_first_coin = find_combinations_count(amount, coins, check_from_index + 1)
        return with_first_coin + without_first_coin''', r'''int findCombinationsCount(int amount, int coins[], int coinsLength, int checkFromIndex) {
    if (amount == 0) return 1;
    else if (amount < 0 || coinsLength == checkFromIndex) return 0;
    else {
        int withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, coinsLength, checkFromIndex);
        int withoutFirstCoin = findCombinationsCount(amount, coins, coinsLength, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}''', r'''int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
{
    if (amount == 0) return 1;
    else if (amount < 0 || coins.Length == checkFromIndex) return 0;
    else
    {
        int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}''')

T["T512"] = (r'''def find_min(A, c):
    x = A[c]
    position = c
    while c < len(A):
        if x > A[c]:
            x = A[c]
            position = c
        c += 1
    return position''', r'''static int findMIN(int A[], int length, int c) {
    int x = A[c];
    int position = c;
    while (c < length) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}''', r'''static int FindMIN(int[] A, int c)
{
    int x = A[c];
    int position = c;
    while (c < A.Length)
    {
        if (x > A[c])
        {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}''')

T["T14"] = (r'''def reverse(self, previous, current):
    if previous is None:
        return None
    if previous == self.head:
        previous.set_next(None)
    if current is None:
        self.head = previous
        return self.head
    else:
        temp = current.get_next()
        current.set_next(previous)
        self.reverse(current, temp)
    return None''', r'''Node *reverse(Node *previous, Node *current) {
    if (previous == NULL) return NULL;
    if (previous == head) previous->next = NULL;
    if (current == NULL) {
        head = previous;
        return head;
    } else {
        Node *temp = current->next;
        current->next = previous;
        reverse(current, temp);
    }
    return NULL;
}''', r'''public Node Reverse(Node previous, Node current)
{
    if (previous == null) return null;
    if (previous.Equals(head)) previous.SetNext(null);
    if (current == null)
    {
        head = previous;
        return head;
    }
    else
    {
        Node temp = current.GetNext();
        current.SetNext(previous);
        Reverse(current, temp);
    }
    return null;
}''')

T["T249"] = (r'''def main(*a):
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for i in range(len(st)):
        ar[ord(st[i])] = ar[ord(st[i])] + 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + "" + str(ar[i]), end="")''', r'''int main(int argc, char *argv[]) {
    char st[4096];
    int ar[256];
    memset(ar, 0, sizeof(ar));
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) st[0] = '\0';
    st[strcspn(st, "\r\n")] = '\0';
    for (int i = 0; i < (int)strlen(st); i++) {
        ar[(unsigned char)st[i]] = ar[(unsigned char)st[i]] + 1;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", ch);
            } else {
                printf("%c%d", ch, ar[i]);
            }
        }
    }
    return 0;
}''', r'''public static void Main(string[] a)
{
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    for (int i = 0; i < st.Length; i++)
    {
        ar[st[i]] = ar[st[i]] + 1;
    }
    for (int i = 0; i < 256; i++)
    {
        char ch = (char)i;
        if (ar[i] > 0)
        {
            if (ar[i] == 1)
            {
                Console.Write(ch);
            }
            else
            {
                Console.Write(ch + "" + ar[i]);
            }
        }
    }
}''')

T["T372"] = (r'''def capitalize(s):
    if s is None or len(s) == 0:
        return ""
    first = s[0]
    if first.isupper():
        return s
    else:
        return first.upper() + s[1:]''', r'''static char *capitalize(const char *s) {
    if (s == NULL || strlen(s) == 0) {
        return strdup("");
    }
    char *result = strdup(s);
    if (!isupper((unsigned char)result[0])) {
        result[0] = (char)toupper((unsigned char)result[0]);
    }
    return result;
}''', r'''private string Capitalize(string s)
{
    if (s == null || s.Length == 0)
    {
        return "";
    }
    char first = s[0];
    if (char.IsUpper(first))
    {
        return s;
    }
    else
    {
        return char.ToUpper(first) + s.Substring(1);
    }
}''')

T["T60"] = (r'''def is_permutation(str1, str2):
    x = sorted(str1)
    y = sorted(str2)
    if x == y:
        return True
    return False''', r'''static int cmpChar(const void *a, const void *b) {
    return (*(const char *)a) - (*(const char *)b);
}

bool isPermutation(const char *str1, const char *str2) {
    char *x = strdup(str1);
    char *y = strdup(str2);
    qsort(x, strlen(x), sizeof(char), cmpChar);
    qsort(y, strlen(y), sizeof(char), cmpChar);
    bool result = strcmp(x, y) == 0;
    free(x);
    free(y);
    if (result) return true;
    return false;
}''', r'''public static bool IsPermutation(string str1, string str2)
{
    char[] x = str1.ToCharArray();
    char[] y = str2.ToCharArray();
    Array.Sort(x);
    Array.Sort(y);
    if (x.SequenceEqual(y)) return true;
    return false;
}''')

T["T172"] = (r'''def is_available(self):
    url = "URL HERE"
    connection = http.client.HTTPConnection(urlparse(url).netloc, timeout=10)
    connection.request("GET", urlparse(url).path or "/", headers={"Connection": "close"})
    if connection.getresponse().status == 200:
        return True
    else:
        return False''', r'''bool isAvailable(void) {
    CURL *curl = curl_easy_init();
    long code = 0;
    curl_easy_setopt(curl, CURLOPT_URL, "URL HERE");
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 10000L);
    struct curl_slist *headers = curl_slist_append(NULL, "Connection: close");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &code);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    if (code == 200) {
        return true;
    } else return false;
}''', r'''public bool IsAvailable()
{
    Uri url = new Uri("URL HERE");
    HttpWebRequest connection = (HttpWebRequest)WebRequest.Create(url);
    connection.KeepAlive = false;
    connection.Timeout = 10000;
    using (HttpWebResponse response = (HttpWebResponse)connection.GetResponse())
    {
        if ((int)response.StatusCode == 200)
        {
            return true;
        }
        else return false;
    }
}''')

T["T713"] = (r'''def set_cursor_color(view, color):
    try:
        drawable_res_id = getattr(view, "mCursorDrawableRes")
        editor = getattr(view, "mEditor")
        drawable = ContextCompat.get_drawable(view.get_context(), drawable_res_id)
        drawable.set_color_filter(color, PorterDuff.Mode.SRC_IN)
        drawables = [drawable, drawable]
        setattr(editor, "mCursorDrawable", drawables)
    except Exception:
        pass''', r'''void setCursorColor(EditText *view, int color) {
    int drawableResId = getIntField(view, "mCursorDrawableRes");
    void *editor = getObjectField(view, "mEditor");
    if (drawableResId < 0 || editor == NULL) {
        return;
    }
    Drawable *drawable = getDrawable(getContext(view), drawableResId);
    if (drawable == NULL) {
        return;
    }
    setColorFilter(drawable, color, PORTER_DUFF_SRC_IN);
    Drawable *drawables[2] = {drawable, drawable};
    setObjectField(editor, "mCursorDrawable", drawables);
}''', r'''public static void SetCursorColor(EditText view, int color)
{
    try
    {
        FieldInfo field = typeof(TextView).GetField("mCursorDrawableRes", BindingFlags.NonPublic | BindingFlags.Instance);
        int drawableResId = (int)field.GetValue(view);
        field = typeof(TextView).GetField("mEditor", BindingFlags.NonPublic | BindingFlags.Instance);
        object editor = field.GetValue(view);
        Drawable drawable = ContextCompat.GetDrawable(view.Context, drawableResId);
        drawable.SetColorFilter(color, PorterDuff.Mode.SrcIn);
        Drawable[] drawables = { drawable, drawable };
        field = editor.GetType().GetField("mCursorDrawable", BindingFlags.NonPublic | BindingFlags.Instance);
        field.SetValue(editor, drawables);
    }
    catch (Exception)
    {
    }
}''')

R["Rbf38b9a69d"] = r'''private void transform (XSSFWorkbook workbookOld, HSSFWorkbook workbookNew, Integer hash, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    styleNew.setVerticalAlignment (styleOld.getVerticalAlignment ());
    styleNew.setWrapText (styleOld.getWrapText ());
    styleNew.setLocked (styleOld.getLocked ());
    styleNew.setIndention (styleOld.getIndention ());
    styleNew.setHidden (styleOld.getHidden ());
    short dataFormat = this.transform (workbookOld, workbookNew, styleOld.getDataFormat ());
    styleNew.setDataFormat (dataFormat);
    styleNew.setFont (this.transform (workbookNew, (XSSFFont) styleOld.getFont ()));
    styleNew.setFillPattern (styleOld.getFillPattern ());
    styleNew.setFillForegroundColor (styleOld.getFillForegroundColor ());
    styleNew.setFillBackgroundColor (styleOld.getFillBackgroundColor ());
    styleNew.setBorderTop (styleOld.getBorderTop ());
    styleNew.setBorderRight (styleOld.getBorderRight ());
    styleNew.setBorderLeft (styleOld.getBorderLeft ());
    styleNew.setBorderBottom (styleOld.getBorderBottom ());
    styleNew.setAlignment (styleOld.getAlignment ());
    this.styleMap.put (hash, styleNew);
}'''

R["Rb9c3635eed"] = r'''public static void main (String args []) {
    inp = new Scanner (System.in);
    String str = inp.nextLine ();
    char [] chars = str.toCharArray ();
    List < Character > arrlist = new ArrayList < Character > ();
    for (char c : chars) {
        arrlist.add (c);
    }
    int idx = 0;
    while (idx < chars.length) {
        char current = chars [idx];
        int freq = Collections.frequency (arrlist, current);
        System.out.println ("Frequency of " + current + "  is:   " + freq);
        idx ++;
    }
}'''

R["Rea67761d7d"] = r'''public static void main (String [] args) {
    String [] samples = {"", null, "Starts with upper case", "starts with lower case"};
    for (String sample : samples) {
        System.out.println (startWithUpperCase (sample));
    }
}'''

R["R357f96f327"] = r'''public static DataTable GetWorksheetAsDataTable(ExcelWorksheet worksheet) {
    DataTable dt = new DataTable(worksheet.Name);
    dt.Columns.AddRange(GetDataColumns(worksheet).ToArray());
    const int headerOffset = 1;
    int width = dt.Columns.Count;
    int depth = GetTableDepth(worksheet, headerOffset);
    int rowNum = 1;
    while (rowNum <= depth) {
        DataRow row = dt.NewRow();
        int col = 0;
        while (col < width) {
            object val = worksheet.Cells[rowNum + headerOffset, col + 1].Value;
            if (val == null) {
                row[col] = null;
            } else {
                row[col] = val.ToString();
            }
            col++;
        }
        dt.Rows.Add(row);
        rowNum++;
    }
    return dt;
}'''

R["Re3d1dfab68"] = r'''def create_lookup_list(messages, labels) :
  return [{"message": message, "label": label} for message, label in zip(messages, labels)]'''

R["Rfe9a432a46"] = r'''public override void OnException (ExceptionContext filterContext) {
    var response = filterContext.HttpContext.Response;
    var routeValues = filterContext.RouteData.Values;
    var model = new HandleErrorInfo (filterContext.Exception, (string) routeValues ["controller"], (string) routeValues ["action"]);
    filterContext.ExceptionHandled = true;
    response.ClearContent ();
    response.TrySkipIisCustomErrors = true;
    var viewData = new ViewDataDictionary < HandleErrorInfo > (model);
    filterContext.Result = new ViewResult {
        ViewName = View,
        MasterName = Master,
        ViewData = viewData,
        TempData = filterContext.Controller.TempData
    };
    filterContext.Exception = null;
}'''

R["Rb8f6c8b5d0"] = r'''int main (void) {
    char s [1000], alp [1000];
    int num [1000];
    int m = 0, n = 0;
    int i, j;
    unsigned char ch;
    scanf ("%999[^\n]", s);
    i = 0;
    while ((ch = s[i]) != 0) {
        if (isalpha (ch)) {
            alp[n] = s[i];
            n++;
        }
        else if (!isdigit (ch)) {
            printf ("include invalid character (%c).\n", ch);
            return -1;
        }
        else {
            num[m] = 0;
            for (; isdigit (ch = s[i]); i++) {
                num[m] = num[m] * 10 + s[i] - '0';
            }
            m++;
            i--;
        }
        i++;
    }
    for (i = 0; i < m; i++) {
        j = 0;
        while (j < num[i]) {
            putchar (alp[i]);
            j++;
        }
    }
    puts ("");
    return 0;
}'''

R["R8b80f20070"] = r'''int main () {
    double v;
    if (scanf ("%lf", &v) != 1) {
        printf ("read failed\n");
        return 0;
    }
    printf ("%lf\n", v);
    return 0;
}'''

R["R4e335703d6"] = r'''int main () {
    char s [SIZE];
    char *months [] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    printf ("enter the month : ");
    gets (s);
    int result = get_month (s, months);
    if (!result) {
        printf ("%s invalid\n", s);
        return 0;
    }
    printf ("%s - %d.  is the month of the year.\n", s, result);
    return 0;
}'''

R["R9fdda16e3c"] = r'''int main () {
    int num, x, tmp, sum = 0;
    scanf ("%d", & num);
    tmp = num;
    printf ("Factors are: ");
    do {
        x = getFirst (tmp);
        printf ("%d ", x);
        if (x != tmp)
            tmp /= x;
    } while (x != tmp);
    printf ("\n");
    printf ("Sum of factors is: ");
    tmp = num;
    do {
        x = getFirst (tmp);
        printf ("%d ", x);
        sum += x;
        if (x != tmp) {
            printf ("+ ");
            tmp /= x;
        }
    } while (x != tmp);
    printf ("= %d\n", sum);
}'''

R["R8c49ec85d8"] = r'''public void filter (String [] words, String text) {
    for (String word : words) {
        if (!text.toLowerCase ().contains (word.toLowerCase ())) {
            continue;
        }
        System.out.println (text);
        return;
    }
}'''

R["R8d187f48ce"] = r'''def traceit(frame, event, arg) :
    if event != "line" :
        return traceit
    filename = frame.f_globals ["__file__"]
    if filename == "<stdin>" :
        filename = "traceit.py"
    if filename[-4:] in (".pyc", ".pyo") :
        filename = filename [: - 1]
    lineno = frame.f_lineno
    name = frame.f_globals ["__name__"]
    line = linecache.getline(filename, lineno)
    print "%s:%s:%s: %s" % (name, lineno, frame.f_code.co_name, line.rstrip())
    return traceit'''

R["R00a4c22b00"] = r'''def roundrobin(* iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    iter_items = []
    for it in itertools.cycle(list(iterables)):
        data = next(it)
        iter_items.append(data)
        yield data'''

R["R2710a37612"] = r'''public static final void main (String...aArgs) {
    log ("Generating 10 random integers in range 1..10.");
    final int START = 1, END = 10;
    Random randomGenerator = new Random ();
    int remaining = 10;
    while (remaining > 0) {
        showRandomInteger (START, END, randomGenerator);
        remaining --;
    }
    log ("Done");
}'''

R["Rf6f525dc34"] = r'''static void Main (string [] args) {
    ProcessStartInfo procStartInfo = new ProcessStartInfo (getLibreOfficePath(), string.Format (CreateParamString (args)));
    Process process = new Process () {StartInfo = procStartInfo,};
    SetProcessStartInfoProperties(procStartInfo);
    ExecuteProcess(process);
    ValidateProcessExitCode(process);
}'''

R["R6ea07c8787"] = r'''public static void Rename (this FileSystemInfo item, string newName) {
    if (item is FileInfo fileInfo) {
        fileInfo.Rename (newName);
    } else if (item is DirectoryInfo directoryInfo) {
        directoryInfo.Rename (newName);
    } else if (item == null) {
        throw new ArgumentNullException ("item");
    } else {
        throw new ArgumentException ("Item", "Unexpected subclass of FileSystemInfo " + item.GetType ());
    }
}'''

R["Rd744148380"] = r'''public void onRequestPermissionsResult (int requestCode, String permissions [], int [] grantResults) {
    super.onRequestPermissionsResult (requestCode, permissions, grantResults);
    if (grantResults.length > 0) {
        int first = grantResults [0];
        if (first == PackageManager.PERMISSION_GRANTED) {
            return;
        }
        if (first == PackageManager.PERMISSION_DENIED) {
            return;
        }
    }
}'''

R["R51669e3825"] = r'''def __init__(self) :
    self.secondsRemaining, self.lastTick = 10.0, 0
    self.isPaused = self.isRunning = False
    self.keepGoing = True'''

R["Ra853448a33"] = r'''int main () {
    int counter = 0;
    struct termios orig_attr, new_attr;
    pthread_t pid;
    tcgetattr (fileno (stdin), & orig_attr);
    new_attr = orig_attr;
    new_attr.c_lflag = new_attr.c_lflag & ~(ICANON | ECHO);
    tcsetattr (fileno (stdin), TCSANOW, & new_attr);
    if (pthread_create (&pid, NULL, thread, &counter) != 0) {
        fprintf (stderr, "Create thread failed");
        exit (1);
    }
    for (;;) {
        getchar ();
        __sync_add_and_fetch (& counter, 1);
        printf ("add: %d\n", counter);
    }
    return 0;
}'''

R["R3713a963cf"] = r'''def json_scan(json_obj, key) :
    result = None
    for element in json_obj :
        value = json_obj [element]
        if str(element) == key :
            result = value
        elif type(value) == DictType :
            result = json_scan(value, key)
        elif type(value) == ListType :
            result = json_scan(element, key)
    return result'''

R["R4474610115"] = r'''int main (void) {
    int start;
    if (scanf ("%d", &start) != 1)
        exit (1);
    int last = start;
    int value;
    while (scanf ("%d", &value) == 1)
        last = value;
    int i = start;
    while (i <= last) {
        printf ("%d\n", i);
        i++;
    }
}'''

R["Refd906fcb2"] = r'''long pow (long a, int b) {
    if (b == 0) return 1;
    long rest = pow (a * a, b / 2);
    return isEven (b) ? rest : a * rest;
}'''

R["Rd40ca7a94c"] = r'''public final void contextDestroyed (ServletContextEvent sce) {
    final ClassLoader cl = Thread.currentThread ().getContextClassLoader ();
    for (Enumeration < Driver > drivers = DriverManager.getDrivers (); drivers.hasMoreElements ();) {
        Driver driver = drivers.nextElement ();
        if (driver.getClass ().getClassLoader () != cl) {
            log.trace ("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver);
            continue;
        }
        try {
            log.info ("Deregistering JDBC driver {}", driver);
            DriverManager.deregisterDriver (driver);
        } catch (SQLException ex) {
            log.error ("Error deregistering JDBC driver {}", driver, ex);
        }
    }
}'''

R["Rfaf0b51ec8"] = r'''def combinations(iterable, r) :
    pool = tuple(iterable)
    n = len(pool)
    if r > n :
        return
    indices = list(range(r))
    while True :
        i = r - 1
        while i >= 0 and indices [i] == i + n - r :
            i -= 1
        if i < 0 :
            return
        indices [i] += 1
        for j in range(i + 1, r) :
            indices [j] = indices [j - 1] + 1
        chosen = tuple(pool [k] for k in indices)
        if not (1 in chosen and 3 in chosen) :
            yield chosen'''

R["R3c52337f3a"] = r'''internal static string GetIPAddress (HttpRequestBase request) {
    string forwarded = request.Headers ["Forwarded"];
    if (!String.IsNullOrEmpty (forwarded)) {
        string [] segments = forwarded.Split (',') [0].Split (';');
        for (int s = 0; s < segments.Length; s++) {
            string [] pair = segments [s].Trim ().Split ('=');
            if (pair.Length != 2 || !pair [0].Equals ("for", StringComparison.OrdinalIgnoreCase)) {
                continue;
            }
            string ip = pair [1].Trim ('"');
            if (ip.Length > 0 && ip [0] == '[') {
                return ip.Substring (1, ip.IndexOf (']') - 1);
            }
            int colon = ip.IndexOf (':');
            return colon == - 1 ? ip : ip.Substring (0, colon);
        }
    }
    string xForwardedFor = request.Headers ["X-Forwarded-For"];
    if (String.IsNullOrEmpty (xForwardedFor)) {
        return request.UserHostAddress;
    }
    return xForwardedFor.Split (',') [0];
}'''

ids = ["T297","T252","T10","T146","T110","T34","T314","T22","T543","T653","T229","T147","T124","T614","T592","T633","T837","T692","T512","T14","T249","T372","T60","T172","T713"]
rids = list(R.keys())
out = []
for i in ids:
    p, c, cs = T[i]
    out.append({"id": i, "outputs": {"python": p, "c": c, "csharp": cs}})
for i in rids:
    out.append({"id": i, "output": R[i]})
with open(r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/out/sonnet_chunk4.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(len(out))

DATA_T4 = {}

DATA_T4["T633"] = {"outputs": {
"python": """import zipfile


def unzip(self):
    try:
        with zipfile.ZipFile(self.zip_file) as zin:
            for ze in zin.infolist():
                log_verbose("Decompress", "Unzipping " + ze.filename)
                if ze.is_dir():
                    self.dir_checker(ze.filename)
                else:
                    target = self.location + ze.filename
                    with zin.open(ze) as src, open(target, "wb") as fout:
                        while True:
                            chunk = src.read(1024)
                            if not chunk:
                                break
                            fout.write(chunk)
        log_debug("Unzip", "Unzipping complete. path :  " + self.location)
    except Exception as e:
        log_error("Decompress", "unzip", e)
        log_debug("Unzip", "Unzipping failed")
""",
"c": """void unzip(void) {
    char cmd[1024];
    FILE *fp;
    ZipEntry *ze = NULL;
    ZipStream *zin = zip_open(zip_file);
    if (zin == NULL) {
        log_error("Decompress", "unzip", NULL);
        log_debug("Unzip", "Unzipping failed");
        return;
    }
    while ((ze = zip_next_entry(zin)) != NULL) {
        log_verbose("Decompress", "Unzipping %s", ze->name);
        if (ze->is_directory) {
            dir_checker(ze->name);
        } else {
            FILE *fout = fopen(join_path(location, ze->name), "wb");
            char buffer[1024];
            int read;
            while ((read = zip_entry_read(zin, buffer, sizeof(buffer))) > 0) {
                fwrite(buffer, 1, read, fout);
            }
            fclose(fout);
            zip_close_entry(zin);
        }
    }
    zip_stream_close(zin);
    log_debug("Unzip", "Unzipping complete. path :  %s", location);
}
""",
"csharp": """public void Unzip() {
    try {
        using (var fin = new FileStream(zipFile, FileMode.Open, FileAccess.Read))
        using (var zin = new ZipInputStream(fin)) {
            ZipEntry ze;
            while ((ze = zin.GetNextEntry()) != null) {
                Log.Verbose("Decompress", "Unzipping " + ze.Name);
                if (ze.IsDirectory) {
                    DirChecker(ze.Name);
                } else {
                    var target = location + ze.Name;
                    var dirName = Path.GetDirectoryName(target);
                    if (!string.IsNullOrEmpty(dirName)) Directory.CreateDirectory(dirName);
                    using (var fout = new BufferedStream(new FileStream(target, FileMode.Create))) {
                        var buffer = new byte[1024];
                        int read;
                        while ((read = zin.Read(buffer, 0, buffer.Length)) > 0) {
                            fout.Write(buffer, 0, read);
                        }
                    }
                }
            }
        }
        Log.Debug("Unzip", "Unzipping complete. path :  " + location);
    } catch (Exception e) {
        Log.Error("Decompress", "unzip", e);
        Log.Debug("Unzip", "Unzipping failed");
    }
}
"""}}

DATA_T4["T837"] = {"outputs": {
"python": """def run(self):
    with list_condition:
        for i in range(10):
            while not shared_list:
                print("Consumer is waiting")
                list_condition.wait()
            k = shared_list.pop(0)
            print("consume=" + str(k))
            list_condition.notify_all()
            time.sleep(0.5)
""",
"c": """pthread_mutex_t list_m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t list_c = PTHREAD_COND_INITIALIZER;

void *run(void *arg) {
    pthread_mutex_lock(&list_m);
    for (int i = 0; i < 10; i++) {
        while (list_size == 0) {
            printf("Consumer is waiting\\n");
            pthread_cond_wait(&list_c, &list_m);
        }
        int k = list_remove_at(0);
        printf("consume=%d\\n", k);
        pthread_cond_broadcast(&list_c);
        struct timespec ts = {0, 500 * 1000 * 1000};
        nanosleep(&ts, NULL);
    }
    pthread_mutex_unlock(&list_m);
    return NULL;
}
""",
"csharp": """public void Run() {
    lock (list) {
        for (int i = 0; i < 10; i++) {
            while (list.Count == 0) {
                Console.WriteLine("Consumer is waiting");
                try {
                    Monitor.Wait(list);
                } catch (SynchronizationLockException ex) {
                    Console.Error.WriteLine(ex.StackTrace);
                }
            }
            int k = list[0];
            list.RemoveAt(0);
            Console.WriteLine("consume=" + k);
            Monitor.PulseAll(list);
            Thread.Sleep(500);
        }
    }
}
"""}}

DATA_T4["T692"] = {"outputs": {
"python": """def find_combinations_count(amount, coins, check_from_index=0):
    if amount == 0:
        return 1
    if amount < 0 or check_from_index == len(coins):
        return 0
    with_first = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
    without_first = find_combinations_count(amount, coins, check_from_index + 1)
    return with_first + without_first
""",
"c": """int findCombinationsCount(int amount, int coins[], int ncoins, int checkFromIndex) {
    if (amount == 0) return 1;
    if (amount < 0 || ncoins == checkFromIndex) return 0;
    int withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, ncoins, checkFromIndex);
    int withoutFirstCoin = findCombinationsCount(amount, coins, ncoins, checkFromIndex + 1);
    return withFirstCoin + withoutFirstCoin;
}
""",
"csharp": """public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex) {
    switch (amount) {
        case 0:
            return 1;
        default:
            if (amount < 0 || coins.Length == checkFromIndex) return 0;
            int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
            int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
            return withFirstCoin + withoutFirstCoin;
    }
}
"""}}

DATA_T4["T512"] = {"outputs": {
"python": """def find_min(a, c):
    x = a[c]
    position = c
    for idx in range(c, len(a)):
        if x > a[idx]:
            x = a[idx]
            position = idx
    return position
""",
"c": """int findMIN(int A[], int len, int c) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}
""",
"csharp": """static int FindMIN(int[] A, int c) {
    int x = A[c];
    int position = c;
    for (int i = c; i < A.Length; i++) {
        if (x > A[i]) {
            x = A[i];
            position = i;
        }
    }
    return position;
}
"""}}

DATA_T4["T14"] = {"outputs": {
"python": """def reverse(previous, current):
    if previous is None:
        return None
    if previous == head:
        previous.next = None
    if current is None:
        head = previous
        return head
    temp = current.next
    current.next = previous
    reverse(current, temp)
    return None
""",
"c": """struct Node {
    int value;
    struct Node *next;
};

struct Node *head;

struct Node *reverse(struct Node *previous, struct Node *current) {
    if (previous == NULL) return NULL;
    if (previous == head) previous->next = NULL;
    if (current == NULL) {
        head = previous;
        return head;
    }
    struct Node *temp = current->next;
    current->next = previous;
    reverse(current, temp);
    return NULL;
}
""",
"csharp": """public Node Reverse(Node previous, Node current) {
    if (previous == null) return null;
    if (previous.Equals(head)) previous.Next = null;
    if (current == null) {
        head = previous;
        return head;
    }
    Node temp = current.Next;
    current.Next = previous;
    Reverse(current, temp);
    return null;
}
"""}}

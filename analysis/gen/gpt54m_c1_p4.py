# gpt-5.4-mini chunk 1 part 4: refactors 14-25
DATA4 = {}

DATA4["Rc34ff3d7d3"] = r'''
private void initData() {
    Object [][] rows = {
        {"Active", 1L, 1, 0},
        {"Dropped", 2L, 2, 1},
        {"Pending", 3L, 3, 2},
        {"Failed", 4L, 4, 3},
        {"Completed", 5L, 5, 4},
        {"Queued", 6L, 6, 5},
        {"Retry", 7L, 7, 6},
        {"Cancelled", 8L, 8, 7},
        {"Expired", 9L, 9, 8},
        {"Held", 10L, 10, 9},
        {"Aborted", 11L, 11, 10},
        {"Archived", 12L, 12, 11}
    };
    for (Object [] row : rows) {
        testData.add(new EventStatus((String) row[0], (long)(Long) row[1], (int)(Integer) row[2], (int)(Integer) row[3]));
    }
    Set<String> uniqueNames = new LinkedHashSet<>();
    for (EventStatus status : testData) {
        uniqueNames.add(status.getName());
    }
    catArray = uniqueNames.toArray(new String[0]);
}
'''

DATA4["R73c281cc62"] = r'''
private static List<T[]> EnumerateCombos<T>(IEnumerable<T> items, int threshold) {
    List<T[]> results = new List<T[]>();
    BuildCombos(items, new List<T>(), 0, threshold, results);
    return results;
}

private static void BuildCombos<T>(IEnumerable<T> items, List<T> currentCombo, int startIndex, int threshold, List<T[]> results) {
    if (currentCombo.Count >= threshold) {
        results.Add(currentCombo.ToArray());
    }
    IList<T> itemList = items as IList<T> ?? items.ToList();
    for (int i = startIndex; i < itemList.Count; i++) {
        currentCombo.Add(itemList[i]);
        BuildCombos(itemList, currentCombo, i + 1, threshold, results);
        currentCombo.RemoveAt(currentCombo.Count - 1);
    }
}
'''

DATA4["R91d065403d"] = r'''
public static File createTempDir(String baseDir, String baseName) {
    File result = attemptCreate(baseDir, baseName);
    if (result == null) {
        throw new IllegalStateException("Failed to create directory within " + MAX_ATTEMPTS + " attempts (tried " + baseName + "0 to " + baseName + (MAX_ATTEMPTS - 1) + ").");
    }
    return result;
}

private static File attemptCreate(String baseDir, String baseName) {
    for (int i = 0; i < MAX_ATTEMPTS; i++) {
        File tempDir = new File(baseDir, baseName + i);
        if (tempDir.mkdir()) {
            return tempDir;
        }
    }
    return null;
}
'''

DATA4["R8cfbeb65a3"] = r'''
public List<ReportFile> ReadFiles(DateTime dateStart, DateTime dateEnd) {
    var reportList = new List<ReportFile>();
    for (DateTime date = dateStart; date < dateEnd; date = date.AddDays(1)) {
        reportList.AddRange(FilesForDay(fileNames, date));
    }
    return reportList;
}

private static IEnumerable<ReportFile> FilesForDay(List<string> fileNames, DateTime date) {
    foreach (string name in fileNames) {
        var reportFile = new ReportFile { FileName = name, Date = date };
        if (File.Exists(reportFile.FullPath)) {
            yield return reportFile;
        }
    }
}
'''

DATA4["R8f617cb401"] = r'''
#include <stdio.h>

int main(void) {
    int data[9];
    int i = 0;
    do {
        data[i] = i;
        i++;
    } while (i < 9);
    for (int j = 0; j < 9; j++) {
        printf("%d ", data[j]);
    }
    printf("\n");
    return 0;
}
'''

DATA4["R593eed57e6"] = r'''
using System;

static void Main(string[] args) {
    int n = Convert.ToInt32(args[0]);
    bool by3 = n % 3 == 0;
    bool by5 = n % 5 == 0;
    if (by3 && by5) {
        Console.WriteLine("fizzbuzz");
    } else if (by3) {
        Console.WriteLine("fizz");
    } else if (by5) {
        Console.WriteLine("buzz");
    } else {
        Console.WriteLine(n);
    }
}
'''

DATA4["Rc5e1a6cc9a"] = r'''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

public class Crawler {
    private Queue<string> queue = new Queue<string>();
    private string[] websites = new string[5];

    void initialize(string[] sites, int threadCountFromTheUser) {
        websites = sites;
        Array.ForEach(websites, queue.Enqueue);
        List<Thread> threads = Enumerable.Range(0, threadCountFromTheUser).Select(_ => new Thread(work)).ToList();
        foreach (Thread thread in threads) {
            thread.Start();
        }
    }

    private void work() {
        while (queue.Count > 0) {
            string site = queue.Dequeue();
            Console.WriteLine(site);
        }
    }
}
'''

DATA4["R35e99f1126"] = r'''
using System;
using System.Collections.Generic;

static void Main(string[] args) {
    List<Point> POINTS = new List<Point>();
    List<Edge> edges = new List<Edge>();
    FillPoints(POINTS);
    FillEdges(edges, POINTS);
    foreach (Edge e in edges) {
        Console.WriteLine(e);
    }
}

static void FillEdges(List<Edge> edges, List<Point> points) {
    Point[] endpoints = new Point[] {
        points[0], points[1],
        points[2], points[3],
        points[4], points[5],
        points[6], points[7],
        points[8], points[9]
    };
    for (int i = 0; i < endpoints.Length; i += 2) {
        edges.Add(new Edge(endpoints[i], endpoints[i + 1]));
    }
}
'''

DATA4["Ra1eaef8d13"] = r'''
public static void removeEven(int[] k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 != 0) {
            k[counter] = k[i];
            counter++;
        }
    }
    java.util.Arrays.fill(k, counter, n, 0);
}
'''

DATA4["R7fe68d314b"] = r'''
public List<City> LoadCitiesByState(string state) {
    DataTable dt = null;
    try {
        using (var connection = new SqlConnection(_connectionString)) {
            connection.Open();
            using (var command = new SqlCommand("SELECT Name FROM City WHERE State = @state", connection)) {
                command.Parameters.AddWithValue("@state", state);
                var adapter = new SqlDataAdapter(command);
                dt = new DataTable();
                adapter.Fill(dt);
            }
        }
    } catch (Exception) {
        dt = null;
    }
    if (dt == null) {
        return cities;
    }
    List<City> result = new List<City>();
    foreach (DataRow row in dt.Rows) {
        result.Add(new City { Name = row["Name"].ToString() });
    }
    return result;
}
'''

DATA4["R83b1b1f08f"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *copy_string(const char *src) {
    size_t len = strlen(src) + 1;
    char *dst = malloc(len);
    memcpy(dst, src, len);
    return dst;
}

int main(int argc, char **argv) {
    char **myargv = malloc(argc * sizeof(char *));
    for (int i = 1; i < argc; i++) {
        myargv[i - 1] = copy_string(argv[i]);
    }
    for (int i = 0; i < argc - 1; i++) {
        printf("%s\n", myargv[i]);
    }
    return 0;
}
'''

DATA4["R08feb9bb95"] = r'''
private void ResetFields() {
    foreach (Control control in Controls) {
        ResetSingleControl(control);
    }
}

private void ResetSingleControl(Control control) {
    if (control is TextBox) {
        ((TextBox)control).Clear();
    } else if (control is NumericUpDown) {
        ((NumericUpDown)control).Value = 0;
    } else if (control.Controls.Count > 0) {
        foreach (Control child in control.Controls) {
            ResetSingleControl(child);
        }
    }
}
'''

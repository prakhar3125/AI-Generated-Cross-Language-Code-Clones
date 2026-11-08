# -*- coding: utf-8 -*-
DATA3 = {
"T203": {
"python": r'''
import gzip
import io
import traceback

def main():
    dataToCompress = "This is the test data.".encode("iso-8859-1")
    try:
        byteStream = io.BytesIO()
        with gzip.GzipFile(fileobj=byteStream, mode="wb") as zipStream:
            zipStream.write(dataToCompress)
        compressedData = byteStream.getvalue()
        with open("C:/Users/UserName/Desktop/zip_file.gz", "wb") as fileStream:
            fileStream.write(compressedData)
    except Exception as e:
        traceback.print_exc()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    unsigned char *data;
    size_t len;
} ByteBuffer;

extern int gzip_compress(const unsigned char *in, size_t inLen, ByteBuffer *out);
extern void byte_buffer_free(ByteBuffer *buf);

int main(void) {
    const char *text = "This is the test data.";
    ByteBuffer compressed;
    FILE *fileStream = NULL;
    if (gzip_compress((const unsigned char *) text, strlen(text), &compressed) != 0) {
        fprintf(stderr, "compression failed\n");
        return 1;
    }
    fileStream = fopen("C:/Users/UserName/Desktop/zip_file.gz", "wb");
    if (fileStream == NULL) {
        perror("fopen failed");
        byte_buffer_free(&compressed);
        return 1;
    }
    fwrite(compressed.data, 1, compressed.len, fileStream);
    fclose(fileStream);
    byte_buffer_free(&compressed);
    return 0;
}
''',
"csharp": r'''
using System;
using System.IO;
using System.IO.Compression;
using System.Text;

public static void Main() {
    byte[] dataToCompress = Encoding.GetEncoding("ISO-8859-1").GetBytes("This is the test data.");
    try {
        byte[] compressedData;
        using (MemoryStream byteStream = new MemoryStream(dataToCompress.Length)) {
            using (GZipStream zipStream = new GZipStream(byteStream, CompressionMode.Compress)) {
                zipStream.Write(dataToCompress, 0, dataToCompress.Length);
            }
            compressedData = byteStream.ToArray();
        }
        using (FileStream fileStream = new FileStream("C:/Users/UserName/Desktop/zip_file.gz", FileMode.Create)) {
            fileStream.Write(compressedData, 0, compressedData.Length);
        }
    } catch (Exception e) {
        Console.Error.WriteLine(e.StackTrace);
    }
}
'''
},
"T397": {
"python": r'''
import os
import shutil

def copyFolder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            relative = os.path.relpath(root, src)
            target = dest if relative == "." else os.path.join(dest, relative)
            if not os.path.isdir(target):
                os.makedirs(target)
            for name in files:
                shutil.copy2(os.path.join(root, name), os.path.join(target, name))
    except Exception as ex:
        print(ex)
''',
"c": r'''
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

void copy_folder(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    if (dir == NULL) {
        perror("opendir failed");
        return;
    }
    mkdir(dest, 0755);
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        char srcPath[1024];
        char destPath[1024];
        snprintf(srcPath, sizeof(srcPath), "%s/%s", src, entry->d_name);
        snprintf(destPath, sizeof(destPath), "%s/%s", dest, entry->d_name);
        struct stat st;
        if (stat(srcPath, &st) == 0 && S_ISDIR(st.st_mode)) {
            copy_folder(srcPath, destPath);
        } else {
            FILE *in = fopen(srcPath, "rb");
            FILE *out = fopen(destPath, "wb");
            if (in != NULL && out != NULL) {
                char buf[4096];
                size_t n;
                while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
                    fwrite(buf, 1, n, out);
                }
            }
            if (in != NULL) fclose(in);
            if (out != NULL) fclose(out);
        }
    }
    closedir(dir);
}
''',
"csharp": r'''
using System;
using System.IO;

public static void CopyFolder(string src, string dest) {
    try {
        foreach (string dirPath in Directory.GetDirectories(src, "*", SearchOption.AllDirectories)) {
            Directory.CreateDirectory(dirPath.Replace(src, dest));
        }
        foreach (string filePath in Directory.GetFiles(src, "*", SearchOption.AllDirectories)) {
            File.Copy(filePath, filePath.Replace(src, dest), true);
        }
    } catch (Exception ex) {
        Console.Error.WriteLine(ex.StackTrace);
    }
}
'''
},
"T430": {
"python": r'''
import time


class Insets:
    def __init__(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right


class EmptyBorder(Insets):
    pass


def run(self):
    try:
        self.runs = True
        if self.noColor < 2:
            self.noColor += 1
        else:
            self.noColor = 0
        self.changeBtnForegroung(self.clr[self.noColor])
        steps = [
            ((10, -10), (0, 5, 10, 5)),
            ((-10, 10), (0, 0, 10, 10)),
            ((10, -10), (5, 10, 5, 0)),
            ((-10, 10), (10, 10, 0, 0)),
            ((0, 0), (5, 5, 5, 5)),
        ]
        for (leftShift, rightShift), border in steps:
            self.changeBtnMargin(Insets(self.initMargin.top,
                                        self.initMargin.left + leftShift,
                                        self.initMargin.bottom,
                                        self.initMargin.right + rightShift))
            self.changePnlBorder(EmptyBorder(border[0], border[1], border[2], border[3]))
            time.sleep(0.1)
        self.count += 1
    except Exception as e:
        print(e)
''',
"c": r'''
#include <stdio.h>

typedef struct {
    int top;
    int left;
    int bottom;
    int right;
} Insets;

typedef struct {
    int noColor;
    int count;
    int runs;
    Insets initMargin;
    int clr[4];
} AppState;

extern void changeBtnForegroung(int color);
extern void changeBtnMargin(Insets margin);
extern void changePnlBorder(Insets border);
extern void sleep_ms(int ms);

void run(AppState *state) {
    if (state->noColor < 2) {
        state->noColor++;
    } else {
        state->noColor = 0;
    }
    changeBtnForegroung(state->clr[state->noColor]);
    int leftShifts[5] = {10, -10, 10, -10, 0};
    int rightShifts[5] = {-10, 10, -10, 10, 0};
    int borders[5][4] = {
        {0, 5, 10, 5}, {0, 0, 10, 10}, {5, 10, 5, 0}, {10, 10, 0, 0}, {5, 5, 5, 5}
    };
    for (int i = 0; i < 5; i++) {
        Insets margin = {state->initMargin.top,
                         state->initMargin.left + leftShifts[i],
                         state->initMargin.bottom,
                         state->initMargin.right + rightShifts[i]};
        changeBtnMargin(margin);
        Insets border = {borders[i][0], borders[i][1], borders[i][2], borders[i][3]};
        changePnlBorder(border);
        sleep_ms(100);
    }
    state->count++;
}
''',
"csharp": r'''
using System;
using System.Threading;

public void Run() {
    try {
        runs = true;
        noColor = noColor < 2 ? noColor + 1 : 0;
        changeBtnForegroung(clr[noColor]);
        int[] leftShifts = { 10, -10, 10, -10, 0 };
        int[] rightShifts = { -10, 10, -10, 10, 0 };
        int[][] borders = {
            new[] { 0, 5, 10, 5 },
            new[] { 0, 0, 10, 10 },
            new[] { 5, 10, 5, 0 },
            new[] { 10, 10, 0, 0 },
            new[] { 5, 5, 5, 5 }
        };
        for (int i = 0; i < 5; i++) {
            changeBtnMargin(new Insets(initMargin.top, initMargin.left + leftShifts[i],
                                       initMargin.bottom, initMargin.right + rightShifts[i]));
            changePnlBorder(new EmptyBorder(borders[i][0], borders[i][1],
                                            borders[i][2], borders[i][3]));
            Thread.Sleep(100);
        }
        count++;
    } catch (Exception e) {
        Console.WriteLine(e);
    }
}
'''
}
}

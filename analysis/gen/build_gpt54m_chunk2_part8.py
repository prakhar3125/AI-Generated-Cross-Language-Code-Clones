DATA_T8 = {
    "T238": {
        "python": r'''def main():
    name = "AnuvratAnuvra"
    arr = list(name)
    char_map = {}
    for val in arr:
        if val in char_map:
            char_map[val] = char_map[val] + 1
        else:
            char_map[val] = 1
    for key, value in char_map.items():
        if value > 1:
            print(str(key) + ":" + str(value))''',
        "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *name = "AnuvratAnuvra";
    size_t name_len = strlen(name);
    int map[256] = {0};
    for (size_t i = 0; i < name_len; i++) {
        unsigned char val = (unsigned char)name[i];
        map[val] = map[val] > 0 ? map[val] + 1 : 1;
    }
    for (int i = 0; i < 256; i++) {
        if (map[i] > 1) {
            printf("%c:%d\n", i, map[i]);
        }
    }
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;

public static class DuplicateChars
{
    public static void Main()
    {
        string name = "AnuvratAnuvra";
        char[] arr = name.ToCharArray();
        var map = new Dictionary<char, int>();
        foreach (char val in arr)
        {
            map[val] = map.ContainsKey(val) ? map[val] + 1 : 1;
        }
        foreach (var entry in map)
        {
            if (entry.Value > 1)
            {
                char key = entry.Key;
                object value = entry.Value;
                Console.WriteLine(key + ":" + value);
            }
        }
    }
}'''
    },
    "T202": {
        "python": r'''import os
import shutil


def copy_folder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            for name in dirs + files:
                s = os.path.join(root, name)
                try:
                    d = os.path.join(dest, os.path.relpath(s, src))
                    if os.path.isdir(s):
                        if not os.path.exists(d):
                            os.mkdir(d)
                        continue
                    shutil.copy(s, d)
                except Exception as e:
                    print(e)
    except Exception as ex:
        print(ex)''',
        "c": r'''#include <stddef.h>

extern int walk_directory(const char *src,
                          void (*visit)(const char *path, int is_dir, void *ctx),
                          void *ctx);
extern void relative_path(const char *src, const char *s, char *out, size_t out_size);
extern void resolve_relative(const char *dest, const char *rel, char *out, size_t out_size);
extern int path_exists(const char *path);
extern int create_directory(const char *path);
extern void copy_file(const char *src, const char *dest);

static void on_entry(const char *s, int is_dir, void *ctx) {
    const char **paths = ctx;
    char rel[1024], d[1024];
    relative_path(paths[0], s, rel, sizeof(rel));
    resolve_relative(paths[1], rel, d, sizeof(d));
    if (is_dir) {
        if (!path_exists(d)) create_directory(d);
        return;
    }
    copy_file(s, d);
}

void copy_folder(const char *src, const char *dest) {
    const char *paths[2] = {src, dest};
    walk_directory(src, on_entry, (void *)paths);
}''',
        "csharp": r'''using System;
using System.IO;

public static class FolderCopier
{
    public static void CopyFolder(DirectoryInfo src, DirectoryInfo dest)
    {
        try
        {
            foreach (var s in src.EnumerateFileSystemInfos("*", SearchOption.AllDirectories))
            {
                try
                {
                    string rel = s.FullName.Substring(src.FullName.Length).TrimStart(Path.DirectorySeparatorChar);
                    string d = Path.Combine(dest.FullName, rel);
                    if ((s.Attributes & FileAttributes.Directory) == FileAttributes.Directory)
                    {
                        if (!Directory.Exists(d)) Directory.CreateDirectory(d);
                        continue;
                    }
                    File.Copy(s.FullName, d);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.StackTrace);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.StackTrace);
        }
    }
}'''
    }
}

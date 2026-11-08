DATA_B7 = {
"T633": {
"python": r"""
import zipfile

_location = "./out/"
_zip_file = "archive.zip"

class Log:
    @staticmethod
    def v(tag, message):
        print(tag + ": " + message)

    @staticmethod
    def d(tag, message):
        print(tag + ": " + message)

    @staticmethod
    def e(tag, message, error=None):
        print(tag + ": " + message)

def _dir_checker(name):
    pass

def unzip():
    try:
        with zipfile.ZipFile(_zip_file) as zin:
            for ze in zin.infolist():
                Log.v("Decompress", "Unzipping " + ze.filename)
                if ze.is_dir():
                    _dir_checker(ze.filename)
                else:
                    with zin.open(ze) as src, open(_location + ze.filename, "wb") as bufout:
                        while True:
                            read = src.read(1024)
                            if read == b"":
                                break
                            bufout.write(read)
        Log.d("Unzip", "Unzipping complete. path :  " + _location)
    except Exception as e:
        Log.e("Decompress", "unzip")
        Log.d("Unzip", "Unzipping failed")
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* minimal stand-ins for Android Log and java.util.zip */
extern void *zip_open_read(const char *path);
extern const char *zip_next_entry(void *archive, char *name, size_t name_size);
extern int zip_entry_is_directory(const char *name);
extern long zip_entry_read(void *archive, unsigned char *buffer, int size);
extern void zip_entry_close(void *archive);
extern void zip_close(void *archive);

static void log_v(const char *tag, const char *message) {
    printf("%s: %s\n", tag, message);
}

static void log_d(const char *tag, const char *message) {
    printf("%s: %s\n", tag, message);
}

static void log_e(const char *tag, const char *message) {
    printf("%s: %s\n", tag, message);
}

static const char *_zip_file = "archive.zip";
static const char *_location = "./out/";

static void _dir_checker(const char *name) {
}

void unzip(void) {
    void *archive = zip_open_read(_zip_file);
    if (archive == NULL) {
        log_e("Decompress", "unzip");
        log_d("Unzip", "Unzipping failed");
        return;
    }
    char name[256];
    while (zip_next_entry(archive, name, sizeof(name)) != NULL) {
        char entry_path[512];
        snprintf(entry_path, sizeof(entry_path), "%s%s", _location, name);
        log_v("Decompress", entry_path);
        if (zip_entry_is_directory(name)) {
            _dir_checker(name);
        } else {
            FILE *bufout = fopen(entry_path, "wb");
            if (bufout != NULL) {
                unsigned char buffer[1024];
                long read = 0;
                while ((read = zip_entry_read(archive, buffer, 1024)) != -1) {
                    fwrite(buffer, 1, (size_t)read, bufout);
                }
                fclose(bufout);
                zip_entry_close(archive);
            }
        }
    }
    zip_close(archive);
    log_d("Unzip", "Unzipping complete");
}
""",
"csharp": r"""
using System;
using System.IO;
using System.IO.Compression;

public static class Decompressor
{
    private static string _zipFile = "archive.zip";
    private static string _location = "./out/";

    private static void LogV(string tag, string message) { Console.WriteLine(tag + ": " + message); }
    private static void LogD(string tag, string message) { Console.WriteLine(tag + ": " + message); }
    private static void LogE(string tag, string message) { Console.WriteLine(tag + ": " + message); }

    private static void DirChecker(string name) { }

    public static void Unzip()
    {
        try
        {
            using (FileStream fin = new FileStream(_zipFile, FileMode.Open, FileAccess.Read))
            using (var zin = new ZipInputStream(fin))
            {
                var ze = zin.GetNextEntry();
                while (ze != null)
                {
                    LogV("Decompress", "Unzipping " + ze.Name);
                    if (ze.IsDirectory)
                    {
                        DirChecker(ze.Name);
                    }
                    else
                    {
                        using (FileStream fout = new FileStream(_location + ze.Name, FileMode.Create))
                        using (BufferedStream bufout = new BufferedStream(fout))
                        {
                            byte[] buffer = new byte[1024];
                            int read = 0;
                            while ((read = zin.Read(buffer, 0, buffer.Length)) != -1)
                            {
                                bufout.Write(buffer, 0, read);
                            }
                        }
                    }
                    ze = zin.GetNextEntry();
                }
            }
            LogD("Unzip", "Unzipping complete. path :  " + _location);
        }
        catch (Exception)
        {
            LogE("Decompress", "unzip");
            LogD("Unzip", "Unzipping failed");
        }
    }
}
"""
}
}

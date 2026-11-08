DATA_A3 = {
"T252": {
"python": r"""
import pickle

class DefaultTableModel:
    def __init__(self, data=None):
        self.data = data or []

class XMLDecoder:
    def __init__(self, stream):
        self.stream = stream

    def readObject(self):
        return pickle.load(self.stream)

class JTable:
    def __init__(self):
        self.model = None

    def setModel(self, model):
        self.model = model

table = JTable()
model = None

def on_action(e, file):
    global model
    try:
        with open(file, "rb") as stream:
            xd = XMLDecoder(stream)
            model = xd.readObject()
            table.setModel(model)
    except IOError as ex:
        import traceback
        traceback.print_exc()
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned char *bytes;
    size_t len;
} TableModel;

static TableModel *model = NULL;
static TableModel *table = NULL;

static TableModel *xml_decoder_read(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    TableModel *m = malloc(sizeof(TableModel));
    m->bytes = malloc(size > 0 ? (size_t)size : 1);
    m->len = fread(m->bytes, 1, (size_t)size, f);
    fclose(f);
    return m;
}

void on_action(const char *file) {
    TableModel *loaded = xml_decoder_read(file);
    if (loaded == NULL) {
        perror("load failed");
        return;
    }
    model = loaded;
    table = loaded;
}
""",
"csharp": r"""
using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

public class DefaultTableModel
{
}

public class JTable
{
    public DefaultTableModel Model { get; set; }
}

public class Loader
{
    private string file;
    private DefaultTableModel model;
    private JTable table = new JTable();

    public void OnAction(EventArgs e)
    {
        try
        {
            using (FileStream fs = new FileStream(file, FileMode.Open, FileAccess.Read))
            using (BufferedStream bs = new BufferedStream(fs))
            {
                var formatter = new BinaryFormatter();
                model = (DefaultTableModel)formatter.Deserialize(bs);
                table.Model = model;
            }
        }
        catch (IOException ex)
        {
            Console.Error.WriteLine(ex.StackTrace);
        }
    }
}
"""
}
}

DATA_B1 = {
"T653": {
"python": r"""
import tkinter.messagebox as tkmsg

def prompt_scale(question, icon_name):
    # minimal stand-in for the Java modal input dialog
    try:
        return input(question)
    except EOFError:
        return None

class Frame:
    def __init__(self):
        self.width = 0
        self.height = 0

    def setSize(self, w, h):
        self.width = w
        self.height = h

def scale(new_width, new_height):
    pass

frame = Frame()

def on_action(e):
    width_icon = "LR-arrows.png"
    scale_width = prompt_scale("What should the new width be?", width_icon)
    height_icon = "UD-arrows.png"
    scale_height = prompt_scale("What should the new height be?", width_icon)
    x = float(scale_width)
    y = float(scale_height)
    new_width = int(x)
    new_height = int(y)
    frame.setSize(new_width, new_height)
    scale(new_width, new_height)
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* minimal stand-ins for the Java dialog and frame */
static char *show_input_dialog(const char *question, const char *icon) {
    char *buf = malloc(256);
    printf("%s", question);
    if (fgets(buf, 256, stdin) == NULL) {
        free(buf);
        return NULL;
    }
    buf[strcspn(buf, "\n")] = '\0';
    return buf;
}

typedef struct {
    int width;
    int height;
} Frame;

static Frame frame;

static void frame_set_size(Frame *f, int w, int h) {
    f->width = w;
    f->height = h;
}

static void scale_frame(int new_width, int new_height) {
    printf("scale %d %d\n", new_width, new_height);
}

void on_action(void) {
    const char *width_icon = "LR-arrows.png";
    char *scale_width = show_input_dialog("What should the new width be?", width_icon);
    const char *height_icon = "UD-arrows.png";
    char *scale_height = show_input_dialog("What should the new height be?", width_icon);
    double x = atof(scale_width);
    double y = atof(scale_height);
    int new_width = (int)x;
    int new_height = (int)y;
    frame_set_size(&frame, new_width, new_height);
    scale_frame(new_width, new_height);
    free(scale_width);
    free(scale_height);
}
""",
"csharp": r"""
using System;
using System.Windows.Forms;

public class ScaleForm
{
    private Form frame = new Form();

    public void OnAction(EventArgs e)
    {
        var widthIcon = new Icon("LR-arrows.png");
        string scaleWidth = Prompt("What should the new width be?", widthIcon);
        var heightIcon = new Icon("UD-arrows.png");
        string scaleHeight = Prompt("What should the new height be?", widthIcon);
        double x = double.Parse(scaleWidth);
        double y = double.Parse(scaleHeight);
        int newWidth = (int)x;
        int newHeight = (int)y;
        frame.Size = new System.Drawing.Size(newWidth, newHeight);
        Scale(newWidth, newHeight);
    }

    private static string Prompt(string question, Icon icon)
    {
        return Microsoft.VisualBasic.Interaction.InputBox(question, "", "");
    }

    private static void Scale(int newWidth, int newHeight)
    {
    }
}
"""
}
}

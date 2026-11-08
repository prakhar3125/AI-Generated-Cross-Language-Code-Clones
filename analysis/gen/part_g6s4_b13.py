DATA_B13 = {
"T713": {
"python": r"""
class Field:
    def __init__(self, name):
        self.name = name

    def get(self, obj):
        return getattr(obj, "_" + self.name, None)

    def set(self, obj, value):
        setattr(obj, "_" + self.name, value)

class TextView:
    def __init__(self, context, cursor_res, editor):
        self.context = context
        self._mCursorDrawableRes = cursor_res
        self._mEditor = editor

    def getDeclaredField(self, name):
        return Field(name)

class Drawable:
    def __init__(self):
        self.filter = None

    def setColorFilter(self, color, mode):
        self.filter = (color, mode)

class ContextCompat:
    @staticmethod
    def getDrawable(context, res_id):
        return Drawable()

class PorterDuff:
    class Mode:
        SRC_IN = "SRC_IN"

def set_cursor_color(view, color):
    try:
        field = TextView.getDeclaredField("mCursorDrawableRes")
        drawable_res_id = field.get(view)
        field = TextView.getDeclaredField("mEditor")
        editor = field.get(view)
        drawable = ContextCompat.getDrawable(view.context, drawable_res_id)
        drawable.setColorFilter(color, PorterDuff.Mode.SRC_IN)
        drawables = [drawable, drawable]
        field = type(editor).getDeclaredField("mCursorDrawable")
        field.set(editor, drawables)
    except Exception:
        pass
""",
"c": r"""
#include <stdlib.h>

/* reflection over private fields approximated with a small property map */
typedef struct {
    const char *name;
    void *value;
} Field;

static Field *get_declared_field(const char *name) {
    Field *f = malloc(sizeof(Field));
    f->name = name;
    f->value = NULL;
    return f;
}

static void field_set_accessible(Field *f, int accessible) {
}

static int field_get_int(Field *f) {
    return f->value ? *(int *)f->value : 0;
}

static void field_set_object(Field *f, void *value) {
    f->value = value;
}

typedef struct {
    int mCursorDrawableRes;
    void *mEditor;
} TextView;

typedef struct {
    int color;
    int mode;
} ColorFilter;

typedef struct {
    ColorFilter *filter;
} Drawable;

static Drawable *get_drawable(int res_id) {
    Drawable *d = malloc(sizeof(Drawable));
    d->filter = NULL;
    return d;
}

static void drawable_set_color_filter(Drawable *d, int color, int mode) {
    d->filter = malloc(sizeof(ColorFilter));
    d->filter->color = color;
    d->filter->mode = mode;
}

void set_cursor_color(TextView *view, int color) {
    Field *field = get_declared_field("mCursorDrawableRes");
    field_set_accessible(field, 1);
    int drawable_res_id = field_get_int(field);
    field = get_declared_field("mEditor");
    field_set_accessible(field, 1);
    void *editor = field->value;
    Drawable *drawable = get_drawable(drawable_res_id);
    drawable_set_color_filter(drawable, color, 1);
    void *drawables[2] = {drawable, drawable};
    field = get_declared_field("mCursorDrawable");
    field_set_object(field, drawables);
}
""",
"csharp": r"""
using System;
using System.Reflection;

public class TextView
{
    internal int mCursorDrawableRes;
    internal object mEditor;
    public object Context { get; set; }
}

public class Drawable
{
    public void SetColorFilter(int color, object mode) { }
}

public static class ContextCompat
{
    public static Drawable GetDrawable(object context, int resId)
    {
        return new Drawable();
    }
}

public static class CursorStyler
{
    public static void SetCursorColor(TextView view, int color)
    {
        try
        {
            const BindingFlags privateFlags = BindingFlags.NonPublic | BindingFlags.Instance;
            FieldInfo field = typeof(TextView).GetField("mCursorDrawableRes", privateFlags);
            int drawableResId = (int)field.GetValue(view);
            field = typeof(TextView).GetField("mEditor", privateFlags);
            object editor = field.GetValue(view);
            Drawable drawable = ContextCompat.GetDrawable(view.Context, drawableResId);
            drawable.SetColorFilter(color, "SRC_IN");
            Drawable[] drawables = { drawable, drawable };
            field = editor.GetType().GetField("mCursorDrawable", privateFlags);
            field.SetValue(editor, drawables);
        }
        catch (Exception)
        {
        }
    }
}
"""
}
}

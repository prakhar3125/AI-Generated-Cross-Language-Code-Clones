DATA_T2 = {}

DATA_T2["T34"] = {"outputs": {
"python": """IMAGE_CAPTURE = 1
RESULT_OK = -1


class DBHelper:
    def __init__(self, context):
        self.context = context

    def get_writable_db(self):
        return SQLiteDatabase()

    def close(self):
        pass


class SQLiteDatabase:
    def exec_sql(self, statement):
        pass

    def close(self):
        pass


def on_activity_result(request_code, result_code, data):
    if request_code == IMAGE_CAPTURE and result_code == RESULT_OK:
        db_helper = DBHelper(self)
        sql = db_helper.get_writable_db()
        sql.exec_sql("insert statement for inserting path to database")
        sql.close()
        db_helper.close()
""",
"c": """#define IMAGE_CAPTURE 1
#define RESULT_OK -1

typedef struct SQLiteDatabase SQLiteDatabase;
typedef struct DBHelper DBHelper;

void sqlite_exec_sql(SQLiteDatabase *db, const char *stmt);
void sqlite_close(SQLiteDatabase *db);
SQLiteDatabase *db_helper_get_writable_db(DBHelper *helper);
void db_helper_close(DBHelper *helper);

void on_activity_result(int requestCode, int resultCode, void *data) {
    if (requestCode == IMAGE_CAPTURE && resultCode == RESULT_OK) {
        DBHelper *dbHelper = db_helper_new(NULL);
        SQLiteDatabase *sql = db_helper_get_writable_db(dbHelper);
        sqlite_exec_sql(sql, "insert statement for inserting path to database");
        sqlite_close(sql);
        db_helper_close(dbHelper);
    }
}
""",
"csharp": """private const int IMAGE_CAPTURE = 1;
private const int RESULT_OK = -1;

protected void OnActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == IMAGE_CAPTURE && resultCode == RESULT_OK) {
        var dbHelper = new DBHelper(this);
        var sql = dbHelper.GetWritableDatabase();
        sql.ExecSQL("insert statement for inserting path to database");
        sql.Close();
        dbHelper.Close();
    }
}
"""}}

DATA_T2["T314"] = {"outputs": {
"python": """def get_name(self, value):
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
    return "".join(buffer)
""",
"c": """char *get_name(const char *value) {
    static char buffer[512];
    buffer[0] = '\\0';
    char high[256], low[256];
    size_t divider = get_part_divider();
    if (strlen(value) < divider) {
        strcpy(high, "");
        strcpy(low, value);
    } else {
        size_t index = strlen(value) - divider;
        strncpy(high, value, index);
        high[index] = '\\0';
        strcpy(low, value + index);
    }
    const char *high_name = get_high_processor_name(high);
    const char *low_name = get_low_processor_name(low);
    if (high_name[0] != '\\0') {
        strcat(buffer, high_name);
        strcat(buffer, SEPARATOR);
        strcat(buffer, get_token());
        if (low_name[0] != '\\0') {
            strcat(buffer, SEPARATOR);
        }
    }
    if (low_name[0] != '\\0') {
        strcat(buffer, low_name);
    }
    return buffer;
}
""",
"csharp": """public string GetName(string value) {
    var buffer = new StringBuilder();
    string high, low;
    if (value.Length < GetPartDivider()) {
        high = "";
        low = value;
    } else {
        int index = value.Length - GetPartDivider();
        high = value.Substring(0, index);
        low = value.Substring(index);
    }
    string highName = GetHighProcessor().GetName(high);
    string lowName = GetLowProcessor().GetName(low);
    if (highName != "") {
        buffer.Append(highName);
        buffer.Append(SEPARATOR);
        buffer.Append(GetToken());
        if (lowName != "") {
            buffer.Append(SEPARATOR);
        }
    }
    if (lowName != "") {
        buffer.Append(lowName);
    }
    return buffer.ToString();
}
"""}}

DATA_T2["T22"] = {"outputs": {
"python": """def main():
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
    print("End of I , J , K")
""",
"c": """int main(void) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            for (int k = 0; k < 9; k++) {
                if (condition1) {
                    printf("Breaking from Loop K and J\\n");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    printf("Breaking from Loop K, J and I\\n");
                    k = 9;
                    j = 9;
                    i = 9;
                }
            }
        }
    }
    printf("End of I , J , K\\n");
    return 0;
}
""",
"csharp": """public static void Main(string[] args) {
    for (int i = 0; i < 9; i++) {
        bool stopI = false;
        for (int j = 0; j < 9 && !stopI; j++) {
            for (int k = 0; k < 9; k++) {
                if (condition1) {
                    Console.WriteLine("Breaking from Loop K and J");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    Console.WriteLine("Breaking from Loop K, J and I");
                    k = 9;
                    j = 9;
                    stopI = true;
                    break;
                }
            }
        }
        if (stopI) break;
    }
    Console.WriteLine("End of I , J , K");
}
"""}}

DATA_T2["T543"] = {"outputs": {
"python": """class ActionEvent:
    def __init__(self, source):
        self.source = source


class Timer:
    def stop(self):
        pass


def action_performed(self, e):
    duration = int(time.time() * 1000) - self.start_time
    progress = float(duration) / float(RUN_TIME)
    self.line_point = Point()
    self.line_point.x = self.get_width() // 2
    if progress < 0.5:
        self.line_point.y = round(self.get_height() * (progress * 2))
    elif progress > 1.0:
        progress = 1.0
        e.source.stop()
        self.line_point = None
        self.ball_point = None
    else:
        self.line_point.y = round(self.get_height() * (progress * 2))
        self.line_point.y = self.get_height() - (self.line_point.y - self.get_height())
        self.ball_point.y = self.line_point.y
    self.repaint()
""",
"c": """typedef struct { int x, y; } Point;

void action_performed(ActionEvent *e) {
    long duration = current_time_millis() - start_time;
    float progress = (float) duration / (float) RUN_TIME;
    line_point.x = get_width() / 2;
    if (progress < 0.5f) {
        line_point.y = (int) roundf(get_height() * (progress * 2));
    } else if (progress > 1.0f) {
        timer_stop(e->source);
        line_point_valid = 0;
        ball_point_valid = 0;
    } else {
        line_point.y = (int) roundf(get_height() * (progress * 2));
        line_point.y = get_height() - (line_point.y - get_height());
        ball_point.y = line_point.y;
    }
    repaint();
}
""",
"csharp": """public void ActionPerformed(ActionEvent e) {
    long duration = System.currentTimeMillis() - startTime;
    float progress = (float) duration / (float) RUN_TIME;
    linePoint = new Point();
    linePoint.x = GetWidth() / 2;
    if (progress < 0.5f) {
        linePoint.y = (int) Math.Round(GetHeight() * (progress * 2));
    } else if (progress > 1f) {
        progress = 1f;
        ((Timer) e.Source).Stop();
        linePoint = null;
        ballPoint = null;
    } else {
        linePoint.y = (int) Math.Round(GetHeight() * (progress * 2));
        linePoint.y = GetHeight() - (linePoint.y - GetHeight());
        ballPoint.y = linePoint.y;
    }
    Repaint();
}
"""}}

DATA_T2["T653"] = {"outputs": {
"python": """def action_performed(e):
    width_icon = ImageIcon("LR-arrows.png")
    scale_width = JOptionPane.show_input_dialog(None, "What should the new width be?", "",
                                                JOptionPane.QUESTION_MESSAGE, width_icon, None, None)
    height_icon = ImageIcon("UD-arrows.png")
    scale_height = JOptionPane.show_input_dialog(None, "What should the new height be?", "",
                                                 JOptionPane.QUESTION_MESSAGE, width_icon, None, None)
    new_width = int(float(scale_width))
    new_height = int(float(scale_height))
    frame.set_size(new_width, new_height)
    scale(new_width, new_height)
""",
"c": """char *show_input_dialog(const char *message, const char *icon);

void action_performed(void) {
    char *scale_width = show_input_dialog("What should the new width be?", "LR-arrows.png");
    char *scale_height = show_input_dialog("What should the new height be?", "UD-arrows.png");
    int new_width = (int) atof(scale_width);
    int new_height = (int) atof(scale_height);
    frame_set_size(new_width, new_height);
    scale(new_width, new_height);
}
""",
"csharp": """public void ActionPerformed(ActionEvent e) {
    var widthIcon = new ImageIcon("LR-arrows.png");
    string scaleWidth = (string) JOptionPane.ShowInputDialog(null, "What should the new width be?", "",
        JOptionPane.QUESTION_MESSAGE, widthIcon, null, null);
    var heightIcon = new ImageIcon("UD-arrows.png");
    string scaleHeight = (string) JOptionPane.ShowInputDialog(null, "What should the new height be?", "",
        JOptionPane.QUESTION_MESSAGE, widthIcon, null, null);
    int newWidth = (int) double.Parse(scaleWidth);
    int newHeight = (int) double.Parse(scaleHeight);
    frame.SetSize(newWidth, newHeight);
    Scale(newWidth, newHeight);
}
"""}}

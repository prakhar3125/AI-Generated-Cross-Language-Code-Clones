DATA_A5 = {
"T34": {
"python": r"""
IMAGE_CAPTURE = 1

class Activity:
    RESULT_OK = -1

class SQLiteDatabase:
    def execSQL(self, statement):
        pass

    def close(self):
        pass

class DBHelper:
    def __init__(self, context):
        self.context = context

    def getWritableDatabase(self):
        return SQLiteDatabase()

    def close(self):
        pass

def on_activity_result(request_code, result_code, data):
    if request_code == IMAGE_CAPTURE and result_code == Activity.RESULT_OK:
        db_helper = DBHelper(None)
        sql = db_helper.getWritableDatabase()
        sql.execSQL("insert statement for inserting path to database")
        sql.close()
        db_helper.close()
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>

#define IMAGE_CAPTURE 1
#define RESULT_OK (-1)

typedef struct SQLiteDatabase SQLiteDatabase;
typedef struct DBHelper DBHelper;

struct SQLiteDatabase {
    void (*execSQL)(SQLiteDatabase *, const char *);
    void (*close)(SQLiteDatabase *);
};

struct DBHelper {
    SQLiteDatabase * (*getWritableDatabase)(DBHelper *);
    void (*close)(DBHelper *);
};

static void exec_sql(SQLiteDatabase *self, const char *statement) {
    printf("exec: %s\n", statement);
}

static void sql_close(SQLiteDatabase *self) {
    free(self);
}

static SQLiteDatabase *get_writable_db(DBHelper *self) {
    SQLiteDatabase *sql = malloc(sizeof(SQLiteDatabase));
    sql->execSQL = exec_sql;
    sql->close = sql_close;
    return sql;
}

static void db_close(DBHelper *self) {
    free(self);
}

void on_activity_result(int request_code, int result_code) {
    if (request_code == IMAGE_CAPTURE && result_code == RESULT_OK) {
        DBHelper *db_helper = malloc(sizeof(DBHelper));
        db_helper->getWritableDatabase = get_writable_db;
        db_helper->close = db_close;
        SQLiteDatabase *sql = db_helper->getWritableDatabase(db_helper);
        sql->execSQL(sql, "insert statement for inserting path to database");
        sql->close(sql);
        db_helper->close(db_helper);
    }
}
""",
"csharp": r"""
using System;

public class Activity
{
    public const int RESULT_OK = -1;
}

public class Intent
{
}

public class SQLiteDatabase
{
    public void ExecSQL(string statement) { }
    public void Close() { }
}

public class DBHelper
{
    public SQLiteDatabase GetWritableDatabase() { return new SQLiteDatabase(); }
    public void Close() { }
}

public class MyActivity
{
    private const int IMAGE_CAPTURE = 1;

    protected void OnActivityResult(int requestCode, int resultCode, Intent data)
    {
        if (requestCode == IMAGE_CAPTURE && resultCode == Activity.RESULT_OK)
        {
            DBHelper dbHelper = new DBHelper();
            SQLiteDatabase sql = dbHelper.GetWritableDatabase();
            sql.ExecSQL("insert statement for inserting path to database");
            sql.Close();
            dbHelper.Close();
        }
    }
}
"""
}
}

DATA_C2 = {
"R357f96f327": r"""
public static DataTable GetWorksheetAsDataTable(ExcelWorksheet worksheet) {
    DataTable dt = new DataTable(worksheet.Name);
    dt.Columns.AddRange(GetDataColumns(worksheet).ToArray());
    int headerOffset = 1;
    int depth = GetTableDepth(worksheet, headerOffset);
    foreach (int rowNum in Enumerable.Range(1, depth)) {
        dt.Rows.Add(BuildRow(dt, worksheet, rowNum, headerOffset));
    }
    return dt;
}

private static DataRow BuildRow(DataTable dt, ExcelWorksheet worksheet, int rowNum, int headerOffset) {
    DataRow row = dt.NewRow();
    int width = dt.Columns.Count;
    foreach (int colNum in Enumerable.Range(1, width)) {
        object val = worksheet.Cells[rowNum + headerOffset, colNum].Value;
        row[colNum - 1] = val == null ? null : val.ToString();
    }
    return row;
}
""",
"Rfe9a432a46": r"""
public override void OnException (ExceptionContext filterContext) {
    MarkExceptionHandled(filterContext);
    var controllerName = (string) filterContext.RouteData.Values ["controller"];
    var actionName = (string) filterContext.RouteData.Values ["action"];
    var model = new HandleErrorInfo (filterContext.Exception, controllerName, actionName);
    filterContext.Result = BuildResult(model, filterContext);
    filterContext.Exception = null;
}

private static void MarkExceptionHandled (ExceptionContext filterContext) {
    filterContext.HttpContext.Response.TrySkipIisCustomErrors = true;
    filterContext.ExceptionHandled = true;
    filterContext.HttpContext.Response.ClearContent ();
}

private static ViewResult BuildResult (HandleErrorInfo model, ExceptionContext filterContext) {
    return new ViewResult {ViewName = View, MasterName = Master, ViewData = new ViewDataDictionary < HandleErrorInfo > (model), TempData = filterContext.Controller.TempData};
}
"""
}

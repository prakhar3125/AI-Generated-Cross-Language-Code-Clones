DATA_R2 = {}

DATA_R2["R357f96f327"] = """public static DataTable GetWorksheetAsDataTable(ExcelWorksheet worksheet) {
    var dt = new DataTable(worksheet.Name);
    var dataColumns = GetDataColumns(worksheet).ToList();
    dt.Columns.AddRange(dataColumns.ToArray());
    int headerOffset = 1;
    int width = dt.Columns.Count;
    int depth = GetTableDepth(worksheet, headerOffset);
    int rowNum = 1;
    while (rowNum <= depth) {
        var row = dt.NewRow();
        int colNum = 1;
        while (colNum <= width) {
            object val = worksheet.Cells[rowNum + headerOffset, colNum].Value;
            row[colNum - 1] = val == null ? null : val.ToString();
            colNum++;
        }
        dt.Rows.Add(row);
        rowNum++;
    }
    return dt;
}"""

DATA_R2["Rfe9a432a46"] = """public override void OnException (ExceptionContext filterContext) {
    filterContext.HttpContext.Response.TrySkipIisCustomErrors = true;
    filterContext.ExceptionHandled = true;
    filterContext.HttpContext.Response.ClearContent ();
    string controllerName = (string) filterContext.RouteData.Values ["controller"];
    string actionName = (string) filterContext.RouteData.Values ["action"];
    BuildErrorView (filterContext, controllerName, actionName);
    filterContext.Exception = null;
}

private void BuildErrorView (ExceptionContext filterContext, string controllerName, string actionName) {
    var model = new HandleErrorInfo (filterContext.Exception, controllerName, actionName);
    filterContext.Result = new ViewResult {
        ViewName = View,
        MasterName = Master,
        ViewData = new ViewDataDictionary < HandleErrorInfo > (model),
        TempData = filterContext.Controller.TempData
    };
}"""

DATA_R2["Rf6f525dc34"] = """static void Main (string [] args) {
    string libreOfficePath = getLibreOfficePath();
    var procStartInfo = new ProcessStartInfo (libreOfficePath, string.Format (CreateParamString (args)));
    SetProcessStartInfoProperties(procStartInfo);
    using (var process = new Process { StartInfo = procStartInfo }) {
        ExecuteProcess(process);
        ValidateProcessExitCode(process);
    }
}"""

DATA_R2["R6ea07c8787"] = """public static void Rename (this FileSystemInfo item, string newName) {
    if (item == null) {
        throw new ArgumentNullException ("item");
    }
    if (item is FileInfo) {
        ((FileInfo) item).Rename (newName);
    } else if (item is DirectoryInfo) {
        ((DirectoryInfo) item).Rename (newName);
    } else {
        throw new ArgumentException ("Item", "Unexpected subclass of FileSystemInfo " + item.GetType ());
    }
}"""

DATA_R2["R3c52337f3a"] = """internal static string GetIPAddress (HttpRequestBase request) {
    string fromForwarded = ParseForwardedHeader (request);
    if (fromForwarded != null) {
        return fromForwarded;
    }
    string xForwardedFor = request.Headers ["X-Forwarded-For"];
    if (! String.IsNullOrEmpty (xForwardedFor)) {
        return xForwardedFor.Split (',') [0];
    }
    return request.UserHostAddress;
}

private static string ParseForwardedHeader (HttpRequestBase request) {
    string forwarded = request.Headers ["Forwarded"];
    if (String.IsNullOrEmpty (forwarded)) {
        return null;
    }
    foreach (string segment in forwarded.Split (',') [0].Split (';')) {
        string [] pair = segment.Trim ().Split ('=');
        if (pair.Length == 2 && pair [0].Equals ("for", StringComparison.OrdinalIgnoreCase)) {
            return StripEndpointSuffix (pair [1].Trim ('"'));
        }
    }
    return null;
}

private static string StripEndpointSuffix (string ip) {
    int left = ip.IndexOf ('[');
    if (left == 0) {
        int right = ip.IndexOf (']');
        return ip.Substring (1, right - 1);
    }
    int colon = ip.IndexOf (':');
    return colon == - 1 ? ip : ip.Substring (0, colon);
}"""

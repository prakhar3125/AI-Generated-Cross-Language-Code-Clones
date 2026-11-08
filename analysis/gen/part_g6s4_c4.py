DATA_C4 = {
"R6ea07c8787": r"""
public static void Rename (this FileSystemInfo item, string newName) {
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
}
""",
"Rd744148380": r"""
public void onRequestPermissionsResult (int requestCode, String permissions [], int [] grantResults) {
    super.onRequestPermissionsResult (requestCode, permissions, grantResults);
    if (grantResults.length == 0 || grantResults == null) {
        return;
    }
    if (grantResults [0] == PackageManager.PERMISSION_GRANTED) {
        return;
    }
    if (grantResults [0] == PackageManager.PERMISSION_DENIED) {
        return;
    }
}
""",
"Refd906fcb2": r"""
long pow (long a, int b) {
    if (b <= 1) return b == 0 ? 1 : a;
    long half = pow (a * a, b / 2);
    return isEven (b) ? half : a * half;
}
"""
}

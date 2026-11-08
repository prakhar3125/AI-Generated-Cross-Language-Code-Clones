DATA_C5 = {
"Rd40ca7a94c": r"""
public final void contextDestroyed (ServletContextEvent sce) {
    ClassLoader cl = Thread.currentThread ().getContextClassLoader ();
    Enumeration < Driver > drivers = DriverManager.getDrivers ();
    while (drivers.hasMoreElements ()) {
        Driver driver = drivers.nextElement ();
        if (driver.getClass ().getClassLoader () != cl) {
            log.trace ("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver);
            continue;
        }
        try {
            log.info ("Deregistering JDBC driver {}", driver);
            DriverManager.deregisterDriver (driver);
        } catch (SQLException ex) {
            log.error ("Error deregistering JDBC driver {}", driver, ex);
        }
    }
}
""",
"R3c52337f3a": r"""
internal static string GetIPAddress (HttpRequestBase request) {
    string forwarded = ExtractForwardedAddress(request);
    if (forwarded != null) {
        return forwarded;
    }
    string xForwardedFor = request.Headers ["X-Forwarded-For"];
    if (! String.IsNullOrEmpty (xForwardedFor)) {
        return xForwardedFor.Split (',') [0];
    }
    return request.UserHostAddress;
}

private static string ExtractForwardedAddress (HttpRequestBase request) {
    string forwarded = request.Headers ["Forwarded"];
    if (String.IsNullOrEmpty (forwarded)) {
        return null;
    }
    foreach (string segment in forwarded.Split (',') [0].Split (';')) {
        string [] pair = segment.Trim ().Split ('=');
        if (pair.Length != 2 || ! pair [0].Equals ("for", StringComparison.OrdinalIgnoreCase)) {
            continue;
        }
        return StripPortOrBrackets(pair [1].Trim ('"'));
    }
    return null;
}

private static string StripPortOrBrackets (string ip) {
    int left = ip.IndexOf ('[');
    if (left == 0) {
        int right = ip.IndexOf (']');
        return ip.Substring (1, right - 1);
    }
    int colon = ip.IndexOf (':');
    if (colon != - 1) {
        return ip.Substring (0, colon);
    }
    return ip;
}
"""
}

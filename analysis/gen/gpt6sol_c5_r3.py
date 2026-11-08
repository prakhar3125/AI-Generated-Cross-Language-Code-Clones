DATAR3 = {}

DATAR3["R7da0cb9ba0"] = '''using System.Text;

public static class TextDuplicator
{
    public static string Duplicate(string inText)
    {
        StringBuilder sb = new StringBuilder();
        int counter = 0;
        while (counter < inText.Length)
        {
            if (counter % 4 == 0)
            {
                sb.Append(sb.ToString());
                sb.Append('-');
            }
            sb.Append(inText.Substring(counter, 1));
            counter++;
        }
        return sb.ToString();
    }
}'''

DATAR3["R06eb22ea20"] = '''using System;
using System.Diagnostics;

public static class StackFrameLogger
{
    private static bool LogFrame(StackFrame frame, string methodName, Exception e)
    {
        int lineNum = frame.GetFileLineNumber();
        int colNum = frame.GetFileColumnNumber();
        Console.WriteLine("Error in " + methodName + ": " + e.Message + " at " + lineNum + "," + colNum);
        return lineNum + colNum > 0;
    }

    public static bool LogError(Exception e)
    {
        StackTrace stackTrace = new StackTrace(e, true);
        int frameIndex = 0;
        bool logged = false;
        while (frameIndex < 3 && frameIndex < stackTrace.FrameCount)
        {
            if (LogFrame(stackTrace.GetFrame(frameIndex), "LogError", e))
            {
                logged = true;
                break;
            }
            frameIndex++;
        }
        return logged;
    }
}'''

DATAR3["R63b80bd2a7"] = '''import java.util.Arrays;

public class ZipfHistogram {

    private static int[] buildHistogram(ZipfGenerator zipf, int size, int trials) {
        int[] hist = new int[size];
        Arrays.fill(hist, 0);
        int i = 0;
        while (i++ < trials) {
            hist[zipf.next()]++;
        }
        return hist;
    }

    public static void main(String[] args) {
        ZipfGenerator zipf = new ZipfGenerator(10, 1.0);
        int[] hist = buildHistogram(zipf, 10, 10000);
        for (int i = 0; i < hist.length; i++) {
            System.out.println((i + 1) + ": " + hist[i]);
        }
    }
}'''

DATAR3["R359253b811"] = '''import javax.swing.JFrame;
import javax.swing.JTextPane;

public class TextPaneFrame extends JFrame {

    private JTextPane createTextPane(String text) {
        JTextPane textPane = new JTextPane();
        textPane.setText(text);
        textPane.setEditable(false);
        return textPane;
    }

    public TextPaneFrame(String title, String text) {
        setTitle(title);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(createTextPane(text));
        setSize(400, 300);
        setVisible(true);
        if (text == null || text.isEmpty()) {
            return;
        }
        System.out.println("Pane ready: " + title);
    }
}'''

DATAR3["Reb0aa16636"] = '''public class PrimeCheck {

    public static boolean isPrime(int number) {
        if (number < 2 || number % 2 == 0) {
            return number == 2;
        }
        int i = 3;
        while (i * i <= number) {
            if (number % i == 0) {
                return false;
            }
            i += 2;
        }
        return true;
    }
}'''

DATAR3["Rcfc9023e76"] = '''public class DigitSum {

    public static int sumDigits(String number) {
        int total = 0;
        int index = 0;
        while (index < number.length()) {
            total += Character.getNumericValue(number.charAt(index));
            index++;
        }
        return total;
    }
}'''

DATAR3["R9f056ca258"] = '''import java.io.BufferedWriter;
import java.io.IOException;

public class TreePrinter {

    private String extend(String indent, boolean isRight, boolean forRightChild) {
        boolean first = (isRight == forRightChild);
        return indent + (first ? "        " : " |      ");
    }

    private void printNode(Node node, String indent, boolean isRight, BufferedWriter out) throws IOException {
        out.write(isRight ? " /" : " \\");
        out.write(node.getValue() + "\\n");
        if (node.getLeft() != null) {
            out.write(extend(indent, isRight, false));
            printNode(node.getLeft(), extend(indent, isRight, false), false, out);
        }
        if (node.getRight() != null) {
            out.write(extend(indent, isRight, true));
            printNode(node.getRight(), extend(indent, isRight, true), true, out);
        }
    }
}'''

DATAR3["Rb2a2baaff7"] = '''public class SievePrint {

    public static void main(String[] args) {
        java.util.BitSet bits = new java.util.BitSet();
        bits.set(1, 100 + 1);
        String set = bits.toString();
        System.out.append(set, 1, set.length() - 1);
        System.out.println();
    }
}'''

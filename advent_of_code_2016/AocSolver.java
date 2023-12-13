import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;

public abstract class AocSolver {

    public String default_filename;

    public AocSolver() {
        default_filename = "test.txt";
    }
    public AocSolver(String filename) {
        default_filename = filename;
    }

    public List<String> getLines(Scanner scan) {
        List<String> lines = new ArrayList<>();
        while (scan.hasNextLine()) {
            lines.add(scan.nextLine());
        }
        return lines;
    }

    public abstract void solve(Scanner scan);

    public void run(String[] argv) {
        String filename = this.default_filename;
        if (argv.length > 0) {
            filename = argv[0];
        }
        Scanner scan = openFile(filename);
        if (scan == null) {
            System.out.printf("File %s not found.\n", filename);
            return;
        }
        solve(scan);
    }

    public Scanner openFile(String filename) {
        try {
            File file = new File(filename);
            Scanner scan = new Scanner(file);
            return scan;
        } catch (FileNotFoundException e) {
            return null;
        }
    }
}

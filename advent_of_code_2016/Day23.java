import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Computer {
    public int regA;
    public int regB;
    public int regC;
    public int regD;
    public int ip;
    public List<Instruction> programCode;

    public Computer(List<Instruction> programCode) {
        this.programCode = programCode;
        reset();
    }

    public void reset() {
        regA = 0;
        regB = 0;
        regC = 0;
        regD = 0;
        ip = 0;
        for (Instruction i : programCode) {
            i.toggled = false;
        }
    }

    public int getReg(int reg) {
        switch (reg) {
            case 0:
                return this.regA;
            case 1:
                return this.regB;
            case 2:
                return this.regC;
            case 3:
                return this.regD;
            default:
                return 0;
        }
    }
    public void setReg(int reg, int value) {
        switch (reg) {
            case 0:
                regA = value;
                return;
            case 1:
                regB = value;
                return;
            case 2:
                regC = value;
                return;
            case 3:
                regD = value;
                return;
        }
    }
    public void jump(int value) {
        ip += value - 1;
    }

    public void run() {
        while (0 <= ip && ip < programCode.size()) {
            programCode.get(ip).execute(this);
            ip++;
        }
    }

    public void toggle(int value) {
        int toggleIp = ip + value;
        if (0 <= toggleIp && toggleIp < programCode.size()) {
            programCode.get(ip + value).toggle();
        }
    }
}

abstract class Param {
    public int value;
    
    public Param(int value) {
        this.value = value;
    }

    public int getValue() {
        return this.value;
    }

    public abstract int resolveValue(Computer c);
}

class LiteralParam extends Param {
    public LiteralParam(int value) {
        super(value);
    }

    public int resolveValue(Computer c) {
        return value;
    }
}
class RegisterParam extends Param {
    public RegisterParam(int value) {
        super(value);
    }
    @Override
    public int resolveValue(Computer c) {
        return c.getReg(value);
    }
}

abstract class Instruction {
    public Param param1;
    public Param param2;
    public String type;
    public boolean toggled;

    public Instruction(Param param1, Param param2) {
        this.param1 = param1;
        this.param2 = param2;
        this.toggled = false;
    }

    public abstract void execute(Computer c);

    public void toggle() {
        this.toggled = !this.toggled;
    }
}
class CPY extends Instruction {

    public CPY(Param param1, Param param2) {
        super(param1, param2);
        type = "cpy";
    }
    @Override
    public void execute(Computer c) {
        if (toggled) {
            Instruction ins = new JNZ(param1, param2);
            ins.execute(c);
            return;
        }
        if (param2 instanceof RegisterParam) {
            c.setReg(param2.getValue(), param1.resolveValue(c));
        }
    }
}
class INC extends Instruction {

    public INC(Param param1) {
        super(param1, null);
        type = "inc";
    }
    @Override
    public void execute(Computer c) {
        if (toggled) {
            Instruction ins = new DEC(param1);
            ins.execute(c);
            return;
        }
        int a = c.getReg(param1.getValue()) + 1;
        c.setReg(param1.getValue(), a);
    }
}
class DEC extends Instruction {

    public DEC(Param param1) {
        super(param1, null);
        type = "dec";
    }
    @Override
    public void execute(Computer c) {
        if (toggled) {
            Instruction ins = new INC(param1);
            ins.execute(c);
            return;
        }
        int a = c.getReg(param1.getValue()) - 1;
        c.setReg(param1.getValue(), a);
    }
}
class JNZ extends Instruction {

    public JNZ(Param param1, Param param2) {
        super(param1, param2);
        type = "jnz";
    }
    @Override
    public void execute(Computer c) {
        if (toggled) {
            Instruction ins = new CPY(param1, param2);
            ins.execute(c);
            return;
        }
        if (param1.resolveValue(c) != 0) {
            c.jump(param2.resolveValue(c));
        }
    }
}
class TGL extends Instruction {

    public TGL(Param param1) {
        super(param1, null);
        type = "tgl";
    }
    @Override
    public void execute(Computer c) {
        if (toggled) {
            Instruction ins = new INC(param1);
            ins.execute(c);
            return;
        }
        c.toggle(param1.resolveValue(c));
    }
}

public class Day23 extends AocSolver {

    public Day23(String filename) {
        super(filename);
    }

    private Param parseParam(String param) {
        int testReg = param.charAt(0) - 'a';

        if (0 <= testReg && testReg <= 4) {
            return new RegisterParam(testReg);
        } else {
            return new LiteralParam(Integer.parseInt(param));
        }
    }
    private List<Instruction> parseInstructions(List<String> lines) {
        List<Instruction> ls = new ArrayList<>();
        for (String line : lines) {
            String[] tokens = line.split(" ");
            String instruction = tokens[0];
            if (instruction.equals("cpy")) {
                Param param1 = parseParam(tokens[1]);
                Param param2 = parseParam(tokens[2]);
                ls.add(new CPY(param1, param2));
            } else if (instruction.equals("inc")) {
                Param param1 = parseParam(tokens[1]);
                ls.add(new INC(param1));
            } else if (instruction.equals("dec")) {
                Param param1 = parseParam(tokens[1]);
                ls.add(new DEC(param1));
            } else if (instruction.equals("jnz")) {
                Param param1 = parseParam(tokens[1]);
                Param param2 = parseParam(tokens[2]);
                ls.add(new JNZ(param1, param2));
            } else if (instruction.equals("tgl")) {
                Param param1 = parseParam(tokens[1]);
                ls.add(new TGL(param1));
            } else {
                System.out.println("Unknown instruction " + line);
            }
        }
        return ls;
    }

    @Override
    public void solve(Scanner scan) {
        List<String> instructionString = getLines(scan);
        scan.close();
        List<Instruction> programCode = parseInstructions(instructionString);
        Computer c = new Computer(programCode);
        c.setReg(0, 7);
        c.run();
        System.out.println("Part 1: " + c.getReg(0));
        c.reset();
        c.setReg(0, 12);
        c.run();
        System.out.println("Part 2: " + c.getReg(0));
    } 

    public static void main(String[] argv) {
        AocSolver solver = new Day23("input23.txt");
        solver.run(argv);
    }    
}

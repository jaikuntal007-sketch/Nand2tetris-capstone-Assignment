"""
assembler.py - Two-pass Hack assembler (Nand to Tetris, Capstone)
Name : Jai Kuntal        Roll No : 2501730416        K = 16

K mod 3 = 1: the optional symbols.txt feature is not required for this submission.

Usage:  python assembler.py Prog.asm      ->  Prog.hack  (+ symbols.txt)
"""
import sys

# ---------------- lookup tables ----------------
PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
for n in range(16):
    PREDEFINED["R" + str(n)] = n

# comp field = a-bit + c1..c6
COMP = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "M":   "1110000",
    "!D":  "0001101", "!A":  "0110001", "!M":  "1110001",
    "-D":  "0001111", "-A":  "0110011", "-M":  "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
# the destination letters may be written in any order (e.g. DM= as well as MD=)
for _d in list(DEST):
    _bits = DEST[_d]
    for _p in __import__("itertools").permutations(_d):
        DEST["".join(_p)] = _bits
# commutative operations may have the operands swapped (A+D, M&D, D|M ...)
for _c in list(COMP):
    for _op in "+&|":
        if _op in _c:
            _l, _r = _c.split(_op)
            COMP[_r + _op + _l] = COMP[_c]
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def clean(line):
    """Strip comment and all whitespace from one source line."""
    return "".join(line.split("//")[0].split())


# ---------------- PASS 1 : labels ----------------
def first_pass(lines):
    """Return (instructions, label_table).
    instructions = list of (source_line_no, text) with labels/comments/blanks removed
    label_table  = {label: ROM address of the instruction that follows it}"""
    instructions, labels = [], {}
    for no, raw in enumerate(lines, 1):
        text = clean(raw)
        if not text:
            continue
        if text[0] == "(" and text[-1] == ")":
            name = text[1:-1]
            if name in labels:
                print(f"Warning: Line {no}: label '{name}' defined more than once")
            labels[name] = len(instructions)      # next instruction's address
        else:
            instructions.append((no, text))
    return instructions, labels


# ---------------- PASS 2 : binary ----------------
def second_pass(instructions, labels):
    """Return (binary_lines, variables)."""
    table = dict(PREDEFINED)
    table.update(labels)
    variables = {}
    next_ram = 16
    out = []
    for no, text in instructions:
        if text[0] == "@":                         # A-instruction
            sym = text[1:]
            if sym.isdigit():
                value = int(sym)
            else:
                if sym not in table:               # new variable
                    table[sym] = next_ram
                    variables[sym] = next_ram
                    next_ram += 1
                value = table[sym]
            out.append(format(value, "016b"))
        else:                                      # C-instruction  dest=comp;jump
            dest = jump = ""
            comp = text
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)
            try:
                out.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
            except KeyError:
                sys.exit(f"Line {no}: invalid instruction '{text}'")
    return out, variables


def write_symbols(labels, variables, path="symbols.txt"):
    """K mod 3 == 0 feature: save every label and variable with its address."""
    with open(path, "w") as f:
        f.write("LABELS (ROM address)\n")
        for name, addr in labels.items():
            f.write(f"{name:<15}{addr}\n")
        f.write("\nVARIABLES (RAM address)\n")
        for name, addr in variables.items():
            f.write(f"{name:<15}{addr}\n")


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        sys.exit("Usage: python assembler.py Prog.asm")
    src = sys.argv[1]
    with open(src) as f:
        lines = f.readlines()

    instructions, labels = first_pass(lines)
    binary, variables = second_pass(instructions, labels)

    dst = src[:-4] + ".hack"
    with open(dst, "w") as f:
        f.write("\n".join(binary) + "\n")
    if 16 % 3 == 0:
        write_symbols(labels, variables)
    else:
        import os
        if os.path.exists("symbols.txt"):
            os.remove("symbols.txt")
    print(f"{src} -> {dst}: {len(binary)} instructions, "
          f"{len(labels)} labels, {len(variables)} variables")


if __name__ == "__main__":
    main()

# Program 1: Generate Symbol Table and Literal Table

# Static ALP code
alp = [
    "START 200",
    "READ A",
    "MOVER AREG, =10",
    "ADD BREG, =5",
    "MOVEM AREG, RESULT",
    "A DS 1",
    "RESULT DS 1",
    "PRINT RESULT",
    "STOP",
    "END"
]

symbol_table = {}
literal_table = {}
lc = 0
lit_count = 0

opcodes = {"MOVER", "ADD", "SUB", "MULT", "MOVEM", "COMP", "BC", "DIV", "READ", "PRINT", "STOP"}
directives = {"START", "END", "DS", "DC"}

for line in alp:
    parts = line.replace(",", "").split()

    # START
    if parts[0] == "START":
        lc = int(parts[1])
        continue

    label = None

    # Detect label
    if parts[0] not in opcodes and parts[0] not in directives:
        label = parts[0]
        symbol_table[label] = lc
        parts = parts[1:]   # remove label

    # Literal handling
    for word in parts:
        if word.startswith("="):
            lit_count += 1
            literal_table[f"L{lit_count}"] = word

    lc += 1

# Output
print("Symbol Table:")
for sym, addr in symbol_table.items():
    print(sym, "->", addr)

print("\nLiteral Table:")
for lit, val in literal_table.items():
    print(lit, "->", val)


# Program 2: Base Table and LC

alp = [
    "START 200",
    "BASE 300",
    "MOVER AREG, X",
    "ADD BREG, Y",
    "X DS 1",
    "Y DS 1",
    "END"
]

lc = 0
base_table = {}
symbol_table = {}
lc_table = []

opcodes = {"MOVER", "ADD", "SUB", "MULT", "MOVEM", "COMP", "BC", "DIV", "READ", "PRINT", "STOP"}
directives = {"START", "END", "DS", "DC", "BASE"}

for line in alp:
    parts = line.replace(",", "").split()

    # START
    if parts[0] == "START":
        lc = int(parts[1])
        continue

    # Store LC before execution
    lc_table.append((line, lc))

    # BASE
    if parts[0] == "BASE":
        base_table["BASE"] = int(parts[1])

    else:
        label = None

        # Detect label
        if parts[0] not in opcodes and parts[0] not in directives:
            label = parts[0]
            symbol_table[label] = lc
            parts = parts[1:]

        # DS directive
        if "DS" in parts:
            lc += int(parts[-1])
            continue

    lc += 1

# Output
print("Base Table:")
for k, v in base_table.items():
    print(k, "->", v)

print("\nLocation Counter (LC):")
for line, loc in lc_table:
    print(loc, ":", line)


# Program 3: MOT, POT and LC

alp = [
    "START 100",
    "MOVER AREG, X",
    "ADD BREG, Y",
    "X DS 1",
    "Y DS 1",
    "STOP",
    "END"
]

# MOT and POT
MOT = {
    "MOVER": "04",
    "ADD": "01",
    "STOP": "00"
}

POT = {
    "START": "AD",
    "END": "AD",
    "DS": "DL"
}

lc = 0
symbol_table = {}
lc_table = []

opcodes = set(MOT.keys())
directives = set(POT.keys())

# PASS 1 → Build Symbol Table + LC
for line in alp:
    parts = line.replace(",", "").split()

    if parts[0] == "START":
        lc = int(parts[1])
        continue

    # Store LC
    lc_table.append((lc, line))

    # Detect label
    if parts[0] not in opcodes and parts[0] not in directives:
        label = parts[0]
        symbol_table[label] = lc
        parts = parts[1:]

    # DS handling
    if "DS" in parts:
        lc += int(parts[-1])
    else:
        lc += 1

# OUTPUT

print("MOT Table:")
for k, v in MOT.items():
    print(k, "->", v)

print("\nPOT Table:")
for k, v in POT.items():
    print(k, "->", v)

print("\nSymbol Table:")
for sym, addr in symbol_table.items():
    print(sym, "->", addr)

print("\nLC Contents:")
for loc, line in lc_table:
    print(loc, ":", line)

alp = [
    "MACRO",
    "INCR &ARG1",
    "ADD AREG, &ARG1",
    "MEND",
    "START",
    "INCR NUM",
    "END"
]

mnt = {}
mdt = []
ala_table = {}

i = 0

while i < len(alp):
    line = alp[i]

    if line == "MACRO":
        i += 1
        parts = alp[i].split()

        macro_name = parts[0]
        params = parts[1:]

        # Build ALA with positional mapping
        ala = {}
        for idx, param in enumerate(params):
            ala[param] = f"#{idx+1}"

        ala_table[macro_name] = ala

        # Store in MNT (name → MDT index, param count)
        mnt[macro_name] = (len(mdt), len(params))

        i += 1

        # Store MDT with positional parameters
        while alp[i] != "MEND":
            line = alp[i]

            for param in ala:
                line = line.replace(param, ala[param])

            mdt.append(line)
            i += 1

        mdt.append("MEND")

    i += 1


# OUTPUT
print("MNT (Macro Name Table):")
for name, (idx, count) in mnt.items():
    print(name, "-> MDT Index:", idx, ", Params:", count)

print("\nMDT (Macro Definition Table):")
for i, line in enumerate(mdt):
    print(i, ":", line)

print("\nALA Table:")
for macro, ala in ala_table.items():
    print(macro, ":", ala)


# Program 5: Macro Expansion using predefined tables

# Predefined tables
MNT = {
    "INCR": (0, 1)
}

MDT = [
    "ADD AREG, #1",
    "MEND"
]

alp = [
    "START",
    "INCR NUM",
    "END"
]

# 🔹 Print MNT
print("MNT (Macro Name Table):")
for name, (idx, count) in MNT.items():
    print(name, "-> MDT Index:", idx, ", Params:", count)

# 🔹 Print MDT
print("\nMDT (Macro Definition Table):")
for i, line in enumerate(MDT):
    print(i, ":", line)

# 🔹 Expansion
print("\nExpanded Code:\n")

for line in alp:
    parts = line.split()

    if parts[0] in MNT:
        mdt_index, param_count = MNT[parts[0]]

        # ALA
        ala = {}
        for i in range(param_count):
            ala[f"#{i+1}"] = parts[i+1]

        # Expand
        i = mdt_index
        while MDT[i] != "MEND":
            expanded = MDT[i]
            for key in ala:
                expanded = expanded.replace(key, ala[key])
            print(expanded)
            i += 1
    else:
        print(line)

# Program 6: Identify Macro and Expand

alp = [
    "MACRO",
    "INCR &ARG1",
    "ADD AREG, &ARG1",
    "MEND",
    "START",
    "INCR NUM",
    "END"
]

mnt = {}
mdt = []

i = 0
inside_macro = False

print("Expanded Code:\n")

while i < len(alp):
    line = alp[i]
    parts = line.replace(",", "").split()

    # 🔹 Start macro definition
    if parts[0] == "MACRO":
        inside_macro = True
        i += 1

        parts = alp[i].split()
        macro_name = parts[0]
        params = parts[1:]

        mnt[macro_name] = len(mdt)

        ala = {}
        for idx, p in enumerate(params):
            ala[p] = f"#{idx+1}"

        i += 1

        # Store MDT with positional params
        while alp[i] != "MEND":
            line = alp[i]
            for p in ala:
                line = line.replace(p, ala[p])
            mdt.append(line)
            i += 1

        mdt.append("MEND")
        inside_macro = False

    # 🔹 Macro call → expand immediately
    elif parts[0] in mnt:
        macro_name = parts[0]
        args = parts[1:]

        # Build ALA
        ala = {}
        for idx, arg in enumerate(args):
            ala[f"#{idx+1}"] = arg

        idx = mnt[macro_name]

        while mdt[idx] != "MEND":
            expanded = mdt[idx]
            for key in ala:
                expanded = expanded.replace(key, ala[key])
            print(expanded)
            idx += 1

    # 🔹 Normal instruction
    elif parts[0] not in ["MEND"]:
        print(line)

    i += 1

# Program 7: Detect Left Recursion

# Static grammar (Dictionary format)
grammar = {
    "A": ["A a", "b"],
    "B": ["c B", "d"],
    "C": ["C d", "e"]
}

print("Left Recursion Detection:\n")

for non_terminal in grammar:
    productions = grammar[non_terminal]
    left_recursive = False

    for prod in productions:
        first_symbol = prod.split()[0]

        # Check if production starts with same non-terminal
        if first_symbol == non_terminal:
            left_recursive = True
            print(f"{non_terminal} -> {prod}  (Left Recursive)")

    if not left_recursive:
        print(f"{non_terminal} has NO left recursion")

# Program 8: Lexical Analyzer (Keywords, Identifiers, Symbols)

import re

code = """
int main() {
    int a = 10;
    float b = a + 5;
    return 0;
}
"""

# Predefined sets
keywords = {"int", "float", "return", "if", "else", "while"}
symbols = {'+', '-', '*', '/', '=', ';', '(', ')', '{', '}'}

found_keywords = set()
identifiers = set()
found_symbols = set()

# Tokenize using regex
tokens = re.findall(r"[a-zA-Z_]\w*|[^\s]", code)

for token in tokens:
    if token in keywords:
        found_keywords.add(token)
    elif token in symbols:
        found_symbols.add(token)
    elif re.match(r"[a-zA-Z_]\w*", token):
        identifiers.add(token)

# Output
print("Keywords:", found_keywords)
print("Identifiers:", identifiers)
print("Symbols:", found_symbols)

# Program 9: Lexical Analyzer (Numbers, Identifiers, Preprocessor Directives)

import re

code = """
#include <stdio.h>
#define MAX 100

int main() {
    int a = 10;
    float b = 20.5;
    return 0;
}
"""

identifiers = set()
numbers = set()
preprocessor = []

lines = code.split("\n")

for line in lines:
    line = line.strip()

    # Preprocessor directive
    if line.startswith("#"):
        preprocessor.append(line)

    # Find tokens
    tokens = re.findall(r"[a-zA-Z_]\w*|\d+\.\d+|\d+", line)

    for token in tokens:
        if re.match(r"\d+\.\d+|\d+", token):
            numbers.add(token)
        elif re.match(r"[a-zA-Z_]\w*", token):
            identifiers.add(token)

# Output
print("Preprocessor Directives:")
for p in preprocessor:
    print(p)

print("\nIdentifiers:", identifiers)
print("Numbers:", numbers)

# Program 11: Code Optimization Techniques

expressions = [
    "a = b + 0",
    "c = a + 5",
    "d = b + 0",
    "e = 2 + 3",
    "f = e"
]

optimized = []
computed = {}   # for common subexpression
values = {}     # for constants / copy propagation

for exp in expressions:
    lhs, rhs = exp.split("=")
    lhs = lhs.strip()
    rhs = rhs.strip()

    # --- Constant Folding ---
    try:
        result = eval(rhs)
        values[lhs] = result
        optimized.append(f"{lhs} = {result}")
        continue
    except:
        pass

    # --- Algebraic Simplification ---
    if "+ 0" in rhs:
        rhs = rhs.replace("+ 0", "").strip()

    # --- Copy Propagation ---
    if rhs in values:
        rhs = str(values[rhs])

    # --- Common Subexpression Elimination ---
    if rhs in computed:
        optimized.append(f"{lhs} = {computed[rhs]}")
    else:
        computed[rhs] = lhs
        optimized.append(f"{lhs} = {rhs}")

# Output
print("Optimized Code:\n")
for line in optimized:
    print(line)

# Program 12: 3-Address Code (Triples)

expression = "a = b + c * d"

triples = []
temp_count = 0

# Split LHS and RHS
lhs, rhs = expression.split("=")
lhs = lhs.strip()
tokens = rhs.strip().split()

# Step 1: Handle * and /
i = 0
while i < len(tokens):
    if tokens[i] in ["*", "/"]:
        op = tokens[i]
        arg1 = tokens[i-1]
        arg2 = tokens[i+1]

        triples.append((temp_count, op, arg1, arg2))

        # Replace with reference
        tokens[i-1:i+2] = [f"({temp_count})"]
        temp_count += 1
        i = 0
    else:
        i += 1

# Step 2: Handle + and -
i = 0
while i < len(tokens):
    if tokens[i] in ["+", "-"]:
        op = tokens[i]
        arg1 = tokens[i-1]
        arg2 = tokens[i+1]

        triples.append((temp_count, op, arg1, arg2))

        tokens[i-1:i+2] = [f"({temp_count})"]
        temp_count += 1
        i = 0
    else:
        i += 1

# Step 3: Assignment
triples.append((temp_count, "=", lhs, tokens[0]))

# Output
print("Triples Representation:\n")
for t in triples:
    print(t)

# Program 14: Lexical Analyzer (Remove Comments, Identify Tokens)

import re

code = """
// This is a comment
int main() {
    int a = 10; /* multi-line
    comment */
    float b = a + 5;
    return 0;
}
"""

# --- Remove comments ---
code = re.sub(r"//.*", "", code)              # single-line
code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)  # multi-line

# --- Define symbols ---
symbols = {'+', '-', '*', '/', '=', ';', '(', ')', '{', '}'}

identifiers = set()
found_symbols = set()

tokens = re.findall(r"[a-zA-Z_]\w*|[^\s]", code)

for token in tokens:
    if token in symbols:
        found_symbols.add(token)
    elif re.match(r"[a-zA-Z_]\w*", token):
        identifiers.add(token)

# Output
print("Code after removing comments:\n")
print(code)

print("\nIdentifiers:", identifiers)
print("Symbols:", found_symbols)
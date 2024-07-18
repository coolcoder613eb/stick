from typing import Dict, List

test_code = """PUSH 8
; Doubling routine
BEGIN DUB
PUSH 2
MUL
END
DUP
PUSH 2
; Modulo
MOD
PUSH 0
CMP
IF DUB
DUP
SHOW
DUB
DUP
SHOW
"""


class Interpreter:
    int_stack = []
    def_stack = []
    defs: Dict[str, List] = {}

    def run(self, line: str):
        toks = line.lstrip().split(None, 1)
        # print(toks,self.defs,self.def_stack,self.int_stack)
        if toks[0].strip().startswith(";"):
            print("Comment:", line)
        elif len(self.def_stack) > 0:
            if len(self.def_stack) == 1:
                if toks[0].upper() == "END":
                    if len(toks) > 0 and len(toks) < 3:
                        print("End:", self.def_stack[-1])
                        self.def_stack.pop()
                        return
                    else:
                        raise Exception(
                            f"{len(toks)}: Incorrect number of arguments for END!"
                        )
            self.defs[self.def_stack[-1]].append(line)
        elif len(self.def_stack) == 0:
            if toks[0].upper() == "PUSH":
                if len(toks) == 2:
                    value = int(toks[1])
                    print("Push:", value)
                    self.int_stack.append(value)
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for PUSH!"
                    )
            elif toks[0].upper() == "SHOW":
                if len(toks) == 1:
                    print("Show")
                    print(self.int_stack.pop())
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for SHOW!"
                    )
            elif toks[0].upper() == "IF":
                if len(toks) == 2:
                    name = toks[1]
                    if name in self.defs:
                        print("If:", name)
                        if self.int_stack.pop():
                            for def_line in self.defs[name]:
                                self.run(def_line)
                    else:
                        raise Exception(f"{name}: Unknown Label!")
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for BEGIN!"
                    )
            elif toks[0].upper() == "DUP":
                if len(toks) == 1:
                    print("Dup")
                    self.int_stack.append(self.int_stack[-1])
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for DUP!"
                    )
            elif toks[0].upper() == "ADD":
                if len(toks) == 1:
                    print("Add")
                    self.int_stack.append(self.int_stack.pop(-2) + self.int_stack.pop())
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for ADD!"
                    )
            elif toks[0].upper() == "SUB":
                if len(toks) == 1:
                    print("Sub")
                    self.int_stack.append(self.int_stack.pop(-2) - self.int_stack.pop())
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for SUB!"
                    )
            elif toks[0].upper() == "DIV":
                if len(toks) == 1:
                    print("Div")
                    self.int_stack.append(
                        self.int_stack.pop(-2) // self.int_stack.pop()
                    )
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for DIV!"
                    )
            elif toks[0].upper() == "MUL":
                if len(toks) == 1:
                    print("Mul")
                    self.int_stack.append(self.int_stack.pop(-2) * self.int_stack.pop())
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for MUL!"
                    )
            elif toks[0].upper() == "MOD":
                if len(toks) == 1:
                    print("Mod")
                    self.int_stack.append(self.int_stack.pop(-2) % self.int_stack.pop())
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for MOD!"
                    )
            elif toks[0].upper() == "CMP":
                if len(toks) == 1:
                    print("Cmp")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) == self.int_stack.pop())
                    )
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for CMP!"
                    )
            elif toks[0].upper() == "AND":
                if len(toks) == 1:
                    print("And")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) and self.int_stack.pop())
                    )
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for AND!"
                    )
            elif toks[0].upper() == "OR":
                if len(toks) == 1:
                    print("Or")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) or self.int_stack.pop())
                    )
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for OR!"
                    )
            elif toks[0].upper() == "BEGIN":
                if len(toks) == 2:
                    name = toks[1]
                    print("Begin:", name)
                    self.def_stack.append(name)
                    self.defs[name] = []
                else:
                    raise Exception(
                        f"{len(toks)}: Incorrect number of arguments for BEGIN!"
                    )
            elif toks[0] in self.defs:
                name = toks[0]
                print(name.capitalize())
                for def_line in self.defs[name]:
                    self.run(def_line)


def main():
    interp = Interpreter()
    for line in test_code.splitlines():
        interp.run(line)
    print(
        "\n".join(
            [
                f"{x}: {interp.__getattribute__(x)}"
                for x in dir(interp)
                if not x.startswith("__")
            ]
        )
    )


if __name__ == "__main__":
    main()

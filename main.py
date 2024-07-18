from typing import Dict, List

test_code = """PUSH 8
BEGIN DUB
PUSH 2
MUL
END
DUP
PUSH 2
MOD
PUSH 0
CMP
IF DUB
SHOW
 ; TEST
ECHO Hello, World!
"""


class Interpreter:
    int_stack = []
    def_stack = []
    defs: Dict[str, List] = {}

    def run(self, line: str):
        toks = line.lstrip().split(None, 1)
        # print(toks,self.defs,self.def_stack)
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
                        raise Exception("Incorrect number of arguments for END!")
            self.defs[self.def_stack[-1]].append(line)
        elif len(self.def_stack) == 0:
            if toks[0].upper() == "PUSH":
                if len(toks) == 2:
                    value = int(toks[1])
                    print("Push:", value)
                    self.int_stack.append(value)
                else:
                    raise Exception("Incorrect number of arguments for PUSH!")
            elif toks[0].upper() == "BEGIN":
                if len(toks) == 2:
                    name = toks[1]
                    print("Begin:", name)
                    self.def_stack.append(name)
                    self.defs[name] = []
                else:
                    raise Exception("Incorrect number of arguments for BEGIN!")


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

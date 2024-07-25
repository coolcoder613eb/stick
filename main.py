from typing import Dict, List

VERSION="0.1"
DEBUG=False

class StickError(SyntaxError):
    pass

def dprint(*args):
    if DEBUG:
        print(*args)


class Interpreter:
    int_stack = []
    def_stack = []
    defs: Dict[str, List] = {}
    memory=[0]*512

    def run(self, line: str):
        toks = line.lstrip().split(None, 1)
        if line.strip()=="":
            dprint("Empty line.")
        elif toks[0].strip().startswith(";"):
            dprint("Comment:", line)
        elif toks[0].upper() == "BEGIN":
            if len(toks) == 2:
                name = toks[1]
                dprint("Begin:", name)
                self.def_stack.append(name)
                self.defs[name] = []
            else:
                raise StickError(
                    f"{len(toks)}: Incorrect number of arguments for BEGIN!"
                )
        elif len(self.def_stack) > 0:
            if toks[0].upper() == "END":
                if len(toks) > 0 and len(toks) < 3:
                    dprint("End:", self.def_stack[-1])
                    self.def_stack.pop()
                    return
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for END!"
                    )
            else:
                self.defs[self.def_stack[-1]].append(line)
        elif len(self.def_stack) == 0:
            if toks[0].upper() == "PUSH":
                if len(toks) == 2:
                    value = int(toks[1])
                    dprint("Push:", value)
                    self.int_stack.append(value)
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for PUSH!"
                    )
            elif toks[0].upper() == "POP":
                if len(toks) == 1:
                    dprint("Pop")
                    self.int_stack.pop()
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for POP!"
                    )
            elif toks[0].upper() == "POKE":
                if len(toks) == 1:
                    addr=self.int_stack.pop()
                    value=self.int_stack.pop()
                    dprint("Poke:",addr,'=',value)
                    self.memory[addr]=value
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for POKE!"
                    )
            elif toks[0].upper() == "PEEK":
                if len(toks) == 1:
                    addr=self.int_stack.pop()
                    dprint("Peek:",addr)
                    self.int_stack.append(self.memory[addr])
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for PEEK!"
                    )
            elif toks[0].upper() == "SHOW":
                if len(toks) == 1:
                    dprint("Show")
                    print(self.int_stack[-1])
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for SHOW!"
                    )
            elif toks[0].upper() == "IF":
                if len(toks) == 2:
                    name = toks[1]
                    if name in self.defs:
                        dprint("If:", name)
                        cond = self.int_stack.pop()
                        if cond:
                            for def_line in self.defs[name]:
                                self.run(def_line)
                        self.int_stack.append(int(not cond))
                    else:
                        raise StickError(f"{name}: Unknown Label!")
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for IF!"
                    )
            elif toks[0].upper() == "WHILE":
                if len(toks) == 2:
                    name = toks[1]
                    if name in self.defs:
                        dprint("While:", name)
                        cond = self.int_stack.pop()
                        while cond:
                            for def_line in self.defs[name]:
                                self.run(def_line)
                            cond = self.int_stack.pop()
                    else:
                        raise StickError(f"{name}: Unknown Label!")
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for WHILE!"
                    )
            elif toks[0].upper() == "DUP":
                if len(toks) == 1:
                    dprint("Dup")
                    self.int_stack.append(self.int_stack[-1])
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for DUP!"
                    )
            elif toks[0].upper() == "ADD":
                if len(toks) == 1:
                    dprint("Add")
                    self.int_stack.append(self.int_stack.pop(-2) + self.int_stack.pop())
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for ADD!"
                    )
            elif toks[0].upper() == "SUB":
                if len(toks) == 1:
                    dprint("Sub")
                    self.int_stack.append(self.int_stack.pop(-2) - self.int_stack.pop())
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for SUB!"
                    )
            elif toks[0].upper() == "DIV":
                if len(toks) == 1:
                    dprint("Div")
                    self.int_stack.append(
                        self.int_stack.pop(-2) // self.int_stack.pop()
                    )
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for DIV!"
                    )
            elif toks[0].upper() == "MUL":
                if len(toks) == 1:
                    dprint("Mul")
                    self.int_stack.append(self.int_stack.pop(-2) * self.int_stack.pop())
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for MUL!"
                    )
            elif toks[0].upper() == "MOD":
                if len(toks) == 1:
                    dprint("Mod")
                    self.int_stack.append(self.int_stack.pop(-2) % self.int_stack.pop())
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for MOD!"
                    )
            elif toks[0].upper() == "CMP":
                if len(toks) == 1:
                    dprint("Cmp")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) == self.int_stack.pop())
                    )
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for CMP!"
                    )
            elif toks[0].upper() == "AND":
                if len(toks) == 1:
                    dprint("And")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) and self.int_stack.pop())
                    )
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for AND!"
                    )
            elif toks[0].upper() == "OR":
                if len(toks) == 1:
                    dprint("Or")
                    self.int_stack.append(
                        int(self.int_stack.pop(-2) or self.int_stack.pop())
                    )
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for OR!"
                    )
            elif toks[0].upper() == "NOT":
                if len(toks) == 1:
                    dprint("Not")
                    self.int_stack.append(
                        int(not self.int_stack.pop())
                    )
                else:
                    raise StickError(
                        f"{len(toks)}: Incorrect number of arguments for NOT!"
                    )
            elif toks[0] in self.defs:
                name = toks[0]
                dprint(name.capitalize())
                for def_line in self.defs[name]:
                    self.run(def_line)
            else:
                raise StickError(f"{toks[0]}: Unrecognised command!")
        dprint(self.int_stack)


def print_attrs(interp):
    print(
        "\n".join(
            [
                f"{x}: {interp.__getattribute__(x)}"
                for x in dir(interp)
                if not hasattr(interp.__getattribute__(x), "__call__")
                and not x.startswith("__")
            ]
        )
    )


def repl():
    import readline
    interp = Interpreter()
    print(f"Stick {VERSION} REPL")
    while True:
        try:
            line = input(". " if len(interp.def_stack) > 0 else "> ")
            if line.upper() == "BYE":
                break
            else:
                interp.run(line)
        except StickError as e:
            print("Error:", e)
        except EOFError:
            print()
            break
    print_attrs(interp)


def main():
    repl()


if __name__ == "__main__":
    main()

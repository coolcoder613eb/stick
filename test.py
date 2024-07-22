import main
import sys
from glob import glob

main.DEBUG=False
filenames=glob("tests/*.stk")

for filename in filenames:
    print("-",filename.upper())
    with open(filename) as f:
        code=f.read()

    interp = main.Interpreter()
    for line in code.splitlines():
        interp.run(line)
    # main.print_attrs(interp)

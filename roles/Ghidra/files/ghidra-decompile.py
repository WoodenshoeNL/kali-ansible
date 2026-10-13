#!/home/michel/tools/ghidramcp-1.4/venv/bin/python
"""Decompile a named function from a binary, no GUI needed.
Usage: ghidra-decompile.py <binary> [function_name]"""
import sys
import pyghidra

pyghidra.start()

with pyghidra.open_program(sys.argv[1], analyze=True) as flat:
    prog = flat.getCurrentProgram()
    target = sys.argv[2] if len(sys.argv) > 2 else "main"
    fm = prog.getFunctionManager()
    fn = None
    for f in fm.getFunctions(True):
        if target in f.getName():
            fn = f
            break
    if fn is None:
        print(f"function matching '{target}' not found")
        sys.exit(1)
    from ghidra.app.decompiler import DecompInterface
    from ghidra.util.task import ConsoleTaskMonitor
    di = DecompInterface()
    di.openProgram(prog)
    res = di.decompileFunction(fn, 120, ConsoleTaskMonitor())
    print(res.getDecompiledFunction().getC())

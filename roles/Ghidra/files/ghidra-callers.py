#!/home/michel/tools/ghidramcp-1.4/venv/bin/python
"""ghidra-callers.py — list callers (and decompile them) of functions whose
name matches a substring. Usage: ghidra-callers.py <binary> <name-substring>"""
import sys
import pyghidra

pyghidra.start()

with pyghidra.open_program(sys.argv[1], analyze=True) as flat:
    prog = flat.getCurrentProgram()
    fm = prog.getFunctionManager()
    from ghidra.app.decompiler import DecompInterface
    from ghidra.util.task import ConsoleTaskMonitor
    di = DecompInterface()
    di.openProgram(prog)
    mon = ConsoleTaskMonitor()
    targets = [f for f in fm.getFunctions(True) if sys.argv[2].lower() in f.getName().lower()]
    for t in targets:
        print(f"=== {t.getName()} @ {t.getEntryPoint()}")
        callers = set(f.getEntryPoint().toString() + " " + f.getName()
                      for f in t.getCallingFunctions(mon))
        for c in sorted(callers):
            print("  <- " + c)
        if len(sys.argv) > 3 and sys.argv[3] == "-d":
            for c in t.getCallingFunctions(mon):
                if c.getName().startswith("FUN_"):
                    r = di.decompileFunction(c, 90, mon)
                    print(f"--- decompiled {c.getName()} @ {c.getEntryPoint()}")
                    print(r.getDecompiledFunction().getC())

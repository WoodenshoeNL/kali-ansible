// DumpSymbols.java — debug: list symbols matching a substring arg
import ghidra.app.script.GhidraScript;
import ghidra.program.model.symbol.*;

public class DumpSymbols extends GhidraScript {
    @Override
    public void run() {
        String pat = getScriptArgs().length > 0 ? getScriptArgs()[0] : "strcpy";
        SymbolIterator it = getCurrentProgram().getSymbolTable().getSymbolIterator("*" + pat + "*", true);
        while (it.hasNext()) {
            Symbol s = it.next();
            println(s.getName() + " | type=" + s.getSymbolType() + " | addr=" + s.getAddress() +
                    " | refs=" + s.getReferenceCount());
        }
    }
}

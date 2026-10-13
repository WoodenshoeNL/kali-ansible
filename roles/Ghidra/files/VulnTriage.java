// VulnTriage.java — Ghidra headless postScript for bughunting triage.
// Flags dangerous API usage (with callers), hardcoded credential strings,
// and interesting string constants. Usage:
//   analyzeHeadless <proj> <name> -import <bin> -postScript VulnTriage.java [reportfile]
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.PrintWriter;
import java.util.*;

public class VulnTriage extends GhidraScript {

    static final String[] DANGEROUS = {
        // C runtime
        "strcpy", "strcat", "sprintf", "vsprintf", "gets", "scanf", "sscanf",
        "fscanf", "system", "popen", "execve", "execl", "execvp", "dlopen",
        "memcpy", "strncpy", "strncat", "realpath", "getenv",
        // Windows
        "CreateProcess", "WinExec", "ShellExecute", "ShellExecuteEx",
        "system", "_wsystem", "lstrcpy", "lstrcat", "wsprintf", "wvsprintf",
        "IsBadReadPtr", "IsBadWritePtr", "CharToOem",
        "VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "CreateRemoteThread",
        "LoadLibrary", "LoadLibraryEx", "GetProcAddress",
        "CryptDecrypt", "CryptEncrypt", "WinVerifyTrust", "IsWellKnownCertificate",
        // Deserialization / misc high-value
        "java_runtime_exec_routines", "ObjectInputStream", "Marshal.PtrToStringAnsi"
    };

    static final String[] CRED_RE = {
        "password", "passwd", "passwort", "secret", "token", "apikey", "api_key",
        "credential", "private_key", "privatekey", " BEGIN ", "authorize", "bearer"
    };

    static final String[] CRT_NOISE = {
        "__acrt", "__scrt", "__std", "__crt", "_Crt", "__p__", "_isctype",
        "iswctype", "setSBUpLow", "_setmbcp", "divide", "feholdexcept",
        "fesetenv", "_getmbcp", "__TypeMatch", "_NLG", "__GSHandlerCheck",
        "capture_pre", "capture_previous_context", "__report_gsfailure",
        "__raise_securityfailure"
    };

    static boolean isCrtNoise(String name) {
        for (String pre : CRT_NOISE) if (name.startsWith(pre)) return true;
        return false;
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outPath = args.length > 0 ? args[0] :
            System.getProperty("user.home") + "/ghidra-triage-" +
            getCurrentProgram().getName() + ".txt";
        PrintWriter out = new PrintWriter(outPath, "UTF-8");
        Program p = getCurrentProgram();

        out.println("=== VulnTriage: " + p.getName() + " (" + p.getLanguageID() + ") ===");
        out.println("Image base: " + p.getImageBase());
        out.println();

        // 0. Imported functions (external entry points) — the real attack surface
        //    for PEs; catches COM/RPC imports that no thunk function exists for.
        out.println("--- Imports (external entry points) ---");
        java.util.List<String> imports = new ArrayList<>();
        ghidra.program.model.symbol.ExternalManager em = p.getExternalManager();
        for (String lib : em.getExternalLibraryNames()) {
            ghidra.program.model.symbol.ExternalLocationIterator li = em.getExternalLocations(lib);
            while (li.hasNext()) {
                ghidra.program.model.symbol.ExternalLocation loc = li.next();
                String n = loc.getLabel();
                if (n != null && !imports.contains(n)) imports.add(n);
            }
        }
        Collections.sort(imports);
        int shown = 0;
        for (String n : imports) {
            if (n.startsWith("_") || n.startsWith("__")) continue; // skip CRT detail
            if (shown++ < 120) out.println("  " + n);
        }
        out.println("  (total " + imports.size() + " imports" +
            (shown > 120 ? ", first 120 shown" : "") + ")");
        out.println();

        // 1. Dangerous imports and their callers
        out.println("--- Dangerous API usage ---");
        FunctionManager fm = p.getFunctionManager();
        ReferenceManager rm = p.getReferenceManager();
        Map<String, List<String>> hits = new TreeMap<>();
        Set<String> seen = new HashSet<>();
        FunctionIterator fit = fm.getFunctions(true);
        while (fit.hasNext()) {
            Function f = fit.next();
            if (!seen.add(f.getEntryPoint().toString())) continue;
            String name = f.getName();
            if (f.isThunk()) {
                Function t = f.getThunkedFunction(true);
                if (t != null) name = t.getName();
            }
            String low = name.toLowerCase();
            String matched = null;
            for (String danger : DANGEROUS) {
                if (low.contains(danger.toLowerCase())) { matched = danger; break; }
            }
            if (matched == null) continue;
            for (Function caller : f.getCallingFunctions(getMonitor())) {
                if (isCrtNoise(caller.getName())) continue;
                hits.computeIfAbsent(matched, k -> new ArrayList<>())
                    .add(caller.getName() + "@" + caller.getEntryPoint());
            }
        }
        int total = 0;
        for (Map.Entry<String, List<String>> e : hits.entrySet()) {
            out.println(e.getKey() + "  x" + e.getValue().size());
            Set<String> uniq = new TreeSet<>(e.getValue());
            int n = 0;
            for (String c : uniq) {
                if (n++ >= 15) { out.println("    ... " + (uniq.size()-15) + " more callers"); break; }
                out.println("    <- " + c);
            }
            total += e.getValue().size();
        }
        if (hits.isEmpty()) out.println("(none)");
        out.println();

        // 2. Credential-like strings
        out.println("--- Credential-like strings ---");
        DataIterator di = p.getListing().getDefinedData(true);
        int credCount = 0;
        while (di.hasNext()) {
            Data d = di.next();
            if (!d.hasStringValue()) continue;
            String v = String.valueOf(d.getValue());
            String low = v.toLowerCase();
            for (String re : CRED_RE) {
                if (low.contains(re)) {
                    out.println(d.getAddress() + "  " + v.replace("\n", "\\n").replace("\r", ""));
                    credCount++;
                    break;
                }
            }
        }
        if (credCount == 0) out.println("(none)");
        out.println();

        // 3. Program stats
        out.println("--- Stats ---");
        out.println("Functions: " + fm.getFunctionCount());
        out.println("Dangerous call sites total: " + total);
        out.println("Credential-like strings: " + credCount);

        out.close();
        println("VulnTriage report written: " + outPath);
    }
}

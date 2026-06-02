---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing C Linker Multiple Definition Errors
translated: false
type: note
---

### Build Issues and Fixes for DirB

Your build log shows successful compilation of individual source files (with some warnings), but it fails during the final linking step due to **multiple definition errors** for global variables and structures. This is a common C issue when header files define (rather than just declare) globals. I'll break it down: first the warnings (non-fatal but worth fixing), then the fatal linker errors with a step-by-step fix.

#### 1. Compilation Warnings (Non-Fatal)
These are from GCC's `-Wall` flag. They don't stop the build but indicate potential bugs. Fix them to clean up the output.

- **utils.c**:
  - Line ~4 (in `location_cmp()`): Format specifier mismatch. `strlen()` returns `size_t` (unsigned long), but you're using `%d` (int).
    **Fix**: Change `%d` to `%zu` in the `printf`:
    ```c
    printf("[++++] location_cmp() RESULT: %d (%zu)\n", result, strlen(A) > strlen(B) ? strlen(A) : strlen(B));
    ```
  - Line 287 (in `kbhit()`): Ignoring `read()` return value (it can fail).
    **Fix**: Check the return value:
    ```c
    if (read(0, &key, 1) != 1) {
        // Handle error, e.g., return 0;
    }
    ```

- **resume.c**:
  - Line 32 (in `dump()`): Misleading indentation—`fflush(stdout)` isn't guarded by the `if`.
    **Fix**: Add braces or reindent:
    ```c
    if (options.debuging > 2) {
        printf("[++] dump() Dumping Session State AT %s", asctime(ptr));
        fflush(stdout);
    }
    ```
  - Lines 38–41 and 109–112: Ignoring `asprintf()` return values (it can fail and leave pointers uninitialized).
    **Fix**: Check returns (e.g., `if (asprintf(&dumppath, ...) < 0) { /* error */ }`). Do this for all calls.
  - Line 120 (in `resume()`): Ignoring `fread()` return value (it might not read the full struct).
    **Fix**: Check it:
    ```c
    if (fread(&options, sizeof(struct opciones), 1, desc) != 1) {
        // Handle error, e.g., fclose(desc); return;
    }
    ```

Recompile after fixes: `make clean && make` (assuming a Makefile; if not, rerun your gcc commands).

#### 2. Fatal Linker Errors (Multiple Definitions)
The linker (`/usr/bin/ld`) complains about dozens of symbols (e.g., `options`, `encontradas`, `curl`, etc.) being defined multiple times across object files (`dirb.o`, `crea_wordlist.o`, etc.). All trace back to `/home/lzwjava/projects/dirb/src/variables.h:XX`.

**Root Cause**:
`variables.h` likely **defines** these globals directly (e.g., `struct opciones options;`) instead of **declaring** them as `extern`. When included in multiple `.c` files, each compiles to an `.o` with its own copy of the definitions. Linking merges them, causing conflicts.

**Solution**:
Use the "extern" pattern for shared globals:
- **Declare** in header with `extern` (tells compiler "this exists elsewhere").
- **Define** (without `extern`) in **exactly one** `.c` file (e.g., `dirb.c`).

Steps:
1. **Edit `variables.h`** (in `src/`): Prefix all global variables/structs with `extern`. Examples based on the errors:
   ```c
   // Before (bad: defines in every .o)
   struct opciones options;
   int contador;
   int nec;
   FILE *outfile;
   CURL *curl;
   int errores;
   int existant;
   int descargadas;
   int encontradas;
   char *wordlist_base;
   char *wordlist_current;
   char *wordlist_final;
   char *exts_base;
   char *exts_current;
   int exts_num;
   char *muts_base;
   char *dirlist_base;
   char *dirlist_current;
   char *dirlist_final;
   int listable;
   int resuming;
   char *next_dir;

   // After (good: declares only)
   extern struct opciones options;
   extern int contador;
   extern int nec;
   extern FILE *outfile;
   extern CURL *curl;
   extern int errores;
   extern int existant;
   extern int descargadas;
   extern int encontradas;
   extern char *wordlist_base;
   extern char *wordlist_current;
   extern char *wordlist_final;
   extern char *exts_base;
   extern char *exts_current;
   extern int exts_num;
   extern char *muts_base;
   extern char *dirlist_base;
   extern char *dirlist_current;
   extern char *dirlist_final;
   extern int listable;
   extern int resuming;
   extern char *next_dir;
   ```
   - Include necessary headers at the top: `#include <stdio.h>`, `#include <curl/curl.h>`, etc.
   - If `struct opciones` is defined in the header, keep that (structs can be defined in headers).

2. **Pick one source file** (e.g., `dirb.c`, the main file) and **define** the globals there (no `extern`):
   ```c
   // In dirb.c, after includes
   struct opciones options = {0};  // Initialize if needed
   int contador = 0;
   int nec = 0;
   FILE *outfile = NULL;
   CURL *curl = NULL;
   // ... repeat for all others, initializing sensibly (e.g., ints to 0, pointers to NULL)
   ```

3. **Clean and rebuild**:
   ```
   make clean  # Or rm *.o
   # Rerun your compile commands, then the final link:
   gcc -Wall -g -O2 -o dirb crea_wordlist.o dirb.o get_url.o lanza_ataque.o calculanec.o utils.o options.o resume.o -lcurl
   ```

4. **Verify**:
   - Run `./dirb --help` to test.
   - If new errors appear (e.g., undefined symbols), ensure the definitions are in `dirb.c` and all files include `variables.h`.

#### Additional Notes
- **Makefile?** If this is from a `Makefile`, add `-Werror` temporarily to treat warnings as errors during dev.
- **DirB Version**: This looks like an older/custom fork (references to `lanza_ataque.c`, etc.). If it's from GitHub, check for upstream fixes: [dirb on GitHub](https://github.com/v0re/dirb).
- **Dependencies**: Ensure libcurl is installed (`sudo apt install libcurl4-openssl-dev` on Debian-based systems).
- If issues persist (e.g., missing `struct opciones` def), share `variables.h` contents for more help.

This should get it linking cleanly! If you paste more code/logs, I can refine.

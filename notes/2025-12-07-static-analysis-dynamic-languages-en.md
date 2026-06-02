---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Static Analysis for Dynamic Languages
translated: false
type: note
---

Question: What does the PDF "pysonar-slides.pdf" say?

Answer:

The PDF "pysonar-slides.pdf" appears to be a presentation slide deck titled "Static Analysis of Dynamically Typed Languages made Easy" by Yin Wang from the School of Informatics and Computing at Indiana University. It discusses challenges and solutions for performing static analysis on dynamically typed languages like Python, based on the author's internships at Google in 2009 and 2010. The work was motivated by Google's Grok Project, which aimed to statically analyze all code at Google (including C++, Java, JavaScript, Python, Sawzall, and Protobuf). The initial goal was to enable IDE-like code browsing, but it proved difficult for Python, leading to more advanced semantic analysis.

### Key Sections and Content

#### Overview (Pages 1-2)

- Describes the internships and motivation.
- Highlights the Grok Project's scope.
- Notes that while the goal started simple (code browsing), Python's dynamic nature made it challenging.

#### Achieved Goals (Page 3)

- Built high-accuracy semantic indexes.
- Detected and reported semantic bugs, such as:
  - Type errors.
  - Missing return statements.
  - Unreachable code.
  - And others.

#### Problems Faced by Static Analysis (Pages 5-23)

The presentation outlines four main problems with solutions:

1. **Problems with Dynamic Typing (Pages 6-9)**:
   - Dynamic typing complicates name resolution, especially in polymorphic functions (e.g., `def h(x): return x.z` – where is `z` defined? It depends on `x`'s type).
   - Solution: Use a static type system with inter-procedural analysis to infer types.

   **Static Type System for Python (Page 10)**:
   - Mostly standard, with extras like union and dict types.
   - Includes:
     - Primitives: int, str, float, bool.
     - Tuples: (int, float), (A, B, C).
     - Lists: [int], [bool], [(int, bool)].
     - Dicts: {int => str}, {A => B}.
     - Classes: ClassA, ClassB.
     - Unions: {int | str}, {A | B | C}.
     - Recursive: #1(int, +), #2(int -> 2).
     - Functions: int -> bool, A -> B.

2. **Problems with Control-Flow Graph (CFG) (Pages 11-13)**:
   - CFGs are hard to build for higher-order programs (e.g., functions passed as arguments like `def g(f, x): return f(x)`).
   - References prior work (Shivers 1988/1991, Might & Shivers 2006/2007, Vardoulakis & Shivers 2010/2011) on complications from CPS (Continuation-Passing Style) and CFG construction.
   - Solution: Avoid CPS and CFG entirely; use a direct-style, recursive abstract interpreter.

3. **Problems with Dynamic Field Creation/Deletion (Pages 14-21)**:
   - Example: `class A: x = 1; obj = A(); obj.y = 3; print obj.x, obj.y`.
   - Solution: Create "abstract objects" at constructor calls and modify them when fields are added/deleted. Classes remain unaffected.

4. **Problems with More Powerful Dynamic Features (Pages 22-23)**:
   - Includes operations on `__dict__` (e.g., setattr, delattr), dynamic reparenting, import hacks, eval, etc.
   - Solution: Enforce a "Python Style Guide" to restrict such features.

Pages 4 and 24-28 appear blank or transitional.

#### Actual Code of Main Interpreter (Pages 29-33)

- Provides Python code snippets for the type inferencer (`infer` function).
- Handles modules, names, lambdas, calls, etc.
- Uses environment (`env`) and stack (`stk`) for recursion detection.
- Looks up types, records info/errors, creates closures, and invokes functions.

Pages 34-39 appear blank or transitional.

#### Recursion Detection (Pages 40-54)

- Uses factorial example (`def fact(n): ...`) to illustrate.
- Assumption: Same call site with same argument types yields same output type (or nontermination).
- Detects loops by checking if a `<call site, arg type>` pair is already on the stack.
- Returns "unknown type" on loop detection, then unifies with known types (may cause false negatives).
- Ultimately infers types like `fact :: int -> int`.

#### Correctness of Recursion Detection (Pages 55-58)

- Views programs as dynamic circuits.
- Call sites are "conjunction points" with deterministic futures.
- If a `<call site, arg type>` repeats on the path, it's a loop.

#### Related Work (Page 59)

- Similar to control-flow analyses (CFAs) but simpler (no explicit CFG or stack management).
- "CFG" is implicit and dynamic.
- Doesn't annotate AST; leverages host language recursion.
- Simpler than Google's JSCompiler (which needs annotations).
- Akin to Near Concrete Interpretation (NCI), but different recursion detection.

#### Connections to Deeper Theories (Page 60)

- Essentially a simple supercompilation.
- Similar to ACL2 theorem prover techniques.
- Tracks only type info; efficient termination (no homeomorphic embedding), but may be less accurate (false negatives).

#### Limitations (Page 61)

- Requires all source code (no bytecode processing; built-ins mocked).
- No value/range tracking for numbers.
- Ignores heap side-effects on typing.
- Possible false negatives in recursions.
- High worst-case complexity (approximations could help, but reduce accuracy).
- Unfriendly error reports for deep bugs.

#### Applicability (Page 62)

- General method for type inference/static analysis.
- Applicable to any language, but most useful for dynamic ones (static languages are easier/modular with annotations).
- Involves trade-offs.

#### Availability (Page 63)

- 2009: "Jython Indexer" (Java, open-source; modular unification like HM; fast but limited; used at Google; contributed to Jython).
- 2010: "PySonar" (Java, not open-source; inter-procedural; resolves most names; detects deep bugs; slow).
- 2011: "mini-pysonar" (Python, open-source on GitHub; essential parts only).

#### Possible Future Work (Page 64)

- Apply to other (simpler) languages.
- Publish a paper on the method.
- Derive related ideas.

Page 65 appears blank.

The slides include code examples, diagrams (e.g., speech bubbles for questions), and references to academic papers. There's a "Demo Time" slide (Page 4), likely for a live demonstration. Overall, it presents a practical approach to making static analysis feasible for Python by addressing dynamic typing challenges through type inference, abstract interpretation, and recursion handling.

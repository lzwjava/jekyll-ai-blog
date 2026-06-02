# CLAUDE.md — Global Coding Principles

## Code Quality
- Repeatedly refine code — great code is rewritten, not written once
- Delete more than you keep; insights come over time

## Code Structure
- Use box-like nesting and tree-like branching
- Every `if` should have an `else` — handle all cases explicitly

## Functions
- Keep functions under ~40 lines (one screen)
- Each function does one thing only
- Use small helper functions freely, even 2-liners
- Pass data via parameters/return values — avoid globals and class members for data passing

## Readability
- Code should be self-explanatory; minimal comments needed
- Use meaningful names for functions and variables
- Keep local variables short and close to their usage
- Don't reuse local variables — declare new ones for new values
- Extract complex logic/expressions into named helpers or intermediate variables

## Simplicity
- Avoid `i++`/`i--` outside simple `for` headers — use explicit two-step ops
- Always use `{}` for `if` bodies, even single-line
- Use parentheses to clarify operator precedence
- Avoid `continue`/`break` in loops — restructure or extract to functions
- Don't abuse `&&`/`||` as control flow — write explicit `if/else`

## Error Handling
- Never ignore return values
- Catch specific exceptions, not broad `Exception`
- Keep `try` blocks small — one call per try/catch when possible
- Handle errors at the point they occur

## Null Safety
- Prefer exceptions over returning null
- Never put null into collections
- Check null immediately at the point of receipt
- Use `Objects.requireNonNull()` to reject null inputs early
- Use `Optional` atomically (check + unwrap together)

## Testing
- Write tests **after** the program and algorithm are stable
- Test essential properties only — not implementation details
- Each test covers one aspect only
- Avoid multi-layer mocks
- Avoid string comparison in tests — use structured comparison
- Don't modify clean code just to satisfy test coverage
- Manual testing has value — don't neglect it

## Anti-Patterns to Avoid
- Over-engineering for imaginary future requirements
- Obsessing over code reuse before code works
- Test-driven development as dogma
- Excessive test scaffolding that complicates simple code

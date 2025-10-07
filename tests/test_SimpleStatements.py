# Simple statements test: assignments, calls, return/pass/break/continue

# --- Assignments (simple and augmented) ---
x = 1
y = 3.14
name = "Fangless"
escaped = "He said \"hi\""
multiline = "Line 1\nLine 2"
truth = True
falsity = False
grouped_num = (42)
alias_name = (name)

# --- Semicolon-separated assignments (lexer splits ';' into logical NEWLINE) ---
a = 10; b = 20; c += 3
u = (x); v = (y); w = (truth)
count += 1; total -= 2; prod *= 8; quot /= 4; ratio //= 2; mod %= 5; power **= 3

# --- Function calls as statements ---
print(x, y, 42)
foo()
bar(1, (2), True, "ok")

# --- Function calls on RHS of assignment ---
sum_result = sum(1, 2, 3)
nested = outer(inner(1, 2), 3)

# --- Control-flow simple statements ---
pass
break
continue

# --- Return statements (with and without value) ---
return
return alias_name

# --- Mixed simple statements in one physical line (lexer turns ';' into NEWLINE) ---
pass; continue; break; foo(1); bar()

# --- Last line without trailing newline (intentional) ---
end_call = func(a, b)
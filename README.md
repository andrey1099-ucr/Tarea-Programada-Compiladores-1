# Programmed Task — Compilers 1

This project implements the **lexical analyzer (lexer)** for a simplified subset of Python called **“Fangless Python.”** The goal is to transform source code into a stream of tokens using the **PLY (Python Lex-Yacc)** library, including indentation handling (INDENT/DENT), skipping single-line comments, validating basic string escape sequences, and robustly reporting lexical errors without crashing.

## 1. Create virtual environment

```bash
py -m venv venv
```

## 2. Activate virtual environment

```bash
venv\Scripts\activate
```

You should see the environment name (venv) at the beginning of the command prompt.

## 3. Install required libraries

Inside the active environment:

```bash
pip install -r requirements.txt
```

## Deactivate virtual environment

When you finish working:

```bash
deactivate
```

## Best practices

Generate an updated requirements.txt after installing new libraries:

```bash
pip freeze > requirements.txt
```

## Useful commands

### View packages installed in the environment

```bash
pip list
```

### Check Python and pip versions

```bash
python --version
pip --version
```

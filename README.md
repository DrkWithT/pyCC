# pyCC (fork)
A basic C compiler written in Python. Will support a teeny tiny part of C89.

## Usage:
```sh
python3 ./pyCC/pyCC.py -S file.c
```

## TODO:
- [x] Test and fix parser!
- [ ] Create IR generator by the ASTVisitor!
- [ ] Create ASM generator to convert from IR.
- [ ] Compare ASM output with GCC -std=c89?

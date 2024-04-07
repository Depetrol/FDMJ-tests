import random

grammar = """
Prog -> MainMethod \\n ClassDeclList
~
MainMethod -> public int main ( ) { \\n VarDeclList StmList \\n }
~
VarDeclList -> ε | VarDecl \\n VarDeclList
~
VarDecl -> class id id ; | int id ; | int id = Const ; | int [ ] id ; | int [ ] id = { ConstList } ; | float id ; | float id = Const ; | float [ ] id ; | float [ ] id = { ConstList } ;
~
Const -> NUM | - NUM
~
ConstList -> ε | Const ConstRest
~
ConstRest -> ε | , Const ConstRest
~
StmList -> ε | Stm \\n StmList
~
Stm -> { StmList } | if ( Exp ) \\n Stm \\n else \\n Stm | if ( Exp ) \\n Stm | while ( Exp ) \\n Stm | while ( Exp ) \\n ; | Exp = Exp ;  | Exp [ ] = { ExpList } ;  | Exp . id ( ExpList ) ;  | continue ; | break ;  | return Exp ;  | putnum ( Exp ) ; | putch ( Exp ) ; | putarray ( Exp , Exp ) ; | starttime ( ) ; | stoptime ( ) ;
~
Exp -> NUM | true | false | length ( Exp ) | getnum ( ) | getch ( ) | getarray ( Exp ) | id | this | new int [ Exp ] | new float [ Exp ] | new id ( ) | Exp op Exp | ! Exp | - Exp | ( Exp ) | ( { StmList } Exp ) | Exp . id | Exp . id ( ExpList ) | Exp [ Exp ]
~
ExpList -> ε | Exp ExpRest
~
ExpRest -> ε | , Exp ExpRest
~
ClassDeclList -> ε | ClassDecl \\n ClassDeclList
~
ClassDecl -> public class id { \\n VarDeclList MethodDeclList \\n } | public class id extends id { \\n VarDeclList MethodDeclList \\n } \\n
~
MethodDeclList -> ε | MethodDecl \\n MethodDeclList
~
MethodDecl -> public Type id ( FormalList ) { \\n VarDeclList StmList \\n }
~
Type -> class id | int | int [ ] | float | float [ ]
~
FormalList -> ε | Type id FormalRest
~
FormalRest -> ε | , Type id FormalRest
"""

EMPTY_RATE = 0.02
EMPTY_RATE_INC = 0.02
ID_MAX_LENGTH = 10
NUM_MAX = 114514


def create_grammar(grammar_str: str, split: str = "->", line_split: str = "~") -> dict:
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip():
            continue
        else:
            exp, stms = line.split(split)
            grammar[exp.strip()] = [s.split() for s in stms.split("|")]
    return grammar


def gen_terminal_exp(exp: str) -> str:
    def _gen_id() -> str:
        first_char: str = random.choice(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        )
        rest_chars: str = "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_",
                k=random.randint(0, ID_MAX_LENGTH),
            )
        )
        return first_char + rest_chars

    def _gen_num() -> str:
        return str(random.randint(0, NUM_MAX))

    def _gen_op() -> str:
        return random.choice(
            ["+", "-", "*", "/", "||", "&&", "<", "<=", ">", ">=", "==", "!="]
        )

    if exp == "id":
        return _gen_id()
    elif exp == "NUM":
        return _gen_num()
    elif exp == "op":
        return _gen_op()
    elif exp == "ε":
        return ""
    else:
        return exp


def generate(gram: list, target: str, erate: float) -> str:
    if target not in gram:  # terminal expression
        return gen_terminal_exp(target)
    else:  # non-terminal expression
        expaned: list = []
        pattern = random.choice(gram[target])
        finished = False
        while not finished:
            r = random.random()
            if pattern == ["ε"]:
                if r < erate:
                    finished = True
                else:
                    pattern = random.choice(gram[target])
            else:
                finished = True
                for t in pattern:
                    expaned.append(generate(gram, t, erate + EMPTY_RATE_INC))
        # expaned = [generate(gram, t, erate + EMPTY_RATE_INC) for t in random.choice(gram[target])]
        codes: str = " ".join([(e) if e != "\\n" else "\n" for e in expaned])
        return codes if target != "Exp" else f"({codes})"


def main() -> None:
    _grammar = create_grammar(grammar)
    _target = "Prog"

    # print(int((1 - EMPTY_RATE) / EMPTY_RATE))
    # print(_grammar[_target])
    with open("random.fmj", "w") as f:
        f.write(generate(_grammar, _target, EMPTY_RATE))


if __name__ == "__main__":
    main()

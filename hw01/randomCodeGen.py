import random
import os

TEST_TIMES = 10
NUM_MAX = 114514
ID_MAX_LENGTH = 10
ID_RATE = 0.4
EXPR_RECURSION_LIMIT = 3
PROG_LENGTH_MIN = 50
PROG_LENGTH_MAX = 70

table: map = {}
outputs: list = []

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_id(alloc: bool = False) -> (str, int):
    if alloc:
        length: int = random.randint(1, ID_MAX_LENGTH)
        first_char = random.choice(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        rest_chars = "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_",
                k=length - 1,
            )
        )
        table[first_char + rest_chars] = None
        return first_char + rest_chars, None
    else:
        while True:
            id = random.choice(list(table))
            if table[id] is not None:
                return id, table[id]


def generate_int_const() -> (str, int):
    num = random.randint(0, NUM_MAX)
    return str(num), num


def generate_expression(depth: int) -> (str, int):
    if depth == 1:
        return generate_id() if random.random() < ID_RATE else generate_int_const()
    else:
        options = [
            "Exp op Exp",
            "id",
            "'-'Exp",
            "INT_CONST",
            "Exp",
            "'(''{'Statement*'}' Exp')'",
        ]
        choice = random.choice(options)
        if choice == "Exp op Exp":
            lexp, lval = generate_expression(depth - 1)
            rexp, rval = generate_expression(depth - 1)
            op = random.choice("+-*/")
            while op == "/" and rval == 0:
                rexp, rval = generate_expression(depth - 1)
            ret: int = int(eval(f"{lval} {op} {rval}"))
            return f"({lexp}) {op} ({rexp})", ret
        elif choice == "id":
            id, val = generate_id()
            return id, val
        elif choice == "'-'Exp":
            exp, val = generate_expression(depth - 1)
            return f"-({exp})", -val
        elif choice == "INT_CONST":
            s, val = generate_int_const()
            return s, val
        elif choice == "Exp":
            exp, val = generate_expression(depth - 1)
            return exp, val
        elif choice == "'(''{'Statement*'}' Exp')'":
            statements = generate_statements(depth - 1, False)
            exp, val = generate_expression(depth - 1)
            return f"({{ {statements} }} {exp})", val
        else:
            raise ValueError("Invalid choice, choice = " + choice)


def generate_statement(new_line: bool = True) -> str:
    options = ["id = Exp;", "putint(Exp);"]
    choice = random.choice(options)
    if choice == "id = Exp;":
        id, _ = generate_id(True)
        exp, val = generate_expression(random.randint(1, EXPR_RECURSION_LIMIT))
        table[id] = val
        return choice.replace("id", id).replace("Exp", exp) + ("\n" if new_line else "")
    else:
        exp, val = generate_expression(random.randint(1, EXPR_RECURSION_LIMIT))
        outputs.append(val)
        return choice.replace("Exp", exp) + ("\n" if new_line else "")


def generate_statements(num_statements, new_line=True) -> str:
    return "".join([generate_statement(new_line) for _ in range(num_statements)])


def generate_main_method() -> str:
    a_init = random.randint(1, NUM_MAX)
    table["a"] = a_init
    return f"""public int main() {{
a = {a_init};
{generate_statements(random.randint(PROG_LENGTH_MIN, PROG_LENGTH_MAX))}}}"""


def generate_program() -> str:
    return generate_main_method()


if __name__ == "__main__":
    for i in range(TEST_TIMES):
        table.clear()
        outputs.clear()
        gen = generate_program()
        with open("gen_program_" + str(i) + ".fdmj", "w") as f:
            f.write(gen)
        with open("gen_program_" + str(i) + ".correct", "w") as f:
            for o in outputs:
                f.write(str(o) + "\n")

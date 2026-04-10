import os

# -------- TOKENISE --------
def get_tokens(expression):
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isdigit() or ch == '.':
            number = ch
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                number += expression[i]
                i += 1
            tokens.append(("NUM", float(number)))
            continue

        elif ch in "+-*/":
            tokens.append(("OP", ch))

        elif ch == "(":
            tokens.append(("LPAREN", ch))

        elif ch == ")":
            tokens.append(("RPAREN", ch))

        elif ch == " ":
            pass

        else:
            raise ValueError("Invalid character in expression")

        i += 1

    tokens.append(("END", ""))
    return tokens


# -------- PARSER --------
def build_tree(tokens):
    index = 0

    def parse_expression():
        nonlocal index
        node = parse_term()

        while tokens[index][1] in ("+", "-"):
            op = tokens[index][1]
            index += 1
            right = parse_term()
            node = (op, node, right)

        return node

    def parse_term():
        nonlocal index
        node = parse_factor()

        while tokens[index][1] in ("*", "/"):
            op = tokens[index][1]
            index += 1
            right = parse_factor()
            node = (op, node, right)

        return node

    def parse_factor():
        nonlocal index
        tok_type, tok_val = tokens[index]

        # unary negation
        if tok_type == "OP" and tok_val == "-":
            index += 1
            return ("neg", parse_factor())

        if tok_type == "NUM":
            index += 1
            return tok_val

        if tok_type == "LPAREN":
            index += 1
            node = parse_expression()
            if tokens[index][0] != "RPAREN":
                raise ValueError("Missing closing bracket")
            index += 1
            return node

        raise ValueError("Invalid syntax")

    return parse_expression()


# -------- TREE STRING --------
def format_tree(node):
    if isinstance(node, float):
        return str(int(node)) if node.is_integer() else str(node)

    if node[0] == "neg":
        return f"(neg {format_tree(node[1])})"

    op, left, right = node
    return f"({op} {format_tree(left)} {format_tree(right)})"


# -------- EVALUATE --------
def solve(node):
    if isinstance(node, float):
        return node

    if node[0] == "neg":
        return -solve(node[1])

    op, left, right = node

    if op == "+":
        return solve(left) + solve(right)
    elif op == "-":
        return solve(left) - solve(right)
    elif op == "*":
        return solve(left) * solve(right)
    elif op == "/":
        return solve(left) / solve(right)


# -------- TOKENS STRING --------
def format_tokens(tokens):
    parts = []
    for t in tokens:
        if t[0] == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{t[0]}:{t[1]}]")
    return " ".join(parts)


# -------- MAIN FUNCTION --------
def evaluate_file(input_path: str):
    results = []
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(input_path, "r") as file, open(output_path, "w") as out:
        for line in file:
            expr = line.strip()
            if not expr:
                continue

            try:
                tokens = get_tokens(expr)
                tree = build_tree(tokens)
                value = solve(tree)

                tree_str = format_tree(tree)
                token_str = format_tokens(tokens)

                if value.is_integer():
                    result_str = str(int(value))
                else:
                    result_str = f"{value:.4f}"

            except:
                tree_str = "ERROR"
                token_str = "ERROR"
                result_str = "ERROR"
                value = "ERROR"

            out.write(f"Input: {expr}\n")
            out.write(f"Tree: {tree_str}\n")
            out.write(f"Tokens: {token_str}\n")
            out.write(f"Result: {result_str}\n\n")

            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": token_str,
                "result": value
            })

    return results
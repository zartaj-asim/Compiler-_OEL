import re

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('NUMBER', self.number())

            if self.current_char == '+':
                self.advance()
                return Token('ADDOP', '+')

            if self.current_char == '-':
                self.advance()
                return Token('ADDOP', '-')

            if self.current_char == '*':
                self.advance()
                return Token('MULOP', '*')

            if self.current_char == '/':
                self.advance()
                return Token('MULOP', '/')

            if self.current_char == '^':
                self.advance()
                return Token('EXPOP', '^')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            self.error()

        return Token('EOF')

def tokenize(input_string):
    lexer = Lexer(input_string)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == 'EOF':
            break
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[0]
        self.pos = 0

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = Token('EOF')
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expression()
            self.eat('RPAREN')
            return result

    def term(self):
        result = self.factor()
        while self.current_token.type in ('MULOP', 'EXPOP', 'DIVOP'):
            token = self.current_token
            if token.type == 'MULOP':
                self.eat('MULOP')
                result = {'*': [result, self.factor()]}
            elif token.type == 'DIVOP':
                self.eat('DIVOP')
                result = {'/': [result, self.factor()]}
            elif token.type == 'EXPOP':
                self.eat('EXPOP')
                result = {'^': [result, self.factor()]}
        return result

    def expression(self):
        result = self.term()
        while self.current_token.type in ('ADDOP', 'SUBOP'):
            token = self.current_token
            if token.type == 'ADDOP':
                self.eat('ADDOP')
                result = {'+': [result, self.term()]}
            elif token.type == 'SUBOP':
                self.eat('SUBOP')
                result = {'-': [result, self.term()]}
        return result

def parse_input(input_string):
    tokens = tokenize(input_string)
    parser = Parser(tokens)
    return parser.expression()

def display_tokenization(tokens):
    print("Tokenization:")
    for token in tokens:
        print(token.type, token.value)

def display_parse_tree(parse_tree):
    if isinstance(parse_tree, dict):
        operator = next(iter(parse_tree))
        left, right = parse_tree[operator]
        print("(")
        display_parse_tree(left)
        print(operator)
        display_parse_tree(right)
        print(")")
    else:
        print(parse_tree)

def get_arithmetic_expression_from_user():
    return input("Enter an arithmetic expression: ")


def main():
    expression = get_arithmetic_expression_from_user()
    tokens = tokenize(expression)
    display_tokenization(tokens)
    parse_tree = parse_input(expression)
    print("Parse Tree:")
    display_parse_tree(parse_tree)
    print("Result:", parse_tree)  


if __name__ == "__main__":
    main()

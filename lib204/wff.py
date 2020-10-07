

def symbol(cls, mode='jape'):
    return {'jape':jape_symbol, 'html': html_symbol, 'python': python_symbol}[mode][cls]


class WFF(object):
    def __and__(self, other):
        return And(self, other)
    def __or__(self, other):
        return Or(self, other)
    def __invert__(self):
        return Not(self)
    def __rshift__(self, other):
        return Implies(self, other)
    def __str__(self):
        return self.dump('jape')
    def __repr__(self):
        return str(self)
    def __eq__(self, o):
        return str(self) == str(o)
    def __hash__(self):
        return hash(str(self))
    def size(self, scoring):
        score = sum([c.size(scoring) for c in self.children])
        return score + scoring[type(self)]


class Variable(WFF):

    def __init__(self, name):
        self.name = name

    def dump(self, _):
        return self.name

    def vars(self):
        return set([self])

    @property
    def children(self):
        return []

class Not(WFF):

    def __init__(self, child):
        self.child = child

    def dump(self, mode):
        return symbol(Not, mode) + self.child.dump(mode)

    def vars(self):
        return self.child.vars()

    @property
    def children(self):
        return [self.child]

class PairFormula(WFF):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def dump(self, mode):
        return "(%s%s%s)" % (self.left.dump(mode), symbol(type(self), mode), self.right.dump(mode))

    def vars(self):
        return self.left.vars() | self.right.vars()

    @property
    def children(self):
        return [self.left, self.right]


class CommutativePairFormula(PairFormula):
    ...

class Implies(PairFormula):
    ...

class Proves(PairFormula):
    def dump(self, mode):
        left = self.left.dump(mode)
        right = self.right.dump(mode)
        if (not isinstance(self.left, Comma)) and left[0] == '(':
            assert left[-1] == ')'
            left = left[1:-1]
        if right[0] == '(':
            assert right[-1] == ')'
            right = right[1:-1]

        return left + symbol(type(self), mode) + right

class Entails(PairFormula):
    ...

class And(CommutativePairFormula):
    ...

class Or(CommutativePairFormula):
    ...

class Comma(object):

    def __init__(self, *children):
        self.children = list(children)

    def dump(self, mode):
        children = [child.dump(mode) for child in self.children]
        def remove_outer_brackets(c):
            if c[0] == '(':
                assert c[-1] == ')'
                return c[1:-1]
            else:
                return c
        return symbol(type(self), mode).join(map(remove_outer_brackets, children))

    def vars(self):
        vars = set()
        for c in self.children:
            vars |= c.vars()
        return vars


jape_symbol = {
    And: '∧',
    Or: '∨',
    Not: '¬',
    Implies: '→',
    Comma: ',',
    Proves: ' ⊢ ',
    Entails: ' ⊨ ',
    # Forall: '∀',
    # Exists: '∃'
}

html_symbol = {
    And: '&and;',
    Or: '&or;',
    Not: '&not;',
    Implies: '&#8594;',
    Comma: '&#44;',
    Proves: ' &#8866; ',
    Entails: ' ⊨ ',
    # Forall: '∀',
    # Exists: '∃'
}

python_symbol = {
    And: '&',
    Or: '|',
    Not: '~',
    Implies: '>>',
    Comma: None,
    Proves: None,
    Entails: None,
    # Forall: '∀',
    # Exists: '∃'
}

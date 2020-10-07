
from lib204 import wff


class Encoding(object):
    def __init__(self):
        self.names = set()
        self.aux = []
        self.constraints = []
        self.building_theory = True

    def tseitin(self, T, name):

        scoring = {
            wff.Variable: 0,
            wff.Not: 1,
            wff.Or: 1,
            wff.And: 1,
            wff.Implies: 1
        }

        assert name not in self.names, "Error: Trying to create a duplicate auxiliary variable %s" % str(name)
        assert T.size(scoring) == 1, "An auxillary variable definition should only use a single operator. %s has %d" % (str(T), T.size(scoring))
        self.names.add(name)

        assert self.building_theory, "Error: You already finalized the theory, and cannot add further Tseitin variables."

        aux = wff.Variable(name)
        self.aux.append(aux)
        self.constraints.append(aux >> T)
        self.constraints.append(T >> aux)
        return aux

    def finalize(self, var):
        assert var.name in self.names, "Error: Finalizing with a variable that wasn't added: %s" % str(var.name)
        self.constraints.append(var)
        self.building_theory = False

    def dump(self, mode='jape'):
        return "\nConstraints:\n - %s\n" % '\n - '.join(map(lambda x: x.dump(mode), self.constraints))

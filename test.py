
from lib204 import wff, semantic_interface

try:
    from run import *
except:
    from .run import *

def test_submission():

    # Q1
    assert isinstance(q1b, list), "q1b must be a list of lists that correspond to equivalent theories"
    theories = []
    for lst in q1b:
        assert isinstance(lst, list), "q1b must be a list of lists that correspond to equivalent theories"
        theories.extend(lst)
        for s in lst:
            assert isinstance(s, wff.WFF), "q1b must be a list of lists that correspond to equivalent theories"
    assert 4 == len(theories), "q1b should contain each of s1,s2,s3,s4 only once"
    for t in [s1,s2,s3,s4]:
        assert t in theories, "q1b should contain each of s1,s2,s3,s4 only once"

    vars = (s1 & s2 & s3 & s4).vars()
    assert isinstance(q1c, dict), "q1c should be a dict mapping Variables to True/False"
    for v in vars:
        assert v in q1c, "q1c is missing a setting for variable %s" % str(v)
        assert isinstance(q1c[v], bool), "q1c should be a dict mapping Variables to True/False"


    # Q2
    def test_steps(steps, starting, stepsname, startingname):
        assert steps[0][0] == starting, "First step of %s should be the same as %s" % (stepsname, startingname)
        for s in steps:
            assert isinstance(s[0], wff.WFF), "Each step should be a well formed formula. Violating step of %s: %s" % (stepsname, str(s))
            assert isinstance(s[1], str), "Each step should have a string explanation for it. Violating step of %s: %s" % (stepsname, str(s))
    test_steps(s5nnf, s5, 's5nnf', 's5')
    test_steps(s6nnf, s6, 's6nnf', 's6')
    test_steps(s5cnf, s5, 's5cnf', 's5')
    test_steps(s6cnf, s6, 's6cnf', 's6')

    assert isinstance(s5tseitin, semantic_interface.Encoding), "s5tseitin should be a semantic_interface.Encoding object"
    assert isinstance(s6tseitin, semantic_interface.Encoding), "s6tseitin should be a semantic_interface.Encoding object"


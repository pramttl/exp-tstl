import sut

t = sut.t()

from pprint import pprint

def print_enabled():
    print
    print '===== enabled ====='
    print
    for act_obj in t.enabled():
        print act_obj[0]
    print '-------------------'


def print_all():
    print
    print '====all_actions===='
    print
    for act_obj in t.actions():
        print act_obj[0]
    print '-------------------'

print_all()
print_enabled()

print "Running t.enabled()[0][2]()"
t.enabled()[0][2]()

print_enabled()

t.enabled()[0][2]()

print_enabled()
g = t.p_GAME[0]

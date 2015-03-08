import sut

t = sut.t()

from pprint import pprint

def penabled():
    """
    Print all enabled actions
    """
    print
    print '===== enabled ====='
    print
    for ctr, act_obj in enumerate(t.enabled()):
        print "%s: %s"%(ctr, act_obj[0])
    print '-------------------'


def pall():
    """
    Print all actions
    """
    print
    print '====all_actions===='
    print
    for ctr,act_obj in enumerate(t.actions()):
        print "%s: %s"%(ctr, act_obj[0])
    print '-------------------'

def takeact(index, enabled=True):
    """
    Take an enabled action via index.
    """
    if enabled:
        print "Running:\n%s"%(t.enabled()[index][0],)
        t.enabled()[index][2]()
    else:
        print "Running:\n%s"%(t.actions()[index][0],)
        t.actions()[index][2]()

pall()
penabled()

takeact(0)
takeact(0)
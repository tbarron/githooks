import docopt
import pdb
import pexpect
import pytest

import githooks
from githooks import ghlib
from githooks import version

@pytest.mark.parametrize("a,b", [('list', 'install'),
                                 ('list', 'show'),
                                 ('list', 'remove'),
                                 ('show', 'list'),
                                 ('show', 'install'),
                                 ('show', 'remove')])
def test_gh_docopt(a, b):
    # pdb.set_trace()
    with pytest.raises(docopt.DocoptExit) as e:
        z = docopt.docopt(githooks.__doc__, [a, b])
    assert 'DocoptExit: Usage:' in str(e)


def template(**kw):
    rv = {'--debug': False,
          '--help': False,
          '--version': False,
          '-d': False,
          '-g': False,
          '<hookname>': None,
          'install': False,
          'list': False,
          'remove': False,
          'show': False}
    for k in kw:
        rv[k] = kw[k]
    return rv


def test_gh_docopt_list(capsys):
    exp = template(list=True)
    z = docopt.docopt(githooks.__doc__, ['list'])
    assert z == exp
#     for k in z:
#         assert z[k] == (k == 'list')


@pytest.mark.parametrize(('argl', 'adj'),
                         [(['list'],
                           {'list': True}),
                          (['--version'],
                           {'--version': True}),
                          (['install', 'brodie'],
                           {'install': True,
                            '<hookname>': 'brodie'}),
                          (['install', '-g', 'brodie'],
                           {'install': True,
                            '-g': True,
                            '<hookname>': 'brodie'}),
                          ])
def test_gh_docopt_good(argl, adj):
    exp = template(**adj)
    z = docopt.docopt(githooks.__doc__, argl)
    assert z == exp

@pytest.mark.parametrize(('argl'),
                         [['list', 'install'],
                          ['--ack'],
                          ['install', 'brodie', 'show'],
                          ['show', 'list'],
                          ['--unknown'],
                          ])
def test_gh_docopt_bad(argl):
    with pytest.raises(docopt.DocoptExit) as e:
        z = docopt.docopt(githooks.__doc__, argl)
    assert 'DocoptExit: Usage:' in str(e)
        

def test_gh_docopt_version():
    exp = template()
    exp['--version'] = True
    z = docopt.docopt(githooks.__doc__, ['--version'])
    assert z == exp
    

# -----------------------------------------------------------------------------
def test_pydoc_gh():
    """
    Ensure 'pydoc gh' produces something reasonable
    """
    r = ghlib.catch_stdout('pydoc githooks')
    assert 'git hook manage' in r
    assert 'gh list' in r


# -----------------------------------------------------------------------------
# def test_gh_list():
#     """
#     Test for 'gh list'
#     """
#     r = ghlib.catch_stdout('gh list')


def test_gh_version():
    z = pexpect.run("gh --version")
    assert version.__version__ in z

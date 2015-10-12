import docopt
import pdb
import pexpect
import pytest

import githooks
from githooks import ghlib
from githooks import version

# -----------------------------------------------------------------------------
def test_hookdict():
    """Test hookdict(): returns a dict of available hook functions
    """
    hd = githooks.hookdict()
    for k in hooklist():
        assert k in hd
        assert hd[k]


# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
def template(**kw):
    rv = {'--debug': False,
          '--help': False,
          '--version': False,
          '-d': False,
          '-g': False,
          '<hookname>': None,
          '<filename>': None,
          'freeze': False,
          'install': False,
          'list': False,
          'remove': False,
          'show': False}
    for k in kw:
        rv[k] = kw[k]
    return rv


# -----------------------------------------------------------------------------
def test_gh_docopt_list(capsys):
    pytest.dbgfunc()
    exp = template(list=True)
    z = docopt.docopt(githooks.__doc__, ['list'])
    assert z == exp
#     for k in z:
#         assert z[k] == (k == 'list')


# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
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
def test_gh_list():
    """Test for 'gh list'
    """
    pytest.dbgfunc()
    r = ghlib.catch_stdout('gh list')
    for h in hooklist():
        assert h in r


# -----------------------------------------------------------------------------
def test_gh_version():
    """Verify that 'gh --version' works
    """
    z = pexpect.run("gh --version")
    assert version.__version__ in z


# -----------------------------------------------------------------------------
def hooklist():
    """Generator to return the names of the canonical hooks
    """
    for h in ['commit-msg.ver',
              'commit-msg.vc',
              'commit-msg.chgid',
              'pre-commit.ver']:
        yield h

"""
Tests for ghlib routines
"""
from conftest import chdir
from githooks import ghlib
import os
import pytest

# -----------------------------------------------------------------------------
def test_catch_stdout_in(tmpdir):
    """
    Run a command and catch its output with no input. Should see files in root
    of repo.
    """
    pytest.dbgfunc()
    result = ghlib.catch_stdout("bc", input='2+2\n')
    assert '4' in result


# -----------------------------------------------------------------------------
def test_catch_stdout_noin(tmpdir):
    """
    Run a command and catch its output with no input
    """
    pytest.dbgfunc()
    result = ghlib.catch_stdout("ls")
    assert 'githooks' in result
    assert 'tests' in result
    assert 'README.md' in result


# -----------------------------------------------------------------------------
def test_catch_stdout_nosuch(tmpdir):
    """
    Run a command that does not exist and catch its output with no input.
    Output should be empty.
    """
    pytest.dbgfunc()
    result = ghlib.catch_stdout("no_such_command")
    assert 'ERR:' in result
    assert 'No such file or directory' in result


# -----------------------------------------------------------------------------
def test_contents(tmpdir):
    """
    Lines read from file should not contain newlines
    If this line is changed, this test will fail
    """
    pytest.dbgfunc()
    a = ghlib.contents("tests/test_ghlib.py")
    assert type(a) == list
    assert 25 < len(a)
    assert "    If this line is changed, this test will fail" in a
    for l in a:
        assert '\n' not in l


# -----------------------------------------------------------------------------
def test_get_version_ht_justhead(tmpdir):
    """
    Test get_version_ht. With just head, tail should be the empty string
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    vname = 'version.py'
    pkg = os.path.join(td, 'pkg')
    os.mkdir(pkg)
    vsh = "2010.1201."
    vst = "3"
    vs = vsh + vst
    v = open(os.path.join(pkg, vname), 'w')
    v.write('__version__ = "%s"\n' % vs)
    v.close()

    with chdir(td):
        ghlib.catch_stdout('git init')
        (full, head, tail) = ghlib.get_version_ht()

    assert full == vs
    assert head == vsh
    assert tail == int(vst)


# -----------------------------------------------------------------------------
def test_get_version_ht_withtail(tmpdir):
    """
    Test get_version_ht. If the version contains a third segment, that should
    be in tail.
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    vname = 'version.py'
    pkg = os.path.join(td, 'pkg')
    os.mkdir(pkg)
    vsh = "2010.1201."
    vst = "125"
    vs = vsh + vst
    v = open(os.path.join(pkg, vname), 'w')
    v.write('__version__ = "%s"\n' % vs)
    v.close()

    with chdir(td):
        ghlib.catch_stdout('git init')
        (full, head, tail) = ghlib.get_version_ht()

    assert full == vs
    assert head == vsh
    assert tail == int(vst)


# -----------------------------------------------------------------------------
def test_get_version_path_top(tmpdir):
    """
    Should find version.py at top of repo
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    vname = 'version.py'
    tests = os.path.join(td, 'tests')
    pkg = os.path.join(td, 'pkg')
    deep = os.path.join(pkg, 'deep')
    for dn in [td, tests, pkg, deep]:
        if not os.path.exists(dn):
            os.mkdir(dn)
        open(os.path.join(dn, vname), 'w').close()

    with chdir(td):
        ghlib.catch_stdout('git init')
        vpath = ghlib.get_version_path()

    assert vpath == os.path.join(td, vname)


# -----------------------------------------------------------------------------
def test_get_version_path_levone(tmpdir):
    """
    Should find version.py one level down
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    vname = 'version.py'
    pkg = os.path.join(td, 'pkg')
    deep = os.path.join(pkg, 'deep')
    for dn in [pkg, deep]:
        if not os.path.exists(dn):
            os.mkdir(dn)
        open(os.path.join(dn, vname), 'w').close()

    with chdir(td):
        ghlib.catch_stdout('git init')
        vpath = ghlib.get_version_path()

    assert vpath == os.path.join(pkg, vname)


# -----------------------------------------------------------------------------
def test_get_version_path_levtwo(tmpdir):
    """
    Should find version.py two levels down
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    vname = 'version.py'
    pkg = os.path.join(td, 'pkg')
    deep = os.path.join(pkg, 'deep')
    for dn in [pkg, deep]:
        if not os.path.exists(dn):
            os.mkdir(dn)

    open(os.path.join(deep, vname), 'w').close()

    with chdir(td):
        ghlib.catch_stdout('git init')
        vpath = ghlib.get_version_path()

    assert vpath == os.path.join(deep, vname)


# -----------------------------------------------------------------------------
def test_git_describe_ht_notag(tmpdir):
    """
    No tags yet added to repo, so head and tail should both be empty
    """
    pytest.dbgfunc()
    td = str(tmpdir)

    with chdir(td):
        z = ghlib.catch_stdout('git init')
        (full, head, tail) = ghlib.git_describe_ht()

    assert full == ''
    assert head == ''
    assert tail == 0


# -----------------------------------------------------------------------------
def test_git_describe_ht_major(tmpdir):
    """
    Major tag added to the repo and that's the commit we're on -- head is a
    non-empty string, tail is empty
    """
    pytest.dbgfunc()
    td = str(tmpdir)

    with chdir(td):
        z = ghlib.catch_stdout('git init')
        open('version.py', 'w').close()
        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m "test commit"')
        z = ghlib.catch_stdout('git tag -a 2009.0507 -m "test tag"')

        (full, head, tail) = ghlib.git_describe_ht()

    assert full == '2009.0507'
    assert head == '2009.0507'
    assert tail == 0


# -----------------------------------------------------------------------------
def test_git_describe_ht_minor(tmpdir):
    """
    Major tag and a commit have been added to the repo. Head and tail should
    both be non-empty strings.
    """
    pytest.dbgfunc()
    td = str(tmpdir)

    with chdir(td):
        z = ghlib.catch_stdout('git init')
        open('version.py', 'w').close()
        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m "test commit"')
        z = ghlib.catch_stdout('git tag -a 2009.0507 -m "test tag"')
        v = open('version.py', 'w')
        v.write('__version__ = "2009.0507.1"')
        v.close()
        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m "another test commit"')

        (full, head, tail) = ghlib.git_describe_ht()

    assert full == '2009.0507.1'
    assert head == '2009.0507'
    assert tail == 1


# -----------------------------------------------------------------------------
def test_select_absent(tmpdir):
    """
    The search expression is not present
    """
    data = ghlib.contents('tests/test_ghlib.py')
    x = 'This line' + ' better not be present'
    assert '' == ghlib.select(x, data)


# -----------------------------------------------------------------------------
def test_select_present_proper(tmpdir):
    """
    The search expression is present and is a sub-expression of a line
    If this line is missing, this test will fail and here's some extra
    """
    data = ghlib.contents('tests/test_ghlib.py')
    exp = '    If this line is missing, this test will fail'
    actual = ghlib.select(exp, data)
    assert exp in actual
    assert len(exp) < len(actual)


# -----------------------------------------------------------------------------
def test_select_present_exact(tmpdir):
    """
    The search expression is present and exactly matches a line
    This should match exactly
    """
    data = ghlib.contents("tests/test_ghlib.py")
    exp = '    This should match exactly'
    actual = ghlib.select(exp, data)
    assert exp == actual
    assert len(exp) == len(actual)


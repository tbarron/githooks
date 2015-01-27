"""
version is not updated
version is updated but not staged
version is staged and ready to go
"""
from conftest import chdir
import editor
from githooks import ghlib
import os
import pytest

def test_pcv_0_not_updated(tmpdir):
    """
    Test pre-commit with version.py not updated from last commit
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    cmd = os.path.abspath(os.path.join('.', 'githooks', 'pre-commit.ver'))

    with chdir(td):
        tag = "2013.1015"
        z = ghlib.catch_stdout('git init')

        v = open('version.py', 'w')
        v.write('__version__ = "%s"' % tag)
        v.close()

        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m inception')
        z = ghlib.catch_stdout('git tag -a -m "version basis" %s' % tag)

        result = ghlib.catch_stdout(cmd)
        assert 'Looks like version.py should contain' in result
        assert "but it's got " in result


def test_pcv_1_not_staged(tmpdir):
    """
    Test pre-commit with version.py updated but not staged
    """
    pytest.dbgfunc()
    td = str(tmpdir)
    cmd = os.path.abspath(os.path.join('.', 'githooks', 'pre-commit.ver'))

    with chdir(td):
        tag = "2013.1015"
        z = ghlib.catch_stdout('git init')

        v = editor.editor('version.py', ['__version__ = "%s"' % tag])
        v.quit(save=True)

        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m inception')
        z = ghlib.catch_stdout('git tag -a -m "version basis" %s' % tag)

        v = editor.editor('version.py')
        v.sub('1015', '1015.1')
        v.quit(save=True)

        result = ghlib.catch_stdout(cmd)
        assert 'is not staged. Looks like you need' in result
        assert "try your commit again." in result


def test_pcv_2_updated_staged(tmpdir):
    pytest.dbgfunc()
    td = str(tmpdir)
    cmd = os.path.abspath(os.path.join('.', 'githooks', 'pre-commit.ver'))

    with chdir(td):
        tag = "2013.1015"
        z = ghlib.catch_stdout('git init')

        v = editor.editor('version.py', ['__version__ = "%s"' % tag])
        v.quit(save=True)

        z = ghlib.catch_stdout('git add version.py')
        z = ghlib.catch_stdout('git commit -m inception')
        z = ghlib.catch_stdout('git tag -a -m "version basis" %s' % tag)

        v = editor.editor('version.py')
        v.sub('1015', '1015.1')
        v.quit(save=True)

        z = ghlib.catch_stdout('git add version.py')
        result = ghlib.catch_stdout(cmd)

        assert '' in result

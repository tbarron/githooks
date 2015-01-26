"""
Need tests for
 - commit-msg.chgid
 + commit-msg.ver
 - commit-msg.vc
 - pre-commit.ver
 - ghlib.py
"""
from conftest import chdir
from githooks import ghlib
import os
import pdb
import pexpect
import pytest
import editor
from githooks import version

# -----------------------------------------------------------------------------
def commit_msg_name(sfx):
    return os.path.abspath("./githooks/commit-msg." + sfx)


# -----------------------------------------------------------------------------
def egdata():
    """
    Sample data for tests
    """
    eg = ["Add test for 'like' in ttype lookup",
          '',
          " - 'like' support for ttype lookup is implemented by calling",
          "    tpop_select_by_paths() so that's what we actually test",
          '',
          'Version:   2014.1217.46',
          'Change-Id: Ia9c0832881fadc61e6511826f4112df72525f1e8',
          '# ',
          '# This here is a comment',
          '#']
    return eg


# -----------------------------------------------------------------------------
def commit_msg_name():
    return "./githooks/commit-msg.ver"


# -----------------------------------------------------------------------------
def test_nov_noc(tmpdir):
    """
    Version not present, Change-Id not present
    """
    path = os.path.join(str(tmpdir), 'example.nov_noc')
    q = editor.editor(path, content=egdata())
    q.delete('(Version|Change-Id): ')
    q.quit(save=True)

    cmd = ('%s %s' % (commit_msg_name(), path))
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])


# -----------------------------------------------------------------------------
def test_cmvx_nov(tmpdir):
    """
    Testing commit-msg.ver, version not present
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.nov_noc')
    q = editor.editor(path, content=egdata())
    q.delete('(Version|Change-Id): ')
    q.quit(save=True)

    cmd = ('%s %s' % (commit_msg_name(), path))
    pexpect.run(cmd)

    exp = 'Version:   %s' % version.__version__
    z = contents(path)
    assert any([exp in l for l in z])
    assert all(['Change-Id: I' not in l for l in z])


# -----------------------------------------------------------------------------
def test_cmvx_mtv(tmpdir):
    """
    Testing commit-msg.ver, version is empty
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.nov_noc')
    q = editor.editor(path, content=egdata())
    q.sub('Version:\s+.*', 'Version:')
    q.delete('Change-Id: ')
    q.quit(save=True)

    cmd = ('%s %s' % (commit_msg_name(), path))
    pexpect.run(cmd)

    exp = 'Version:   %s' % version.__version__
    z = contents(path)
    assert any([exp in l for l in z])
    assert all(['Change-Id: I' not in l for l in z])


# -----------------------------------------------------------------------------
def test_cmvx_ver(tmpdir):
    """
    Testing commit-msg.ver, version is present
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.nov_noc')
    q = editor.editor(path, content=egdata())
    q.delete('Change-Id: ')
    q.quit(save=True)

    exp = setup_version(tmpdir)
    cmd = ('%s %s' % (commit_msg_name('ver'), path))

    with chdir(str(tmpdir)):
        z = ghlib.catch_stdout(cmd)

    z = ghlib.contents(path)
    assert not exp_in_list(exp, z)
    assert exp_in_list('Version:  ', z, exact=False)
    assert not exp_in_list('Change-Id: I', z, exact=True)
    assert not exp_in_list('Change-Id: I', z, exact=False)
    assert "\n\n\n" not in ''.join(z)


# -----------------------------------------------------------------------------
def test_cmxc_noc(tmpdir):
    """
    Version irrelevant, Change-Id not present
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.noc')

    q = editor.editor(path, content=egdata())
    q.delete('(Version|Change-Id): ')
    q.quit(save=True)

    cmd = ('%s %s' % (commit_msg_name('chgid'), path))

    with chdir(str(tmpdir)):
        z = ghlib.catch_stdout('git init')
        z = ghlib.catch_stdout(cmd)

    z = ghlib.contents(path)
    assert not exp_in_list('Version:', z, exact=False)
    assert exp_in_list('Change-Id: I', z, exact=False)
    assert "\n\n\n" not in ''.join(z)


# -----------------------------------------------------------------------------
def test_cmxc_mtc(tmpdir):
    """
    Version irrelevant, Change-Id is empty
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.mtc')

    q = editor.editor(path, content=egdata())
    q.delete('(Version): ')
    q.sub('Change-Id:\s+.*', 'Change-Id:  ')
    q.quit(save=True)

    cmd = " ".join([commit_msg_name('chgid'), path])

    with chdir(str(tmpdir)):
        z = ghlib.catch_stdout('git init')
        z = ghlib.catch_stdout(cmd)

    z = ghlib.contents(path)
    assert not exp_in_list('Version:', z, exact=False)
    assert exp_in_list('Change-Id: I', z, exact=False)
    assert "\n\n\n" not in ''.join(z)


# -----------------------------------------------------------------------------
def test_cmxc_chid(tmpdir):
    """
    Version irrelevant, Change-Id is present
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.chid')

    q = editor.editor(path, content=egdata())
    q.delete('(Version): ')
    q.quit(save=True)

    cmd = " ".join([commit_msg_name('chgid'), path])

    with chdir(str(tmpdir)):
        z = ghlib.catch_stdout('git init')
        z = ghlib.catch_stdout(cmd)

    z = ghlib.contents(path)

    assert not exp_in_list('Version:', z, exact=False)
    assert exp_in_list('Change-Id: I', z, exact=False)
    assert "\n\n\n" not in ''.join(z)


# -----------------------------------------------------------------------------
def test_cmvc_nov_noc(tmpdir):
    """
    Version not present, Change-Id not present
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.nov_noc')

    q = editor.editor(path, content=egdata())
    q.delete('(Version|Change-Id): ')
    q.quit(save=True)

    exp = setup_version(tmpdir)
    cmd = ('%s %s' % (commit_msg_name('vc'), path))

    with chdir(str(tmpdir)):
        z = ghlib.catch_stdout('git init')
        z = ghlib.catch_stdout(cmd)

    exp = 'Version:   2014.1217.46'
    z = contents(path)
    assert any([exp in l for l in z])
    assert all(['Change-Id: I' not in l for l in z])


# -----------------------------------------------------------------------------
def test_nov_mtc(tmpdir):
    """
    Version not present, Change-Id is empty
    """
    pytest.dbgfunc()
    path = os.path.join(str(tmpdir), 'example.nov_mtc')
    q = editor.editor(path, content=egdata())
    q.delete('(Version): ')
    q.sub('Change-Id:\s+.*', 'Change-Id:  ')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])

    
# -----------------------------------------------------------------------------
def test_nov_chid(tmpdir):
    """
    Version not present, Change-Id is present
    """
    path = os.path.join(str(tmpdir), 'example.nov_chid')
    q = editor.editor(path, content=egdata())
    q.delete('(Version): ')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])


# -----------------------------------------------------------------------------
def test_mtv_noc(tmpdir):
    """
    Version is empty, Change-Id not present
    """
    path = os.path.join(str(tmpdir), 'example.mtv_noc')
    q = editor.editor(path, content=egdata())
    q.sub('Version:\s+.*', 'Version:')
    q.delete('Change-Id:')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])
    assert all(['Change-Id: I75803' not in l for l in z])


# -----------------------------------------------------------------------------
def test_mtv_mtc(tmpdir):
    """
    Version is empty, Change-Id is empty
    """
    path = os.path.join(str(tmpdir), 'example.mtv_noc')
    q = editor.editor(path, content=egdata())
    q.sub('Version:\s+.*', 'Version:')
    q.sub('Change-Id:\s.*', 'Change-Id:')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])
    assert all(['Change-Id: I75803' not in l for l in z])


# -----------------------------------------------------------------------------
def test_mtv_chid(tmpdir):
    """
    Version is empty, Change-Id is present
    """
    path = os.path.join(str(tmpdir), 'example.mtv_noc')
    q = editor.editor(path, content=egdata())
    q.sub('Version:\s+.*', 'Version:')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2015.0112.x' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])
    assert any(['Change-Id: I75803' not in l for l in z])


# -----------------------------------------------------------------------------
def test_ver_noc(tmpdir):
    """
    Version is present, Change-Id is not
    """
    path = os.path.join(str(tmpdir), 'example.ver_noc')
    q = editor.editor(path, content=egdata())
    q.delete('(Change-Id): ')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2014.1217.46' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])


# -----------------------------------------------------------------------------
def test_ver_mtc(tmpdir):
    """
    Version is present, Change-Id is empty
    """
    path = os.path.join(str(tmpdir), 'example.ver_mtc')
    q = editor.editor(path, content=egdata())
    q.sub('Change-Id:\s+.*', 'Change-Id:')
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2014.1217.46' in l for l in z])
    assert any(['Change-Id: I' in l for l in z])

    
# -----------------------------------------------------------------------------
def test_ver_chid(tmpdir):
    """
    Version is present, Change-Id is present
    """
    path = os.path.join(str(tmpdir), 'example.ver_chid')
    q = editor.editor(path, content=egdata())
    q.quit(save=True)

    # cmd = ('./githooks/commit-msg %s' % path)
    cmd = " ".join([commit_msg_name(), path])
    pexpect.run(cmd)

    z = contents(path)
    assert any(['Version:   2014.1217.46' in l for l in z])
    assert any(['Change-Id: Ia9c08' in l for l in z])

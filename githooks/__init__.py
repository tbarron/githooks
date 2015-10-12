"""git hook manager

git hooks are scripts stored in $REPO/.git/hooks that git invokes at various
points in the development cycle (before commit, after the commit message is
composed, etc.). See 'man git' for details.

gh will install, list, show, and remove useful hooks in a git repository. By
default, it puts scripts in $REPO/githooks with symlinks from $REPO/.git/hooks
into $REPO/githooks. With the -d option on the install command, it will put the
script directly in $REPO/.git/hooks.

Usage:
   gh list [(-d | --debug)]
   gh freeze [(-d | --debug)] <filename>
   gh install  [(-d | --debug)] [-g] <hookname>
   gh show [(-d | --debug)]
   gh remove  [(-d | --debug)] <hookname>
   gh (-h | --help)
   gh --version

Options:
   -h --help        Provide help info (this document)
   --version        Show version
   -g               Install hook script in .git/hooks dir
"""
import inspect
import pdb
from docopt import docopt
import sys

try:
    from githooks import version
except:
    pass


# -----------------------------------------------------------------------------
def main():
    """Entrypoint
    """
    o = docopt(sys.modules[__name__].__doc__)
    if o['--debug'] or o['-d']:
        pdb.set_trace()

    if o['--version']:
        print(version.__version__)
        sys.exit()

    for k in (_ for _ in o.keys() if _[0] not in ('-', '<') and o[_]):
        f = getattr(sys.modules[__name__], "_".join(['gh', k]))
        f(sys.argv[2:])


# -----------------------------------------------------------------------------
def gh_list(opts):
    """
    gh list displays a list of available hook routines that can be installed

    Usage:
       gh list [-d | --debug]
    """
    hd = hookdict()
    for k in hd:
        print("%s: %s" % (k, hd[k]))


# -----------------------------------------------------------------------------
def gh_install(args):
    hd = hookdict()
    print("called gh_install(%s)" % args)


# -----------------------------------------------------------------------------
def gh_show(args):
    print("called gh_show(%s)" % args)


# -----------------------------------------------------------------------------
def gh_remove(args):
    print("called gh_remove(%s)" % args)


# -----------------------------------------------------------------------------
def hookdict():
    """
    Generate and return a dict of hook routines that looks like:

        {'commit-msg.ver': <function-object>,
         'pre-commit.ver': <function-object>',
         ...
         }

    Hook function name must start with 'hook_'. First word in __doc__ must be
    the installable name of the hook (commit-msg.ver, pre-commit.ver, etc.)
    """
    md = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    hd = dict([(k, v) for k, v in md if k.startswith('hook_')])
    rv = {}
    for k in hd:
        d = hd[k].__doc__
        n = d.strip().split()[0]
        rv[n] = hd[k]

    return rv


# -----------------------------------------------------------------------------
def hook_commit_msg_ver():
    """
    commit-msg.ver - Makes sure a version appears in the commit message

    After you write your commit message, this hook will scan it and add a line
    like

        Version:   A.B.C

    if one is not already present.
    """
    print("hook code to be installed")


# -----------------------------------------------------------------------------
def hook_commit_msg_vc():
    """commit-msg.vc - Ensure commit message contains a version and change id

    After you write your commit message, this hook will scan it and add lines
    like

        Version:   A.B.C
        ChangeId:  <hash value>

    if they are not already present.
    """
    print("hook code to be installed")


# -----------------------------------------------------------------------------
def hook_commit_msg_chgid():
    """commit-msg.chgid - Ensure commit message contains a change id

    After you write your commit message, this hook will scan it and add a line
    like

        ChangeId:  <hash value>

    if one is not already present.
    """
    print("hook code to be installed")


# -----------------------------------------------------------------------------
def hook_pre_commit_ver():
    """pre-commit.ver - Verify version.py

    With this hook installed, when you run 'git commit', before starting your
    editor on the commit message, git will check that version.py exists, has
    been updated since the last commit, and is staged. If any of those
    conditions are not satisfied, pre-commit.ver will put out a message
    explaining the problem and asking you to correct it.
    """
    print("hook code to be installed")


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.path.append('githooks')
    import version
    main()

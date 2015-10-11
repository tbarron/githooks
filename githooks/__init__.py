"""git hook manager

git hooks are scripts stored in $REPO/.git/hooks that git invokes at various
points in the development cycle (before commit, after the commit message is
composed, etc.). See 'man git' for details.

gh will install, list, show, and remove useful hooks in a git repository. By
default, it puts scripts in $REPO/githooks with symlinks from $REPO/.git/hooks
into $REPO/githooks. With the -d option on the install command, it will put the
script directly in $REPO/.git/hooks.

Usage:
   gh list
   gh install [-g] <hookname>
   gh show
   gh remove <hookname>
   gh (-d | --debug)
   gh (-h | --help)
   gh --version

Options:
   -h --help        Provide help info (this document)
   --version        Show version
   -g               Install hook script in .git/hooks dir
"""
try:
    from githooks import version
except:
    pass
import pdb
from docopt import docopt
import sys


# -----------------------------------------------------------------------------
def main():
    o = docopt(sys.modules[__name__].__doc__)
    if o['--debug'] or o['-d']:
        pdb.set_trace()

    if o['--version']:
        print(version.__version__)
        sys.exit()

    for k in ['list', 'install', 'show', 'remove']:
        if o[k]:
            f = getattr(sys.modules[__name__], "_".join(['gh', k]))
            f(sys.argv[2:])


# -----------------------------------------------------------------------------
def gh_list(args):
    print("called gh_list(%s)" % args)


# -----------------------------------------------------------------------------
def gh_install(args):
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
if __name__ == '__main__':
    sys.path.append('githooks')
    import version
    main()

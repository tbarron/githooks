"""Githooks manager

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
   -g               Install hook script dire
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
if __name__ == '__main__':
    sys.path.append('githooks')
    import version
    main()

# git hook scripts for various purposes

### commit-msg.ver (linkname: commit-msg)

Adds a version line based on a file named 'version.py' to each git
commit message if not already present.

### commit-msg.chgid (linkname: commit-msg)

Adds a gerrit-friendly Change-Id line to each commit message if not
already present.

### commit-msg.vc (linkname: commit-msg)

Adds both gerrit-friendly Change-Id and Version line to each commit
message if not already present.

### pre-commit.ver (linkname: pre-commit)

Checks 1) that version.py has been incremented since last commit and
2) that version.py is staged for the upcoming commit. This enforces a
version update for each commit (some folks may think this is
overkill).

# development approach

  * activate virtual environment gh
  * git status
  * commit anything outstanding
  * git push

  * set version M.N.P
  * make branch
  * write test
  * while not ready for release
    * while test is not satisfied
      * tweak
    * set version M.N.(P+1)
    * git commit
    * write another test

  * ready for release
  * git checkout master
  * git merge branch
  * set version M.(N+1).0.cC
  * git tag -a M.(N+1).0.cC
  * make sdist
  * test deploy
  * while deploy fails
    * tweak
    * set version M.(N+1).0.c(C+1)
    * git commit
    * git tag -a M.(N+1).0.c(C+1)
    * make sdist
    * test deploy
  * set version M.(N+1).0
  * git commit
  * git push
  * git tag -a M.(N+1).0
  * git push --tag

Jeff sez this file should contain at least
  * a description of the project -- check
  * a link to the project's readthedocs page (not yet)
  * A TravisCI button showing the state of the build (not yet)
  * QuickStart documentation (not yet)
  * List of non-Python dependencies and how to install them (git?)

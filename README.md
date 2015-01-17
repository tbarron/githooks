# githooks - git hook scripts for various purposes

### commit-msg.ver

Adds a version line based on a file named 'version.py' to each git commit message

### commit-msg.chgid

Adds a gerrit-friendly Change-Id line to each commit message

### commit-msg.vc

Adds both gerrit-friendly Change-Id and Version line to each commit message

### pre-commit.ver

Checks 1) that version.py has been incremented since last commit and
2) that version.py is staged for the upcoming commit.


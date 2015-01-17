# -----------------------------------------------------------------------------
def catch_stdout(cmd, input=None):
    """
    Run *cmd*, optionally passing string *input* to it on stdin, and return
    what the process writes to stdout
    """
    p = subprocess.Popen(shlex.split(cmd),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if input:
        p.stdin.write(input)
    (o, e) = p.communicate()
    if p.returncode == 0:
        return o
    else:
        return ''

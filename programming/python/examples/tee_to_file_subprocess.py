#!/usr/bin/env python3

import sys
import os
import datetime
import subprocess
import contextlib
import threading


class TeeLogger:
    def __init__(self, stream, logfile):
        self.original_stream = stream
        self.logfile = logfile

    def write(self, data):
        self.original_stream.write(data)
        self.original_stream.flush()
        if data == os.linesep:
            self.logfile.write(data)
        else:
            self.logfile.write(datetime.datetime.now().replace(microsecond=0).isoformat() + " " + data)
        self.logfile.flush()

    def flush(self):
        self.original_stream.flush()
        self.logfile.flush()


@contextlib.contextmanager
def tee_output(logfile_path):
    """Context manager that tees stdout/stderr to a logfile and restores them automatically"""
    with open(logfile_path, "a", encoding="utf8") as logfile:
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = TeeLogger(stream=sys.stdout, logfile=logfile)
            sys.stderr = TeeLogger(stream=sys.stderr, logfile=logfile)
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def run_command_with_live_output(command):
    # check_call with stdout=sys.stdout, stderr=sys.stderr won't do because
    # subprocess doesn't use these parameters as objects. If stdout or stderr is
    # an object, it gets fileno property and writes directly using it. Proxying
    # original_stream's fileno property in TeeLogger helps, but nothing gets into
    # our log file for obvious reasons
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,  # Line buffered
        universal_newlines=True,  # Text mode
        encoding="utf-8",  # Explicit encoding
        errors="replace",  # Handle encoding errors
    )

    def handle_stream(stream, output):
        for line in stream:
            output.write(line)
            output.flush()
        stream.close()

    # Start threads for stdout and stderr
    stdout_thread = threading.Thread(target=handle_stream, args=(process.stdout, sys.stdout))
    stderr_thread = threading.Thread(target=handle_stream, args=(process.stderr, sys.stderr))

    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()

    # Wait for process to complete
    process.wait()

    # Wait for threads to finish processing remaining output
    stdout_thread.join(timeout=1)
    stderr_thread.join(timeout=1)

    # Check exit code
    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, process.args, None, None  # We're already showing output live
        )

    return process.returncode


def main():
    with tee_output("/tmp/python_logfile_test.log"):
        print("This goes to stdout and log file (INFO level)")
        print("This goes to stderr and log file (ERROR level)", file=sys.stderr)

        run_command_with_live_output(("ping", "-c", "10", "localhost"))


if __name__ == "__main__":
    main()

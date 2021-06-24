#!/usr/bin/python3

import os
import tempfile
import threading
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))

def write_named_pipe(np_path):
    # We use a named pipe (FIFO special file) instead of a regular file because it has
    # no contents on the filesystem; the filesystem entry merely serves as a reference
    # point so that processes can access the pipe using a name in the filesystem.
    os.mkfifo(np_path, mode=0o600)
    with open(np_path, "w") as np_file:
        # This is to make sure the file is deleted after use. Since it is open, the
        # descriptor is still available for the current process (and subprocesses). The
        # filesystem entry will be deleted by the filesystem on close. Even if we don't
        # close if explicitly, the kernel will do this automatically when the process
        # exits (including kills and crashes).
        os.unlink(np_path)
        np_file.write("test\n")


with tempfile.TemporaryDirectory() as tmp_dir:
    np_path = os.path.join(tmp_dir, "np_test.tmp")
    print(np_path)

    threading.Thread(target=write_named_pipe, name="write_np", args=(np_path,)).start()
    print("starting")
    subprocess.check_call([os.path.join(script_dir, "read_file.sh"), np_path])
    print("finishing")

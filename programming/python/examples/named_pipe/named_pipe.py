#!/usr/bin/python3

import os
import tempfile
import subprocess

script_dir = os.path.dirname(os.path.realpath(__file__))

with tempfile.TemporaryDirectory() as tmp_dir:
    np_path = os.path.join(tmp_dir, "np_test.tmp")
    print(np_path)
    os.mkfifo(np_path, mode=0o600, dir_fd=os.O_RDWR)
    # os.mkfifo(np_path)
    # with open(np_path, "w") as np_file:
    fd = os.open(np_path, os.O_RDWR)
    f = os.fdopen(fd, "w")
        # pass
    #     print("unlink", flush=True)
    #     # os.unlink(np_path)
    #     print("write", flush=True)
    f.write("test_me1\n")
    f.write("test_me2\n")
    # subprocess.check_call([os.path.join(script_dir, "read_file.sh"), np_path])
    input("Press Enter to continue...")

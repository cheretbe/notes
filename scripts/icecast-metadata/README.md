* https://github.com/dirble/streamscrobbler-python/tree/master
* There is a Python3 fork: https://github.com/andreztz/streamscrobbler-python
    * https://pypi.org/project/streamscrobbler3/
    * Doesn't seem to work(`get_server_info()` returns nothing)

So we just stick with Python2 version in Docker:
```shell
docker run -v $(pwd)/absolutechillout:/data --rm -it python:2.7.18-stretch bash
pip install httplib2  streamscrobbler@git+https://github.com/dirble/streamscrobbler-python
git clone https://github.com/cheretbe/notes.git
notes/scripts/icecast-metadata/get_metadata.py /data/absolutechillout.com_tracks.txt
```

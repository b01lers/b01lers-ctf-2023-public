# cfifufuuufuuuuu

This is a `pwn` challenge written in C and Python.

The files to be distributed (and that need to go into the docker container) are `s` (from `src/s.c`) and `loader.pyc` (from `src/loader.py`).

To build the challenge, use the script `src/test_and_build.sh`.
This script takes care of building `loader.pyc` and `s`, testing them, and copying all files in the different directories (`solve/`, `dist/`, and `deploy/`).
However, **do not rebuild the challenge by yourself**.
The solution relies on specific addresses, and recompiling `s` would likely change them.
The challenge needs to be compiled and run on `Ubuntu 18.04`.
The `Dockerfile` takes care of creating a container running the proper Linux version.

### Running
```bash
cd deploy
docker-compose up
```

### Testing
After running the challenge as explained above, run:
```bash
cd solve
python3 ./test_all.py 127.0.0.1 3071
```

### Solving
See [solve/solve.md](solve/solve.md)


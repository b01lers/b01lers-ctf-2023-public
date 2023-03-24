# CTF Name

A template repository for a CTF competition. This is a description of the CTF event.

[CTFTime Link](https://ctftime.org/event/<this-ctfs-page>)

# Structure

Challenges are organized by category into subdirectories:

- rev
- pwn
- web
- crypto
- misc


Inside each challenge, there may be several of the following:

- src: contains the source code for the challenge
- dist: the files that are provided to players during the competition
- deploy: files used to deploy remote challenges (generally, dockerfiles and such)
- solve: files pertaining to the solution of the challenge, usually including a writeup

- Challenges that were deployed with KCTF also have their KCTF configurations included. 
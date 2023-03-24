# Installation

`$ \python3 -m pip install -r requirements.txt`

# Usage

```
usage: mkchal.py [-h] --type {rev,pwn,crypto,web,misc} --name NAME --author AUTHOR --description DESCRIPTION
                 [DESCRIPTION ...] --flag FLAG --provides PROVIDES [PROVIDES ...] --ports PORTS [PORTS ...]
                 [--remote REMOTE [REMOTE ...]]

Create a CTF challenge.

optional arguments:
  -h, --help            show this help message and exit
  --type {rev,pwn,crypto,web,misc}, -t {rev,pwn,crypto,web,misc}
                        The type of the challenge.
  --name NAME, -n NAME  The name of the challenge. Example: `a_creative_name`
  --author AUTHOR, -a AUTHOR
                        The author's name. Example: `you`
  --description DESCRIPTION [DESCRIPTION ...], -d DESCRIPTION [DESCRIPTION ...]
                        The description of the challenge. Example: `This is a description...good luck!
  --flag FLAG, -f FLAG  The flag for the challenge. Example: `flag{flag!}`
  --provides PROVIDES [PROVIDES ...], -p PROVIDES [PROVIDES ...]
                        The paths to files that the challenge provides. Example: `dist/chal dist/chal.tar.gz`
  --ports PORTS [PORTS ...], -P PORTS [PORTS ...]
                        The ports that the challenge provides. Example: 1337 1338
  --remote REMOTE [REMOTE ...], -r REMOTE [REMOTE ...]
                        The command to run from the challenge directory to deploy.Example: `docker-compose --project_name
                        chal up --build`
```

# Example

`$  \python3 mkchal/mkchal.py --type pwn --name chal --author novafacing --description Okay, now hijack control flow. --flag 'flag{this_is_a_flag}' --provides dist/chal --ports 1337 --remote 'cd deploy && docker-compose --project_name chal --force-recreate --build up'`
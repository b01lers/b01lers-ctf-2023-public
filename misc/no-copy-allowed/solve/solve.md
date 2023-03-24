# No Copy Allowed - misc

The first 200 webpages are trivial, just parse the html and extract the text.
Starting from the 201st page, the text is encoded in custom fonts using ligatures, so we need to parse the font file and decode the text before proceeding to the next page.

The flag can be found on the 1000th page.

Please refer to the script below for further details.

```python
import requests, re, tempfile
from fontTools.ttLib import TTFont

urlbase = "http://HOSTNAME:4567"

name_map = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'underscore': '_',
    'braceleft': '{',
    'braceright': '}',
    'space': ' ',
    'comma': ',',
    'period': '.',
    'exclam': '!',
    'question': '?',
    'hyphen': '-',
}

def name_to_char(name):
    if name in name_map:
        return name_map[name]
    return name

def parse_ligas(fontpath):
    font = TTFont(fontpath)
    liga_lookup = font['GSUB'].table.LookupList.Lookup[0].SubTable[0].ligatures
    ligas = {}
    for first_glyph, lookuplist in liga_lookup.items():
        for lookup in lookuplist:
            ligas["".join([name_to_char(i) for i in [first_glyph] + lookup.Component])] = name_to_char(lookup.LigGlyph)
    return ligas

def decode(text, ligas):
    # copilot wrote this, I didn't check it but it seems to work
    decoded = ""
    i = 0
    while i < len(text):
        for liga in ligas:
            if text[i:].startswith(liga):
                decoded += ligas[liga]
                i += len(liga)
                break
        else:
            decoded += text[i]
            i += 1
    return decoded


def solve(path="index.html"):
    r = requests.get(f"{urlbase}/{path}")
    fontpath = re.search(r"url\(\"(.+)\"\)", r.text).group(1)
    text = re.search(r'<p>(.*?)</p>', r.text).group(1)
    try:
        text = re.search(r'<span>(.*?)</span>', text).group(1)
    except:
        pass
    if len(text) == 40:
        return text
    with tempfile.NamedTemporaryFile() as f:
        f.write(requests.get(f"{urlbase}/{fontpath}").content)
        return decode(text, parse_ligas(f.name))

page = "index"
while True:
    page = solve(f"{page}.html")
    print(page)
    if "bctf{" in page:
        break
```

For further information, please refer to https://learn.microsoft.com/en-us/typography/opentype/spec/gsub#LS

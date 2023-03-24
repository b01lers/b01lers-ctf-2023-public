import random, os, string, multiprocessing, tempfile, shutil

class LevelType:
    PLAIN = 0b00000000
    LIGA = 0b00000001
    ANTI_OCR = 0b00000010

LEVELS = ([LevelType.PLAIN] * 2 + [LevelType.ANTI_OCR] * 2) * 50 + \
         [LevelType.LIGA] * 100 + [LevelType.LIGA | LevelType.ANTI_OCR] * 700

LEVEL_IDS = [''.join(random.choices(string.ascii_letters + string.digits, k=40)) for _ in range(len(LEVELS))]
FLAG = "bctf{l1gatur3_4bus3_15_fun_X0UOBDvfRkKa99fEVloY0iYuaxzS9hj4rIFXlA3B}"

output_dir = "/var/www/localhost/htdocs"
font_name = "ZXX"

charset = string.ascii_letters + string.digits + '_{} ,.!?-'
repr = {
    **{char:f"\{char}" for char in string.ascii_letters},
    '0': '\\zero',
    '1': '\\one',
    '2': '\\two',
    '3': '\\three',
    '4': '\\four',
    '5': '\\five',
    '6': '\\six',
    '7': '\\seven',
    '8': '\\eight',
    '9': '\\nine',
    '_': '\\underscore',
    '{': '\\braceleft',
    '}': '\\braceright',
    ' ': '\\space',
    ',': '\\comma',
    '.': '\\period',
    '!': '\\exclam',
    '?': '\\question',
    '-': '\\hyphen',
}

html = """
<html>
	<head>
        <style>
            @font-face {{font-family:b;src:url("{fontpath}")}}
            p, input {{ font-size:3vw; }}
            span {{ font-family:b;font-size:2vw; }}
            input {{ border: solid 0.4vw;width:60vw; }}
        </style>
	</head>
	<body>
		<table width="100%" height="100%"><tbody><tr><td><center>
            <p>Enter "<span>{encoded}</span>" to continue</p><input>
		</center></td></tr></tbody></table>
        <script>
            var input = document.querySelector("input");
            input.addEventListener("keypress", function(e) {{
                if (e.keyCode == 13) {{
                    window.location.href = input.value + ".html";
                }}
            }});
        </script>
	</body>
</html>
"""

flag_html = """
<html>
	<head>
        <style>
            @font-face {{font-family:b;src:url("{fontpath}")}}
            p {{ font-size:3vw; font-family:b; }}
        </style>
	</head>
	<body>
		<table width="100%" height="100%"><tbody><tr><td><center>
            <p>{encoded}</p>
		</center></td></tr></tbody></table>
	</body>
</html>
"""

def liga_gen(k=5):
    ligas = {}
    for char in charset:
        ligas[char] = random.choices(charset[:52], k=k)
    return ligas

def encode(ligas, text):
    if ligas:
        return ".".join("".join(ligas[char]) for char in text) + "."
    else:
        return text

def feature_gen(ligas):
    result = "feature liga {\n"
    for char, sub in ligas.items():
        result += f"    sub {' '.join(sub)} \\period by {repr[char]};\n"
    result += "} liga;"
    return result

def font_gen(temp_ufo_path, ttf_path, ligas=None, anti_ocr=False):
    shutil.copytree(os.path.join("fonts", f"{font_name}.ufo"), temp_ufo_path)
    if ligas:
        with open(f"{temp_ufo_path}/features.fea", "w") as f:
            f.write(feature_gen(ligas))
    if anti_ocr:
        for c in string.ascii_letters:
            style = random.choice(['Default', 'Camo', 'False', 'Noise', 'Xed'])
            if style != 'Default':
                glif_filename = f"{c}.glif" if c in string.ascii_lowercase else f"{c}_.glif"
                shutil.copyfile(os.path.join("fonts", f"{font_name}-{style}-Glyphs", f"{glif_filename}"), os.path.join(temp_ufo_path, "glyphs", f"{glif_filename}"))
    os.system(f"fontmake -u {temp_ufo_path} -o ttf --output-path {ttf_path}")

def level_gen(level, temp_ufos):
    ligas = None
    anti_ocr = False
    level_name = LEVEL_IDS[level] if level != 0 else "index"
    template = html if level != len(LEVEL_IDS)-1 else flag_html
    content = LEVEL_IDS[level+1] if level != len(LEVEL_IDS)-1 else FLAG

    if LEVELS[level] & LevelType.LIGA:
        ligas = liga_gen()
    if LEVELS[level] & LevelType.ANTI_OCR:
        anti_ocr = True

    font_gen(f"{temp_ufos}/{level}", f"{output_dir}/{level_name}.ttf", ligas, anti_ocr)
    with open(f"{output_dir}/{level_name}.html", "w") as f:
        f.write(template.format(
            fontpath=f"{level_name}.ttf",
            encoded=encode(ligas, content),
        ))

def generate_challenge():
    if not os.path.exists(f"{output_dir}"):
        os.makedirs(f"{output_dir}")
    with tempfile.TemporaryDirectory() as temp_ufos:
        with multiprocessing.Pool() as pool:
            pool.starmap(level_gen, [(level, temp_ufos) for level in range(len(LEVELS))])

generate_challenge()

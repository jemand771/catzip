import io
import multiprocessing.pool
import zipfile

import requests
from flask import Flask, send_file

APP = Flask(__name__)
MESSAGE = "the .zip tld was a great idea"
# language=markdown
README = f"""# malzware.zip

{MESSAGE}

look, I'm just trying to shitpost.
let me know if you have cool ideas for this - I'm @jemand771 pretty much everywhere.

powered by [The Cat API](https://thecatapi.com)
"""


@APP.get("/")
def download():
    words = MESSAGE.split()
    cats: list[dict[str, str | int]] = requests.get(
        f"https://api.thecatapi.com/v1/images/search?limit={len(words)}"
    ).json()
    buf = io.BytesIO()
    with multiprocessing.pool.ThreadPool(len(words)) as pool:
        images = pool.map(lambda url: requests.get(url).content, [cat.get("url") for cat in cats])
    with zipfile.ZipFile(buf, "w") as archive:
        for i, (cat, r, word) in enumerate(zip(cats, images, words)):
            _, ext = cat.get("url").rsplit(".", 1)
            archive.writestr(f"{i}. {word}.{ext}", r)
        archive.writestr("README.md", README)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name="malzware.zip",
        mimetype="application/zip"
    )


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5000, debug=True)

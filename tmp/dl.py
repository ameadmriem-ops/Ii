import urllib.request
import re

url = "https://www.mediafire.com/file/tv0d0fr3nvj3o6a/MY_MOVIE_project.zip/file"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")
print("Page length:", len(html))

# Look for download url pattern
match = re.search(r'href="(https://download[^"]+)"', html)
if match:
    print("Direct link:", match.group(1))
    durl = match.group(1)
else:
    # Look for any downloadButton link
    match2 = re.search(r'id="downloadButton"[^>]*href="([^"]+)"', html)
    if match2:
        print("Direct link:", match2.group(1))
        durl = match2.group(1)
    else:
        # Search all links with .zip
        zips = re.findall(r'href="([^"]+\.zip[^"]*)"', html)
        print("Zip links:", zips)
        durl = zips[0] if zips else None

if durl:
    print("Downloading from:", durl)
    req2 = urllib.request.Request(durl, headers=headers)
    with urllib.request.urlopen(req2) as resp, open("/tmp/MY_MOVIE_project.zip", "wb") as f:
        f.write(resp.read())
    print("Download completed!")

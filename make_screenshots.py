import os
import shutil
import glob
from playwright.sync_api import sync_playwright
from PIL import Image

out_dir = "screenshots"
shutil.rmtree(out_dir, ignore_errors=True)
os.makedirs(out_dir, exist_ok=True)


with open("data.txt", "r") as f:
    urls = f.readlines()

print("fetching images")
with sync_playwright() as p:
    browser = p.firefox.launch()
    for x in urls:
        url = x.strip()
        name = f'{x.strip()[:-1].split("/")[-1]}.png'
        f_name = os.path.join(out_dir, name)
        print(f"saving screenshot from {url} as {f_name}")
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.goto(url)
        page.screenshot(path=f_name)
    browser.close()

files = glob.glob(f"{out_dir}/*.png")
print(f"compressing {len(files)} images")

for x in files:
    with Image.open(x) as my_image:
        image_height = my_image.height
        image_width = my_image.width
        print(
            "The original size of Image is: ",
            round(len(my_image.fp.read()) / 1024, 2),
            "KB",
        )
        my_image = my_image.resize((image_width, image_height), Image.NEAREST)
        my_image.save(x)

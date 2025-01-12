from PIL import Image
from glob import glob
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 933120000
imgs = glob("imgs/*.png")
conv = glob("imgs_conv/*")
for c in conv:
    img = c.replace("imgs_conv", "imgs")
    imgs.remove(img)

print(imgs)
# exit()
for i in imgs:
    print(i)
    img_path = i
    img = Image.open(img_path)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img.save(i.replace("imgs","imgs_conv"), optimize=True)
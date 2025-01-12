from cairosvg import svg2png

svg_code = """
    <svg height="30" width="200" xmlns="http://www.w3.org/2000/svg">
  <text x="5" y="30" fill="red">I love SVG!</text>
</svg>
"""

svg2png(bytestring=svg_code,write_to='output.png')
from PIL import Image, ImageTk
Image.open(svg_code)
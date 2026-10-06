"""export_pptx.py
Exports a matplotlib Figure onto a single PowerPoint slide (A4 landscape).
"""
import io
from pptx import Presentation
from pptx.util import Cm


def export_to_pptx(fig, save_path: str):
    img_stream = io.BytesIO()
    fig.savefig(img_stream, format="png", dpi=150, bbox_inches="tight")
    img_stream.seek(0)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(33.87), Cm(19.05)  # A4 landscape
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    slide.shapes.add_picture(img_stream, Cm(1.0), Cm(1.0), width=Cm(31.87), height=Cm(17.05))
    prs.save(save_path)

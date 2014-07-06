from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from impress import SLIDE_DELIMITER


class Slide:
    def __init__(self, content, num=None):
        self.content = content
        self.num = num

    def as_html(self):
        return markdown(self.content)

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<Slide {}>'.format(self.num)


def split_slides(content, delimiter=SLIDE_DELIMITER, strip=True):
    split = delimiter.split(content)
    slides = []

    for num, slide in enumerate(split, start=1):
        slide = slide.strip() if strip else slide
        slides.append(Slide(slide, num=num))

    return slides


def render(slides, template_dir='template', **kwargs):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('presentation.html')

    # TODO: add some config object with settings like transition duration with defaults, overridable from kwargs
    template_vars = {
        'slides': slides,
        'num_slides': len(slides),
    }
    template_vars.update(kwargs)

    return template.render(**template_vars)

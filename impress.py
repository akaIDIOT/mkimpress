import argparse
import re

from jinja2 import Environment, FileSystemLoader
from markdown import markdown


class Slide:
    def __init__(self, content, num=None):
        self.content = content
        self.num = num

    @property
    def html(self):
        return markdown(self.content, extensions=[
            'extra',
            'codehilite'
        ])

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<Slide {}>'.format(self.num)


def split_slides(content, delimiter=re.compile(r'(?:\r?\n){3,}'), strip=True):
    split = delimiter.split(content)
    slides = []

    for num, slide in enumerate(split, start=1):
        slide = slide.strip() if strip else slide
        slides.append(Slide(slide, num=num))

    return slides


def render(slides, template_dir='template', **kwargs):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('index.html')

    # TODO: add some config object with settings like transition duration with defaults, overridable from kwargs
    template_vars = {
        'slides': slides,
        'num_slides': len(slides),
    }
    template_vars.update(kwargs)

    return template.render(**template_vars)


def make(infile, outfile, template_dir='template'):
    with open(infile, 'rt') as infile:
        content = infile.read()

    slides = split_slides(content)
    slides = render(slides, template_dir=template_dir)

    with open(outfile, 'wt') as outfile:
        outfile.write(slides)


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', metavar='INFILE')
    parser.add_argument('outfile', metavar='OUTFILE')

    parser.add_argument('-t', '--template-dir', default='template')

    args = parser.parse_args(args)

    make(args.infile, args.outfile, template_dir=args.template_dir)


if __name__ == '__main__':
    main()
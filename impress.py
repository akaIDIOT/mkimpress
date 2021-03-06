import argparse
import json
from os import path
import re

import fs
from jinja2 import Environment
from jinja2_fsloader import FSLoader
from markdown import markdown


class Template:
    @classmethod
    def create(cls, source):
        if path.isfile(source):
            source = f'zip://{source}'

        return cls(fs.open_fs(source))

    def __init__(self, source_fs):
        self._source_fs = source_fs
        with source_fs.open('template.json') as meta:
            self._meta = json.load(meta)
        self._env = Environment(loader=FSLoader(self._source_fs))

    def render(self, slides, **kwargs):
        template_vars = {
            'slides': slides,
            'num_slides': len(slides),
        }
        template_vars.update(kwargs)

        template = self._env.get_template(self._meta['template'])
        # TODO: copy patterns defined in template file when, to where?

        return template.render(**template_vars)


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


def split_slides(content, delimiter=re.compile(r'(?:\r?\n){4,}'), strip=True):
    split = delimiter.split(content)
    slides = []

    for num, slide in enumerate(split, start=1):
        slide = slide.strip() if strip else slide
        slides.append(Slide(slide, num=num))

    return slides


def make(infile, outfile, template, **kwargs):
    template = Template.create(template)

    with open(infile, 'rt') as infile:
        slides = split_slides(infile.read())
    slides = template.render(slides, **kwargs)

    with open(outfile, 'wt') as outfile:
        outfile.write(slides)


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', metavar='INFILE')
    parser.add_argument('outfile', metavar='OUTFILE')

    parser.add_argument('--template', default='template')
    parser.add_argument('--title', default='Presentation')

    args = parser.parse_args(args)

    make(args.infile, args.outfile, template=args.template, title=args.title)


if __name__ == '__main__':
    main()

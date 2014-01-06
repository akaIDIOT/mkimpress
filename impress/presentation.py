from impress import SLIDE_DELIMITER


class Slide:
    def __init__(self, content, num=None):
        self.content = content
        self.num = num

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
"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame


def draw_speech_arrow(display, fix_point, rect, bg_color='white', outline_color='black', width=50):
    try:
        p1, p2, p3 = get_speech_arrow_points(fix_point, rect, width)
        pygame.draw.polygon(display, bg_color, (p1, p2, p3))
        pygame.draw.polygon(display, outline_color, (p1, p2, p3), 3)
        pygame.draw.line(display, bg_color, p2, p3, 3)
    except TypeError:
        return


def get_speech_arrow_points(fix_point, rect, width):
    p1, p2, p3 = fix_point, 0, 0
    if rect.top > p1[1]:
        if rect.left > p1[0]:
            p2 = rect.topleft
            p3 = p2[0] + width, p2[1]
        elif rect.right < p1[0]:
            p2 = rect.topright
            p3 = p2[0] - width, p2[1]
        else:
            p2 = rect.centerx - width / 2, rect.top
            p3 = rect.centerx + width / 2, rect.top
    elif rect.bottom < p1[1]:
        if rect.left > p1[0]:
            p2 = rect.bottomleft
            p3 = p2[0] + width, p2[1]
        elif rect.right < p1[0]:
            p2 = rect.bottomright
            p3 = p2[0] - width, p2[1]
        else:
            p2 = rect.centerx - width / 2, rect.bottom
            p3 = rect.centerx + width / 2, rect.bottom
    else:
        if rect.left > p1[0]:
            p2 = rect.left, rect.centery - width / 2
            p3 = rect.left, rect.centery + width / 2
        elif rect.right < p1[0]:
            p2 = rect.right, rect.centery - width / 2
            p3 = rect.right, rect.centery + width / 2
        else:
            return False
    return p1, p2, p3


class Box(pygame.sprite.Sprite):
    def __init__(self,
                 lines=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 width=0,
                 text_color='white',
                 text_size=32,
                 text_aa=True,
                 text_align='left',
                 font_path=None,
                 bg_color='darkblue',
                 offset=6,
                 spaccing=2,
                 border_radius=-1,
                 outline=0,
                 outline_color='white',
                 typing_vel=1,
                 on_end=lambda: None):
        super().__init__()

        # properties
        self.lines = pygame.sprite.Group()
        self.bg_color = bg_color
        self.offset = offset
        self.outline_width = 1
        self.outline_color = bg_color
        self.border_r = border_radius

        # default box
        text_dict = {'text_color': text_color,
                     'text_size': text_size,
                     'text_aa': text_aa,
                     'font_path': font_path,
                     'bg_color': bg_color,
                     'vel': typing_vel,
                     'offset': 0}

        # lines
        last_line = None
        last_bottom = offset
        for i in range(len(lines)):
            if i == 0:
                line = TypingText(text=lines[i], **text_dict)
            else:
                line = TypingText(text=lines[i], start_at_init=False, **text_dict)
                last_line.on_end = line.start
                if i == len(lines) - 1:
                    line.on_end = on_end
            last_line = line
            line.rect.topleft = offset, last_bottom
            last_bottom = line.rect.bottom + spaccing
            self.lines.add(line)

        # gets surf width
        if not width:
            for line in self.lines:
                width = line.rect.w if line.rect.w > width else width
            width += 2 * offset

        # gets surf height
        height = self.lines.sprites()[-1].rect.bottom - self.lines.sprites()[0].rect.top + 2 * offset

        # image'n'rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # align
        for line in self.lines:
            match text_align:
                case 'right':
                    line.rect.right = self.rect.w - offset
                case 'center':
                    line.rect.centerx = round(self.rect.w / 2)

        # outline
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

    def set_on_end(self, new_function):
        self.lines.sprites()[-1].on_end = new_function

    def update(self):
        rect = pygame.Rect([0, 0, *self.rect.size])
        pygame.draw.rect(self.image, self.bg_color, rect, border_radius=self.border_r)
        pygame.draw.rect(self.image, self.outline_color, rect, self.outline_width, border_radius=self.border_r)
        self.lines.update()
        self.lines.draw(self.image)


class NameBox(pygame.sprite.Sprite):
    def __init__(self,
                 lines=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 width=0,
                 text_color='white',
                 text_size=32,
                 text_aa=True,
                 text_align='left',
                 font_path=None,
                 bg_color='darkblue',
                 name='',
                 name_color='white',
                 name_size='match',
                 name_bg_color='blue',
                 name_pos='left',
                 name_font_path: int = 'match',
                 offset=6,
                 name_offset=4,
                 spaccing=2,
                 border_radius=-1,
                 outline=0,
                 outline_color='white',
                 typing_vel=1):
        super().__init__()

        self.group = pygame.sprite.Group()

        # name
        name_height = 0
        if name:
            if name_font_path == 'match':
                name_font_path = font_path
            if name_size == 'match':
                name_size = text_size
            name = TypingText(text=name,
                              text_color=name_color,
                              text_size=name_size,
                              font_path=name_font_path,
                              bg_color=name_bg_color,
                              offset=name_offset,
                              finish_at_init=True)
            name_height = name.rect.h
            self.group.add(name)

        # box
        box = Box(lines,
                  width,
                  text_color,
                  text_size,
                  text_aa,
                  text_align,
                  font_path,
                  bg_color,
                  offset,
                  spaccing,
                  border_radius,
                  outline,
                  outline_color,
                  typing_vel)

        box.rect.top = name_height
        self.group.add(box)

        # name exists
        if name_height > 0:
            width = box.rect.w if box.rect.w > name.rect.w else name.rect.w
            box.rect.top = name.rect.bottom
            # name positioning
            match name_pos:
                case 'right':
                    name.rect.right = width
                case 'center':
                    name.rect.centerx = round(width / 2)
            #
        else:
            width = box.rect.w

        self.image = pygame.Surface((width, box.rect.height + name_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        self.group.update()
        self.group.draw(self.image)


class TypingText(pygame.sprite.Sprite):
    def __init__(self,
                 text="I'm an Animated Text!",
                 text_color='white',
                 text_size=32,
                 text_aa=True,
                 font_path=None,
                 bg_color='black',
                 offset=10,
                 vel=1,
                 outline=0,
                 outline_color='white',
                 start_at_init=True,
                 finish_at_init=False,
                 on_end=lambda: None
                 ):
        super().__init__()

        # font
        try:
            self.font = pygame.font.Font(font_path, text_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, text_size)

        # properties
        self.text = list(text)
        self.offset = offset
        self.frame = 0
        self.frame_counter = 0
        self.vel = 1/vel * 2
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_aa = text_aa
        self.outline_width = 1
        self.outline_color = bg_color
        self.on_end = on_end

        # get text size
        text = self.font.render(''.join(self.text), self.text_aa, 'black')

        # image'n'rect
        self.image = pygame.Surface(
            (text.get_width() + 2 * self.offset, text.get_height() + 2 * self.offset))
        self.rect = self.image.get_rect()

        # outline setup
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

        # initial state managment
        if finish_at_init:
            self.finish()
        elif start_at_init:
            self.start()

    def start(self):
        self.frame_counter = 1

    def finish(self):
        self.frame = len(self.text) * self.vel

    def end(self):
        self.on_end()
        self.on_end = lambda: None

    def update(self):
        self.image.fill(self.bg_color)
        if self.frame < len(self.text) * self.vel:
            text = self.font.render(
                ''.join(self.text[:round(self.frame/self.vel)]), self.text_aa, self.text_color, self.bg_color)
            self.frame += self.frame_counter
        else:
            self.end()
            text = self.font.render(
                ''.join(self.text), self.text_aa, self.text_color, self.bg_color)
        self.image.blit(text, 2 * [self.offset])
        pygame.draw.rect(self.image, self.outline_color, [0, 0, *self.image.get_size()], self.outline_width)

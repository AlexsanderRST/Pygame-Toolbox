"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

from pygame.locals import *

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
        self.on_end = on_end
        self.ended = False

        # default box
        text_dict = {'text_color': text_color,
                     'text_size': text_size,
                     'text_aa': text_aa,
                     'font_path': font_path,
                     'bg_color': bg_color,
                     'vel': typing_vel,
                     'offset': 0}

        # dialog lines sprites
        last_line = None
        last_bottom = offset
        for i in range(len(lines)):
            if i == 0:
                line = TypingText(text=lines[i], **text_dict)
            else:
                line = TypingText(text=lines[i], start_at_init=False, **text_dict)
                last_line.on_end = line.start
            last_line = line
            line.rect.topleft = offset, last_bottom
            last_bottom = line.rect.bottom + spaccing
            self.lines.add(line)

        # set on end function at last sprite
        self.set_on_end(on_end)

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

    def call_on_end(self, on_end):
        self.ended = True
        on_end()

    def end(self):
        for line in self.lines:
            line.finish()

    def set_on_end(self, new_function):
        self.lines.sprites()[-1].set_on_end(lambda: self.call_on_end(new_function))

    def update(self):
        rect = pygame.Rect([0, 0, *self.rect.size])
        pygame.draw.rect(self.image, self.bg_color, rect, border_radius=self.border_r)
        pygame.draw.rect(self.image, self.outline_color, rect, self.outline_width, border_radius=self.border_r)
        self.lines.update()
        self.lines.draw(self.image)


class Manager(pygame.sprite.GroupSingle):
    def __init__(self,
                 dialogs: list = None,
                 on_end=lambda: None,
                 end_at_last_dialog=True):
        super().__init__()

        # warning dialog when dialogs is None
        if dialogs is None:
            dialogs = [Box(lines=['No dialogs inserted'])]

        # properties
        self.dialogs = dialogs
        self.current_dialog = 0
        self.add(self.dialogs[self.current_dialog])
        self.on_end = on_end
        self.ended = False

        # the on_end function will be called at last dialog's end
        if end_at_last_dialog:
            self.dialogs[-1].set_on_end(on_end)

    def next_dialog(self):
        if self.current_dialog + 1 >= len(self.dialogs):
            self.on_end()
            self.ended = True
        else:
            self.current_dialog += 1
            self.add(self.dialogs[self.current_dialog])

    def update(self, events):
        current_dialog = self.sprite
        for event in events:
            if event.type == MOUSEBUTTONUP and not self.ended:
                if current_dialog.ended:
                    self.next_dialog()
                else:
                    current_dialog.end()
        super().update()


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
                 width=0,
                 text="I'm an Animated Text!",
                 text_color='white',
                 text_size=32,
                 text_aa=True,
                 text_align='left',
                 font_path=None,
                 bg_color='black',
                 offset=10,
                 vel=1,
                 outline=0,
                 outline_color='white',
                 start_at_init=True,
                 finish_at_init=False,
                 on_end=lambda: None):
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
        self.ended = False

        # generic text surf and rect
        text_surf = self.font.render(text, text_aa, text_color)
        self.text_rect = text_surf.get_rect()

        # get text size
        text_w, text_h = self.font.size(text)

        # get surf width
        if not width:
            width = text_w + 2 * offset
        height = text_h + 2 * offset

        # image'n'rect
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

        # align
        match text_align:
            case 'center':
                self.text_rect.center = width / 2, height / 2
            case 'right':
                self.text_rect.midright = width - offset, height / 2
            case _:
                self.text_rect.midleft = offset, height / 2

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

    def set_on_end(self, on_end):
        self.on_end = on_end

    def finish(self):
        self.frame = len(self.text) * self.vel
        self.end()

    def end(self):
        self.on_end()
        self.ended = True
        self.on_end = lambda: None

    def update(self):
        self.image.fill(self.bg_color)
        if self.frame < len(self.text) * self.vel:
            text = self.font.render(
                ''.join(self.text[:round(self.frame/self.vel)]), self.text_aa, self.text_color, self.bg_color)
            self.frame += self.frame_counter
        else:
            self.end()
            text = self.font.render(''.join(self.text), self.text_aa, self.text_color, self.bg_color)
        self.image.blit(text, self.text_rect)
        pygame.draw.rect(self.image, self.outline_color, [0, 0, *self.image.get_size()], self.outline_width)

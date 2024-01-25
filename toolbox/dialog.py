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
                 *_,
                 bg_color='darkblue',
                 font_path=None,
                 on_end=lambda: None,
                 outline=0,
                 outline_color='white',
                 padx=10,
                 pady=20,
                 roundness=-1,
                 size_hint=(0., 0.),
                 spacing=10,
                 text_aa=True,
                 text_align='left',
                 text_color='white',
                 text_size=32,
                 transparency=50,
                 typing_vel=1.,
                 width=0,
                 ):
        super().__init__()

        # properties
        self.bg_color = bg_color
        self.ended = False
        self.lines = pygame.sprite.Group()
        self.on_end = on_end
        self.outline_width = 1
        self.outline_color = bg_color
        self.roundness = roundness
        self.transparency = transparency

        # get the screen size
        screen_size = pygame.display.get_window_size()

        # default text params
        text_dict = {'text_color': text_color, 'text_size': text_size, 'text_aa': text_aa,
                     'font_path': font_path, 'vel': typing_vel, 'offset': 0}

        # dialog lines sprites
        last_line = None
        last_bottom = pady
        for i in range(len(lines)):
            if i == 0:
                line = TypingText(text=lines[i], **text_dict)
            else:
                line = TypingText(text=lines[i], start_at_init=False, **text_dict)
                last_line.on_end = line.start
            last_line = line
            line.rect.topleft = padx, last_bottom
            last_bottom = line.rect.bottom + spacing
            self.lines.add(line)

        # set the 'on_end' function at the last sprite
        self.set_on_end(on_end)

        # get the box width
        if size_hint[0]:
            width = size_hint[0] * screen_size[0]
        elif not width:
            for line in self.lines:
                width = line.rect.w if line.rect.w > width else width
            width += 2 * padx

        # get the box height
        if size_hint[1]:
            height = size_hint[1] * screen_size[1]
        else:
            height = self.lines.sprites()[-1].rect.bottom - self.lines.sprites()[0].rect.top + 2 * pady

        # set the image and rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # set the align
        for line in self.lines:
            match text_align:
                case 'right':
                    line.rect.right = self.rect.w - padx
                case 'center':
                    line.rect.centerx = round(self.rect.w / 2)

        # set the outline
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

    def update_surf(self):

        # redraw image
        self.image = pygame.Surface(self.image.get_size(), SRCALPHA)

        # redraw the box
        box_rect = pygame.Rect([0, 0, *self.rect.size])
        box_surf = pygame.Surface(box_rect.size, SRCALPHA)
        pygame.draw.rect(box_surf, self.bg_color, box_rect, border_radius=self.roundness)
        box_surf.set_alpha(round(255 * self.transparency / 100))
        self.image.blit(box_surf, (0, 0))

        # draw the ouline
        pygame.draw.rect(self.image, self.outline_color, box_rect, self.outline_width, border_radius=self.roundness)

        # redraw the text lines
        self.lines.draw(self.image)

    def update(self):
        self.lines.update()
        self.update_surf()


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


class NamedBox(pygame.sprite.Sprite):
    def __init__(self,
                 lines=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 name='Alexsander',
                 *_,
                 bg_color='#fbfcfa',
                 font_path=None,
                 name_bg_color='blue',
                 name_color='white',
                 name_font_path='match',
                 name_padx=15,
                 name_pady=7,
                 name_pos='left',
                 name_roundness=0,
                 name_size='match',
                 name_spacing=0,
                 name_transparency=100,
                 outline=2,
                 outline_color='#373737',
                 padx=10,
                 pady=20,
                 roundness=-1,
                 size_hint=(0., 0.),
                 spacing=4,
                 text_aa=True,
                 text_align='left',
                 text_color='black',
                 text_size=42,
                 trasparency=100,
                 typing_vel=.72,
                 width=0,
                 ):
        super().__init__()

        self.group = pygame.sprite.Group()

        # get the screen size
        screen_size = pygame.display.get_window_size()

        # set the width
        if size_hint[0]:
            width = screen_size[0] * size_hint[0]
        elif not width and not name:
            width = screen_size[0] * .8

        # set the boxes style
        boxes_style = {'outline': outline, 'outline_color': outline_color}

        # box
        box = Box(lines=lines, bg_color=bg_color, font_path=font_path, padx=padx, pady=pady,
                  roundness=roundness, size_hint=size_hint, spacing=spacing, text_aa=text_aa, text_align=text_align,
                  text_color=text_color, text_size=text_size, transparency=trasparency, typing_vel=typing_vel,
                  width=width, **boxes_style)
        self.group.add(box)

        # name
        if name:
            if name_font_path == 'match':
                name_font_path = font_path
            if name_size == 'match':
                name_size = text_size
            name_box = Box(lines=[name], bg_color=name_bg_color, font_path=name_font_path,
                           padx=name_padx, pady=name_pady, roundness=name_roundness,
                           text_color=name_color, text_size=name_size, transparency=name_transparency,
                           **boxes_style)
            self.group.add(name_box)
            width = box.rect.w if box.rect.w > name_box.rect.w else name_box.rect.w
            box.rect.top = name_box.rect.bottom + name_spacing
            match name_pos:
                case 'center':
                    name_box.rect.centerx = round(width / 2)
                case 'right':
                    name_box.rect.right = width

        # set image and rect
        self.image = pygame.Surface((width, box.rect.bottom), SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        self.group.update()
        self.image = pygame.Surface(self.image.get_size(), SRCALPHA)
        self.group.draw(self.image)


class RPGM(NamedBox):
    def __init__(self,
                 lines=('Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5'),
                 name='Alex',
                 portrait_surf: pygame.Surface = None,
                 *_,
                 bg_color='blue',
                 box_style='default',
                 portrait_pos='left',
                 position='bottom',
                 ):

        # properties
        text_color = 'white'
        ouline_color = 'white'
        size_hint = (.9, 0.35)

        # get the screen size
        screen_size = pygame.display.get_window_size()

        # get the box height
        box_w, box_h = screen_size[0] * size_hint[0], screen_size[1] * size_hint[1]

        # get the portrait size
        portrait_h = box_h * .8

        # get the padx
        padx = box_h * .1 if portrait_pos == 'right' else portrait_h + box_h * .2

        # set the dialog's end arrow
        self.arrow = pygame.sprite.Sprite()
        arrow_h = box_h * .04
        self.arrow.image = pygame.Surface(2 * [arrow_h], SRCALPHA)
        pygame.draw.polygon(self.arrow.image, 'white', ((0, 0), (arrow_h / 2, arrow_h), (arrow_h, 0)))

        # get style
        style = {}
        match box_style:
            case 'dim':
                style['outline'], style['roundness'], style['bg_color'], style['trasparency'] = 0, 0, 'black', 80
                style['name_bg_color'], style['name_transparency'] = 'black', 80
            case 'transparent':
                style['outline'], style['trasparency'] = -1, 0
            case _:
                style['outline'], style['roundness'], style['bg_color'], style['trasparency'] = 2, 12, bg_color, 100

        # call super
        super().__init__(lines=lines, name=name, name_spacing=5, outline_color=ouline_color, padx=padx,
                         size_hint=size_hint, text_color=text_color, **style)

        # get the portrait position
        portrait_bottom = self.rect.height - box_h * .1
        portrait_pos = {'bottomleft': (box_h * .1, portrait_bottom)} if portrait_pos != 'right' else \
            {'bottomright': (box_w - box_h * .1, portrait_bottom)}

        # set the portrait
        self.portrait = pygame.sprite.Sprite()
        if portrait_surf is not None:
            self.portrait.image = pygame.transform.smoothscale(portrait_surf, 2 * [portrait_h])
        else:
            self.portrait.image = pygame.Surface(2 * [portrait_h])
            self.portrait.image.fill('red')
        self.portrait.rect = self.portrait.image.get_rect(**portrait_pos)

        # set up the position
        match position:
            case 'top':
                self.rect.midtop = screen_size[0] / 2, screen_size[1] * .05
            case 'center':
                self.rect.center = screen_size[0] / 2, screen_size[1] / 2
            case _:
                self.rect.midbottom = screen_size[0] / 2, screen_size[1] * .95

        # positionating the arrow
        self.arrow.rect = self.arrow.image.get_rect(midbottom=(box_w / 2, box_h * .95))

        # add the portrait to group
        self.group.add(self.portrait)


class TypingText(pygame.sprite.Sprite):
    def __init__(self,
                 text="I'm an Animated Text!",
                 *_,
                 finish_at_init=False,
                 font_path=None,
                 offset=10,
                 on_end=lambda: None,
                 outline=0,
                 outline_color='white',
                 start_at_init=True,
                 text_aa=True,
                 text_align='left',
                 text_color='white',
                 text_size=32,
                 vel=1,
                 width=0,
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
        self.vel = 1 / vel * 2
        self.text_info = [text_aa, text_color]
        self.outline_width = 1
        self.on_end = on_end
        self.ended = False
        self.update = self.typing_anim

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

    def end(self):
        self.on_end()
        self.on_end = lambda: None
        self.update = lambda: None
        self.ended = True

    def finish(self):
        self.frame = len(self.text) * self.vel
        self.typing_anim()
        self.end()

    def set_on_end(self, on_end):
        self.on_end = on_end

    def start(self):
        self.frame_counter = 1

    def typing_anim(self):
        if self.frame > len(self.text) * self.vel:
            self.end()
        else:
            self.image = pygame.Surface(self.image.get_size(), SRCALPHA)
            text = self.font.render(''.join(self.text[:round(self.frame / self.vel)]), *self.text_info)
            self.image.blit(text, self.text_rect)
            self.frame += self.frame_counter

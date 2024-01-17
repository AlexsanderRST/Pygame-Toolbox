![](https://i.ibb.co/Y2JJKm2/01.png)

# Slide Bar

You might be familiar with a slide bar when you adjust the volume on your phone, for example. In your game, you can use it to adjust 
the sound volume. The idea is simple: a **bar** and an interactive **slider**. The position of the slider in relation
to the width (or height if vertical) is returned as a _float_ **value**. For example, if the slider is in the middle of the
bar (50% of the width), the returned value will be about _0.5_. Now let's look at the parameters, attributes, methods and 
some examples:

## Parameters

### pos

A _dict_ that specifies the origin of the rect. You can type _{'center': (screen_w * .5, screen_h * 0.5)}_ to position the
bar in the center of the screen. ⚠️ For now, the group's rect is a small invisible square, and the bar's center is based on its
center, limiting positioning to the center.

### vertical

A _bool_ that indicates the orientation of the bar. 

### inverted_value

It is mainly used on vertical sliders. _(1 - value)_ is returned instead of _value_.

### bar_surf

You can specify a custom _pygame.Surface_. In this case the size will be taken from the surface (it will not be resized). 
Other parameters like roudness, color, outline; will be ignored.

### bar_w & bar_h

The width and height of the bar. It overrides bar_hint_w and bar_hint_h. It won't be taken into account if you enter a
bar_surf.

### bar_hint_w & bar_hint_h

The width and height of the bar are related to the screen size. Examples: if a bar has bar_hint_w=.5 and a screen width=1280,
the bar width will be 640 pixels.

### bar_roundness

![](https://i.ibb.co/gFwyjC6/imagem-2024-01-13-125105696.png)

### bar_outline

![](https://i.ibb.co/1QcDN1f/02.png)

### bar_color

You can enter a **hex** _string_ or a **rgb** _tuple_ (or any **named color** _string_ supported by pygame). For example,
the default bar color is the named color 'gray', but it can also be represented by _'#bebebe'_ or _(190, 190, 190)_.
The same is true for other color parameters.

### bar_outline_color

### slider_surf

### slider_w & slider_h

### slider_shape

For now, only the square and circle shapes are suported.

![](https://i.ibb.co/18TyT1W/05.png)

### slider_outline

![](https://i.ibb.co/f1Y1j5Z/04.png)

### slider_color

### slider_color_outline

## Attributes

- For bars: image & rect (sprites), roundness, outline, color, color_outline and surf.
- For sliders: image & rect (sprites), shape, outline, color, color_outline and surf.

## Methods

### set_bar_style

You can call this method to apply the changes made to the bar's attributes. See Example 1.

### set_slider_style

You can call this method to apply changes made to the slider's attributes. See Example 2.

### slider_hovered

Returns when the mouse hovers over the slider. This is useful for a context cursor, for example.

## Examples

### Example 1: Color Maker

![](https://i.ibb.co/rtLCYrg/06.png)

### Example 2: Happiness Bar

![](https://i.ibb.co/2YBycv3/imagem-2024-01-17-100519895.png)

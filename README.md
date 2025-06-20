# <ins>typedecker's Flet Utility Repository</ins>

This repo consists of a bunch of useful utility code that I developed over my time working with flet, for ease of use. Some of it's contents include:
1. A `ResponsiveLayer` class that lets you add responsiveness to your apps. The controls resize automatically, as long as they are used as instructed in the [`ResponsiveLayer` section](https://github.com/typedecker/custom_flet_utils/edit/main/README.md#1-responsivelayer-docs) given below.
2. A custom control that allows for Absolute Positioning of widgets. It is pretty easy to understand and use, for more information you can [check out the section](https://github.com/typedecker/custom_flet_utils/edit/main/README.md#2-positioned-control-docs) for it down below as well.

---
<a name="responsive-layer-section"></a>
### 1.) `ResponsiveLayer` Docs
The responsive layer class allows users to add responsiveness to their flet apps, by allowing them to use features such as fractional, padded, relative and percentage based parameters. It can be used to automatically resize the controls, depending on the dimensions of the device itself.

To start working with it, you must initialize an object of this class, the constructor takes the `page` itself as it's first parameter, and the other two parameters are `BASE_WIDTH` and `BASE_HEIGHT`; These two are supposed to represent the dimensions of the window that you wanna code with respect to. This allows you to mention all the other widths and heights in your code whilst assuming that your window will always be `BASE_WIDTH x BASE_HEIGHT`, and the responsive layer object will automatically calculate the respective values for other window sizes as and when required! The second and third parameters are completely optional and default to values of `800` and `600` respectively.

```py
# I've passed the second and third parameter here to demonstrate their usage,
# you need not pass them if you like the default values.
rl: ResponsiveLayer = ResponsiveLayer(page, 800, 600)
```

Once you have your `rl` object initialized -- The next step is to define a separate `draw_page()` function. This function will allow us to redraw everything if the window were to be resized, and also help with the segregation of the UI code from the rest of the setup code around it. Within the `draw_page()` function, we shall clear the currently present controls off of the `page.controls` list, and redraw them. For the example below, I'll be using a dummy container which will be drawn with a <ins>relative width</ins> of `200` with respect to a base window width of `800`; i.e. It will be `200` pixels wide for a window with a width of `800`, for other window widths it'll be automatically resized:

```py
# You can also choose to fetch the page off of the rl object, but im not sure if it is reliable.
def draw_page(page: ft.Page, rl: ResponsiveLayer) -> None :
  page.controls.clear()

  example_container: ft.Container = ft.Container(
    ft.Text('Test container'),
    
    width = rl.rw(200), # rw here stands for relative-width
    height = rl.rh(200), # rh stands for relative-height
    
    # rl also provides responsive margin and padding parameters
    margin = rl.Margin(10, 10, 10, 10),
    padding = rl.Padding(5, 5, 5, 5)
  )

  page.add(example_container)
  return
```

Once we have defined a base `draw_page()` function in our code, we can then bind the `page`'s `on_resize` event to a callback that updates `r'`'s dimensions and redraws the page accordingly.

```py
  def on_resize(e: ft.WindowResizeEvent) -> None :
    rl.update_dimensions()
    draw_page(page, rl)
    return
    
  page.on_resized = on_resize
```

## \# <ins>FAQ</ins>
Before, we go over all the available parameters for the responsive layer, I must clear out some possible concerns:
1. Isn't drawing the page everytime the window gets resized inefficient?
> Yes, it could possibly be inefficient in many ways, but the window isn't regularly resized, a user only ever resizes it once or twice, but this code has been stress tested and does well even with really large UI compositions and continous resizing. <ins>Keep in mind that the resizing only takes place after your mouse button is released.</ins>
2. The UI isn't resizing as I'd like it to, it keeps going out of screen for really small window sizes!
> There is a limit to how much the resizing can do for you. The responsiveness works well for most modern and even pretty moderately old device resolutions. I would still not recommend using this for dimensions that are super small and not practically viable. It is natural and expected that it'd break under such circumstances, if you face issues over a more moderate resolution, feel free to post an issue and I'll take a look!
3. My app supports both smartphone and desktop, but I am having trouble keeping it responsive.
> This responsiveness-upon-resize part of this utility kit has been made solely for apps that can be resized within their devices. The utility kit works cross platform though and can be used with major success even for android and ios devices. But I'd suggest defining a combined draw function that calls two separate draw functions based on the platforms used. I've used this in my apps with success.
4. Does this work with views? and what about classes?
> Yes, it does work with views and classes both. I'll provide a code example for the same underneath at the very end of this section if you'd like to work alongside them! And, for classes you can simply just define the draw function within it, and call it from within as well, everything else remains the same.
5. This makes it impossible to retain data in the UI! On resizing all the data goes poof!
> I am aware of this issue, and there is a very simple and easy fix for this! You can maintain all the data you need to keep track of in a dictionary/list, and pass it as a third parameter/argument to the `draw_page()` function. You can then use the data dictionary to load back the values for every single part of the UI as per your wish. The data will then be retained over resize attempts. Is this inefficient? Yes, probably. But that does not make this project or the utility kit irrelevant, its focused on creativity and usability, not efficiency, but if you have a better idea for this, I'd love to hear it out! Please be positive and constructive with your interactions though.
6. How do I decide the window's width and height with respect to the dimensions of the device itself?
> I'll be answering this whilst keeping in mind that this is only applicable for Windows, Mac and Linux. You can use an external third party python module called `pyautogui` to get the size of the screen. A small sample program is provided below.
> ```py
> import pyautogui
> 
> # ...
>
> def main(ft.Page) :
>   EXPECTED_SCREEN_WIDTH, EXPECTED_SCREEN_HEIGHT = 2560, 1600
>   DESIRED_WINDOW_WIDTH, DESIRED_WINDOW_HEIGHT = 1000, 850
>   
>   rl: ResponsiveLayer = ResponsiveLayer()
>   
>   if not (page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS, ft.PagePlatform.ANDROID_TV]) :
>     DETECTED_SCREEN_WIDTH, DETECTED_SCREEN_HEIGHT = pyautogui.size()
>   
>     # Update the window's width and height to the relatively-equivalent parameters for the detected device resolution.
>     page.window.width = (DESIRED_WINDOW_WIDTH) * (DETECTED_SCREEN_WIDTH / EXPECTED_SCREEN_WIDTH)
>     page.window.height = (DESIRED_WINDOW_HEIGHT) * (DETECTED_SCREEN_HEIGHT / EXPECTED_SCREEN_HEIGHT)
>     
>     page.update()
>     rl.update_dimensions()
>      
>  def on_resize(e: ft.WindowResizeEvent) -> None :
>     rl.update_dimensions()
>     draw_page(page, rl)
>     return
>   
>  draw_page(page, rl)
>  return
> # ...
> ```

### \# Parameters
ResponsiveLayer provides a bunch of different parameter types for usage in your responsive designs:

1. <ins>**Percentage-Based Parameters**</ins>

```
rl.pw(percentage, _min = 0, width = page_width)
rl.ph(percentage, _min = 0, height = page_height)
```

* Percentage based parameters allow for the usage of percentage to define the width or height of a particular control. You can use `rl.pw` or `rl.ph` for width and height respectively.
* By default the percentages are measured with respect to the size of the page. But you can change the width and height with respect to which it calculates the percentages, by passing in width and height parameters to `rl.pw` and `rl.ph`.
* The _min parameter defines the minimum possible width or height that will be passed back to you. If you do not want your controls to resize past a certain width or height, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
example_container = ft.Container(
  ft.Text('test'),
  width = rl.pw(25, _min = 100, width = 800), # I've also passed the optional arguments to demonstrate their usage.
  height = rl.ph(33, _min = 100, height = 600) # 25% of 800 = 200; 33.33% of 600 = 200; so this follows from our original example.
)
```

2. <ins>**Fractional Parameters**</ins>

```
rl.fw(fraction, _min = 0, width = page_width)
rl.fh(fraction, _min = 0, height = page_height)
```

* Fractional parameters allow for the usage of fractions to define the width or height of a particular control. You can use `rl.fw` or `rl.fh` for width and height respectively.
* By default the fractions are measured with respect to the size of the page. But you can change the width and height with respect to which it calculates the fractions, by passing in width and height parameters to `rl.fw` and `rl.fh`.
* The _min parameter defines the minimum possible width or height that will be passed back to you. If you do not want your controls to resize past a certain width or height, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
example_container = ft.Container(
  ft.Text('test'),
  width = rl.fw(0.25, _min = 100, width = 800), # I've also passed the optional arguments to demonstrate their usage.
  height = rl.fh(0.33, _min = 100, height = 600) # 0.25 x 800 = 200; 0.33 x 600 = 200; so this follows from our original example.
)
```

3. <ins>**Padded Parameters**</ins>

```
rl.pdw(padding, _min = 0, width = page_width)
rl.pdh(padding, _min = 0, height = page_height)
```

* Padding based parameters allow for the calculation of width and height with the padding applied to it on either ends, this might allow you to make your UI's width and height calculations more easily. Nested Controls work well with this. You can use `rl.pdw` or `rl.pdh` for width and height respectively.
* By default the paddings are subtracted off from the width and height of the page. But you can change the width and height with respect to which it calculates the padded values, by passing in width and height parameters to `rl.pdw` and `rl.pdh`.
* The _min parameter defines the minimum possible width or height that will be passed back to you. If you do not want your controls to resize past a certain width or height, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
example_container = ft.Container(
  ft.Text('test'),
  width = rl.pdw(300, _min = 100, width = 800), # I've also passed the optional arguments to demonstrate their usage.
  height = rl.pdh(200, _min = 100, height = 600) # 800 - (2 x 300) = 200; 600 - (2 x 200) = 200; so this follows from our original example.
)
```

4. <ins>**Relative Parameters**</ins>

```
rl.rw(width, _min = 0, BASE_WIDTH = BASE_WIDTH)
rl.rh(height, _min = 0, BASE_HEIGHT = BASE_HEIGHT)
```

* Relative parameters allow us to define the width or height of a particular control with respect to an BASE_WIDTH and BASE_HEIGHT decided. For other window sizes, the equivalent measurements are calculated accordingly, which still give the same feeling it did with the original due to the ratios remaining the same. You can use `rl.rw` or `rl.rh` for width and height respectively.
* By default the relative width and height are calculated with respect to the BASE_WIDTH and BASE_HEIGHT parameters passed to the constructor of the `ResponsiveLayer` object. But you can change the width and height with respect to which it calculates the relative measurements, by passing in BASE_WIDTH and BASE_HEIGHT parameters to `rl.rw` and `rl.rh`.
* The _min parameter defines the minimum possible width or height that will be passed back to you. If you do not want your controls to resize past a certain width or height, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
example_container = ft.Container(
  ft.Text('test'),
  width = rl.rw(200, _min = 100, BASE_WIDTH = 800), # I've also passed the optional arguments to demonstrate their usage.
  height = rl.rh(200, _min = 100, BASE_HEIGHT = 600) # 200 wrt to 800; 200 wrt to 600; so this follows from our original example.
)
```

5. <ins>**Numerical Parameters**</ins>

```
rl.nw(n, _min = 0, BASE_WIDTH = BASE_WIDTH)
rl.nh(n, _min = 0, BASE_HEIGHT = BASE_HEIGHT)
```

* Numerical parameters allow us to define a numerical quantity that changes as per the width and height of the window. This can be used in usecases such as when mentioning the font size for a `ft.Text` control. You can use `rl.pnw` or `rl.nh` for width and height respectively.
* By default the width and height based numbers are calculated with respect to the BASE_WIDTH and BASE_HEIGHT parameters passed to the constructor of the `ResponsiveLayer` object. But you can change the width and height with respect to which it calculates the numerical measurements, by passing in BASE_WIDTH and BASE_HEIGHT parameters to `rl.nw` and `rl.nh`.
* The _min parameter defines the minimum possible number that will be passed back to you. If you do not want your number to go down past a certain limit, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
example_container = ft.Container(
  ft.Text('test', size = rl.rw(32, _min = 12, BASE_WIDTH = 800)), # Mentioned optional parameters too for ease of understanding.
  width = rl.rw(200),
  height = rl.rh(200)
)
```

6. <ins>**Relative Side Parameter**</ins>

```
rl.rs(side, _min = 0, BASE_WIDTH = BASE_WIDTH, BASE_HEIGHT = BASE_HEIGHT)
```

* Relative Side parameter allows for the calculation of a side for varying widths and heights of the window, given the BASE_WIDTH and BASE_HEIGHT. It preserves the area ratio. It is very useful in cases where the resolution/dimensions of a Control are more importantly to be preserved than the individual width and height. You can use `rl.rs` to utilize it.
* By default the relative side is calculated with respect to the BASE_WIDTH and BASE_HEIGHT parameters passed to the constructor of the `ResponsiveLayer` object. But you can change the width and height with respect to which it calculates the relative side, by passing in BASE_WIDTH and BASE_HEIGHT parameters to `rl.rs`.
* The _min parameter defines the minimum possible side that will be passed back to you. If you do not want your controls to resize past a certain size, you can pass in the value for this parameter, it is set to zero[0] by default.

e.g.
```py
# I've used optional parameters here for demonstration purposes.
# (200x200)/(800x600) is the ratio of areas, which will be conserved.
side = rl.rs(200, _min = 0, BASE_WIDTH = 800, BASE_HEIGHT = 600)
example_container = ft.Container(
  ft.Text('test'),
  width = side
  height = side
)
```

---

<a name="positioning-widget-section"></a>
### 2.) <ins>`Positioned` Control Docs</ins>

<ins>NOTE:</ins>
> This widget will work for all flet supported platforms, but the positioning is heavily dependent on the actual device resolution, the developer has the duty of ensuring that the coordinates are logical enough for the widget to be visible, if its not visible, then its most likely an error on the coordination/positioning front rather than of the control implementation itself.

`Positioned` is the name of the custom control that allows for absolute positioning of controls on the screen. It is built upon the native `ft.Stack` control from flet. It also utilizes `ft.TransparentPointer` in the backend and allows for the passing of events through it's layers of controls. It's constructor takes two major parameters: `controls` which is a list of tuples(or lists) that have the controls to be placed as their first element, and the position tuple(or list) as the second element, and `permeable` -- which is an optional parameter and defaults to True; it determines whether the events will be passed through or not.

```py
Positioned([
  [ft.TextField(multiline = True, min_lines = 20), [0, 0]],
  [ft.Button(text = 'test'), [95, 50]]
], permeable = True) # I've passed the optional parameter here to demonstrate the usage of the parameter.
```

Given below is a small demo of how it could be used:

```py
import flet as ft
from flet_utils import Positioned

def main(page: ft.Page) :
    page.window.width = 800
    page.window.height = 600
    page.window.center()
    
    page.add(
        Positioned([
            [ft.TextField(multiline = True, min_lines = 20), [0, 0]],
            [ft.Button(text = 'test'), [95, 50]]
        ])
    )


ft.app(main)
```

---

<ins>NOTE:</ins>
> Let me know if anyone who uses or views this project has any ideas for more stuff to implement, I will list some of the things I'd like to implement in the future if possible, down below here. Keep in mind that all of the code here is in pure python and if an idea requires usage of the inclusion of a third party package or, involves usage of dart then it's addition might be discouraged. The idea here is to develop things purely in flet, inefficiency isn't a huge concern as this repo is more so focused on creativity of ideas, but if you'd like to help make these widgets more efficient, you're more than welcome to help me with it! I'll review any and all issues or pull requests sent here as soon as possible! The maintenace of this for future flet versions is not guaranteed but I'll try my best to keep it up to date, if theres an urgency or need for usage of this, you can reach out to me personally via my discord: `@typedecker`.

## <ins>Future Goals: </ins>
1. Make a more customizable and useful canvas.
2. A better event system for flet.
3. A better referential system for flet.
4. Improved Multiline text field widget with more options and customization.
5. A much better, and more efficient build system [Help might be needed with this one, dm me if interested in working on this with me! I am open to taking flet build issues and fixing them on here, we can use more than just python for this specific goal]

---

## License

This code is licensed under the Creative Commons Attribution 4.0 License (CC BY 4.0).  
You're free to use or modify this project as long as you **credit the author ("typedecker")** in your app or codebase.  
[Read the full license here.](https://creativecommons.org/licenses/by/4.0/)

# For now I am gonna add them both in the same file for ease of use.
import math
import flet as ft

class ResponsiveLayer() :
    def __init__(self, page: ft.Page, BASE_WIDTH: int = 800, BASE_HEIGHT: int = 600) -> None :
        self.page: ft.Page = page
        
        self.BASE_WIDTH: int = BASE_WIDTH
        self.BASE_HEIGHT: int = BASE_HEIGHT
        
        self.update_dimensions()
        return
    
    def update_dimensions(self) -> None :
        self.page_width: int = self.page.width
        self.page_height: int = self.page.height
        
        self.width_relativity_factor: int = (0.00001 + (self.page_width / self.BASE_WIDTH))
        self.height_relativity_factor: int = (0.00001 + (self.page_height / self.BASE_HEIGHT))
        
        # percentage width, percentage height
        self.pw = lambda percentage, _min = 0, width = self.page_width: result if (result := ((percentage / 100) * width)) >= _min else _min
        self.ph = lambda percentage, _min = 0, height = self.page_height: result if (result := ((percentage / 100) * height)) >= _min else _min
        
        # fractional width, fractional height
        self.fw = lambda fraction, _min = 0, width = self.page_width: result if (result := (fraction * width)) >= _min else _min
        self.fh = lambda fraction, _min = 0, height = self.page_height: result if (result := (fraction * height)) >= _min else _min
        
        # padded parameters
        self.pdw = lambda padding, _min = 0, width = self.page_width: result if (result := (self.get_padded_dimension(width, padding))) >= _min else _min
        self.pdh = lambda padding, _min = 0, height = self.page_height: result if (result := (self.get_padded_dimension(height, padding))) >= _min else _min
        
        # relative parameters
        self.rw = lambda width, _min = 0, BASE_WIDTH = self.BASE_WIDTH: result if (result := (self.page_width * (0.00001 + (width / BASE_WIDTH)))) >= _min else _min
        self.rh = lambda height, _min = 0, BASE_HEIGHT = self.BASE_HEIGHT: result if (result := (self.page_height * (0.00001 + (height / BASE_HEIGHT)))) >= _min else _min
        
        # Responsive Padding
        self.Padding = lambda left, top, right, bottom: ft.Padding(
            self.rw(left),
            self.rh(top),
            self.rw(right),
            self.rh(bottom)
        )
        
        # Responsive Margin
        self.Margin = lambda left, top, right, bottom: ft.Padding(
            self.rw(left),
            self.rh(top),
            self.rw(right),
            self.rh(bottom)
        )
        
        # numerical conversions for horizontal and vertical layouts
        # e.g. if a grid takes 3 items within a width of 800, how much will it take for a resized window of 1200 lets say.
        self.nw = lambda n, _min = 0, BASE_WIDTH = self.BASE_WIDTH: result if (result := (math.floor((self.page_width * n) / BASE_WIDTH))) >= _min else _min
        self.nh = lambda n, _min = 0, BASE_HEIGHT = self.BASE_HEIGHT: result if (result := (math.floor((self.page_height * n) / BASE_HEIGHT))) >= _min else _min
        
        # relative-side parameter, useful for when the area needs to be preserved. 
        self.rs = lambda side, _min = 0, BASE_WIDTH = self.BASE_WIDTH, BASE_HEIGHT = self.BASE_HEIGHT: result if (result := (((((self.page_width * self.page_height) / (BASE_WIDTH * BASE_HEIGHT)) * (side ** 2)) ** 0.5))) >= _min else _min
        return
    
    def get_padded_dimension(self, dimension: int, padding: int) -> int :
        # returns any dimension with the given padding, can be useful in some cases.
        return (dimension - (2 * padding))

class Positioned(ft.Container) :
    def __init__(self, controls: list[list[ft.Control, list[int]]], permeable: bool = True, *args, **kwargs) -> None :
        super().__init__(*args, **kwargs)
        
        self._stack = ft.Stack()
        self.content = self._stack
        
        self._controls = controls
        self.permeable = permeable
        return
    
    def did_mount(self) -> None :
        self._position_controls()
        return
    
    def _position_controls(self) :
        for control, position in self._controls :
            self.add_control(control, position)
        return
    
    def add_control(self, control: ft.Control, position: list[int]) -> None :
        if self.permeable :
            control_container = ft.TransparentPointer(ft.Container(
                control,
                padding = ft.Padding(position[0], position[1], 0, 0),
                margin = ft.Margin(0, 0, 0, 0)
            ))
        else :
            control_container = ft.Container(
                control,
                padding = ft.Padding(position[0], position[1], 0, 0),
                margin = ft.Margin(0, 0, 0, 0)
            )
        
        self._stack.controls.append(control_container)
        self._stack.update()
        return

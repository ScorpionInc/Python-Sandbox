import math
import time
import random

from multipledispatch import dispatch
from point2d import Point2D
import matplotlib
import pyautogui
import win32gui
import dxcam
import keras_ocr

print("Script is initializing.")

def linear_lerp(x:float) -> float:
    #Returns a "y" value between 0.0 to 1.0 given x.
    return x
def parabolic_lerp(x:float) -> float:
    #Returns a "y" value between 0.0 to 1.0 given x.
    #Lower than linear values.
    return x * x
def root_lerp(x:float) -> float:
    #Returns a "y" value between 0.0 to 1.0 given x.
    #Higher than linear values.
    return math.sqrt(x)
def step_lerp(x:float) -> float:
    #Returns a "y" value between 0.0 to 1.0 given x.
    #Values tend toward the middle. (Stair step)
    #This formula can be more generalized as:
    #y=4^n(x-0.5)^(1+2n)+0.5 where n is a factor of 2.
    #As n approaches infinity the changes get steeper.
    #As n approaches zero the changes get flatter.
    #Here n = 1.
    return 4 * ((x - 0.5) ** 3) + 0.5

def random_weighted_value(min_value:float, max_value:float, weight_func:callable = linear_lerp) -> float:
    #Returns weighted random value between min and max float values.
    next_uniform = weight_func(random.random())#0.0->1.0
    next_uniform *= (max_value - min_value)#0.0->(max_value - min_value)
    next_uniform += min_value#(min_value)->(max_value)
    return next_uniform

@dispatch(int, int, min_time=float, max_time=float, weight_func=object, tween_mode=object)
def mouse_move(x:int, y:int, min_time:float = 0.0, max_time:float = -1.0, weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Moves mouse to screen coord(x,y) in random time.
    #Returns mouse movement duration.
    if(max_time < 0):
        max_time = min_time
    t = random_weighted_value(min_time, max_time, weight_func)
    pyautogui.moveTo(x, y, t, tween_mode)
    return t
@dispatch(Point2D, min_time=float, max_time=float, weight_func=object, tween_mode=object)
def mouse_move(screen_point:Point2D, min_time:float = 0.0, max_time:float = -1.0, weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Helper Function
    return mouse_move(round(screen_point.x), round(screen_point.y), min_time=min_time, max_time=max_time, weight_func=weight_func, tween_mode=tween_mode)

@dispatch(int, int, min_time=float, max_time=float, weight_func=object, tween_mode=object)
def lmb(x:int, y:int, min_time:float = 0.0, max_time:float = -1.0, weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Moves mouse to screen coord(x,y) and clicks with left mouse button in random time.
    #Returns mouse movement duration.
    t = mouse_move(x, y, min_time=min_time, max_time=max_time, weight_func=weight_func, tween_mode=tween_mode)
    pyautogui.click(x, y)
    return t
@dispatch(Point2D, min_time=float, max_time=float, weight_func=object, tween_mode=object)
def lmb(screen_point:Point2D, min_time:float = 0.0, max_time:float = -1.0, weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Helper Function
    return lmb(round(screen_point.x), round(screen_point.y), min_time=min_time, max_time=max_time, weight_func=weight_func, tween_mode=tween_mode)

@dispatch(Point2D, float, dist_weight_func=object, angle_weight_func=object)
def random_point_in_circle(center:Point2D, radius:float, dist_weight_func:callable = root_lerp, angle_weight_func:callable = linear_lerp) -> Point2D:
    #Returns a random point in a circle centered around x,y
    p = Point2D(r=random_weighted_value(0.0, radius, dist_weight_func), a=random_weighted_value(0.0, math.tau, angle_weight_func))
    return (p + center)
@dispatch(int, int, float, dist_weight_func=object, angle_weight_func=object)
def random_point_in_circle(center_x:int, center_y:int, radius:float, dist_weight_func:callable = root_lerp, angle_weight_func:callable = linear_lerp) -> Point2D:
    #Helper Function
    return random_point_in_circle(Point2D(center_x, center_y), radius, dist_weight_func=dist_weight_func, angle_weight_func=angle_weight_func)

@dispatch(Point2D, float, min_time=float, max_time=float, time_weight_func=object, dist_weight_func=object, angle_weight_func=object, tween_mode=object)
def lmb_point_in_circle(center:Point2D, radius:float, min_time:float = 0.0, max_time:float = -1.0, time_weight_func:callable = parabolic_lerp, dist_weight_func:callable = root_lerp, angle_weight_func:callable = linear_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Returns the time to move mouse to a random point in defined circle and clicking with the left mouse button.
    return lmb(random_point_in_circle(center, radius, dist_weight_func=dist_weight_func, angle_weight_func=angle_weight_func), min_time=min_time, max_time=max_time, weight_func=time_weight_func, tween_mode=tween_mode)
@dispatch(int, int, float, min_time=float, max_time=float, time_weight_func=object, dist_weight_func=object, angle_weight_func=object, tween_mode=object)
def lmb_point_in_circle(center_x:int, center_y:int, radius:float, min_time:float = 0.0, max_time:float = -1.0, time_weight_func:callable = parabolic_lerp, dist_weight_func:callable = root_lerp, angle_weight_func:callable = linear_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Helper Function
    return lmb_point_in_circle(Point2D(center_x, center_y), radius, min_time=min_time, max_time=max_time, time_weight_func=time_weight_func, dist_weight_func=dist_weight_func, angle_weight_func=angle_weight_func, tween_mode=tween_mode)

@dispatch(float, float, float, float, x_weight_func=object, y_weight_func=object)
def random_point_in_rect(min_x:float, min_y:float, max_x:float, max_y:float, x_weight_func:callable = linear_lerp, y_weight_func:callable = linear_lerp) -> Point2D:
    #Returns a random point within rectangle defined by parameters.
    return Point2D(random_weighted_value(min(min_x, max_x), max(min_x, max_x), x_weight_func), random_weighted_value(min(min_y, max_y), max(min_y, max_y), y_weight_func))
@dispatch(float, float, float, float, min_time=float, max_time=float, x_weight_func=object, y_weight_func=object, time_weight_func=object, tween_mode=object)
def lmb_point_in_rect(min_x:float, min_y:float, max_x:float, max_y:float, min_time:float = 0.0, max_time:float = -1.0, x_weight_func:callable = linear_lerp, y_weight_func:callable = linear_lerp, time_weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Returns the time to move mouse to a random point in defined rectangle and clicking with the left mouse button.
    return lmb(random_point_in_rect(min_x, min_y, max_x, max_y, x_weight_func=x_weight_func, y_weight_func=y_weight_func), min_time=min_time, max_time=max_time, weight_func=time_weight_func, tween_mode=tween_mode)
@dispatch(Point2D, Point2D, x_weight_func=object, y_weight_func=object)
def random_point_in_rect(point_a:Point2D, point_b:Point2D, x_weight_func:callable = linear_lerp, y_weight_func:callable = linear_lerp) -> Point2D:
    #Helper Function
    return random_point_in_rect(point_a.x, point_a.y, point_b.x, point_b.y, x_weight_func=x_weight_func, y_weight_func=y_weight_func)
@dispatch(int, int, int, int, min_time=float, max_time=float, x_weight_func=object, y_weight_func=object, time_weight_func=object, tween_mode=object)
def lmb_point_in_rect(min_x:int, min_y:int, max_x:int, max_y:int, min_time:float = 0.0, max_time:float = -1.0, x_weight_func:callable = linear_lerp, y_weight_func:callable = linear_lerp, time_weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Helper Function
    return lmb_point_in_rect(min_x * 1.0, min_y * 1.0, max_x * 1.0, max_y * 1.0, min_time=min_time, max_time=max_time, x_weight_func=x_weight_func, y_weight_func=y_weight_func, time_weight_func=time_weight_func, tween_mode=tween_mode)
@dispatch(Point2D, Point2D, min_time=float, max_time=float, x_weight_func=object, y_weight_func=object, time_weight_func=object, tween_mode=object)
def lmb_point_in_rect(point_a:Point2D, point_b:Point2D, min_time:float = 0.0, max_time:float = -1.0, x_weight_func:callable = linear_lerp, y_weight_func:callable = linear_lerp, time_weight_func:callable = parabolic_lerp, tween_mode:callable = pyautogui.easeInQuad) -> float:
    #Helper Function
    return lmb_point_in_rect(point_a.x, point_a.y, point_b.x, point_b.y, min_time=min_time, max_time=max_time, x_weight_func=x_weight_func, y_weight_func=y_weight_func, time_weight_func=time_weight_func, tween_mode=tween_mode)

@dispatch(float, float, float, float, object)
def capture_screen_region(min_x:float, min_y:float, max_x:float, max_y:float, cam:dxcam):
    #Returns image value of screen region defined by points (min_x, min_y) -> (max_x, max_y).
    return capture_screen_region(round(min_x), round(min_y), round(max_x), round(max_y), cam)
@dispatch(Point2D, Point2D, object)
def capture_screen_region(point_a:Point2D, point_b:Point2D, cam:dxcam):
    #Returns image value of screen region defined by points a -> b.
    return capture_screen_region(point_a.x, point_a.y, point_b.x, point_b.y, cam)
@dispatch(int, int, int, int, object)
def capture_screen_region(min_x:int, min_y:int, max_x:int, max_y:int, cam:dxcam):
    #Returns image value of screen region defined by points (min_x, min_y) -> (max_x, max_y).
    return cam.grab(region=(min(min_x, max_x), min(min_y, max_y), max(min_x, max_x), max(min_y, max_y)))

@dispatch(int, int, object)
def get_pixel_at(x:int, y:int, cam:dxcam) -> matplotlib.colors:
    #Returns a single pixel from screen capture.
    return capture_screen_region(x, y, x + 1, y + 1, screen)[0][0]
@dispatch(float, float, object)
def get_pixel_at(x:float, y:float, cam:dxcam) -> matplotlib.colors:
    #Helper Function
    return get_pixel_at(round(x), round(y), cam)
@dispatch(Point2D, object)
def get_pixel_at(point_a:Point2D, cam:dxcam) -> matplotlib.colors:
    #Helper Function
    return get_pixel_at(point_a.x, point_a.y, cam)

@dispatch(str)
def IsWindowMinimized(name:str) -> bool:
    #Returns true if window by name is minimized.
    #Returns false otherwise.
    window_handle = win32gui.FindWindow(None, "" + name)
    if window_handle:
        tup = win32gui.GetWindowPlacement(window_handle)
        return tup[1] == win32con.SW_SHOWMINIMIZED
    else:
        return false
@dispatch(str)
def IsWindowMaximized(name:str) -> bool:
    #Returns true if window by name is maximized.
    #Returns false otherwise.
    window_handle = win32gui.FindWindow(None, "" + name)
    if window_handle:
        tup = win32gui.GetWindowPlacement(window_handle)
        return tup[1] == win32con.SW_SHOWMAXIMIZED
    else:
        return false
@dispatch(str)
def GetWindowRectFromName(name:str) -> tuple:
    #Returns bounds of window by name.
    window_handle = win32gui.FindWindow(None, "" + name)
    return win32gui.GetWindowRect(window_handle)

screen = dxcam.create()
pipeline = keras_ocr.pipeline.Pipeline()
print("Script has started.")
#time.sleep(1.0)
#num_of_clicks = 50
#for i in range(num_of_clicks):
    #lmb_point_in_circle(500, 300, 50.0, min_time=0.1, max_time=0.2)
    #lmb_point_in_rect(400, 400, 500, 550, min_time=0.1, max_time=0.2)
#matplotlib.pyplot.style.use('_mpl-gallery-nogrid')
#matplotlib.pyplot.axis('off')
#matplotlib.pyplot.imshow(capture_screen_region(0, 0, 100, 100, screen))
#matplotlib.pyplot.show()
print( str(get_pixel_at(0, 0, screen)) )
print( GetWindowRectFromName("Notepad") )
print("Script has stopped.")

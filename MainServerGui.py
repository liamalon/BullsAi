import kivy
__author__ = "Liam Alon"
__date__ = "25/02/2022"
import os
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.text import LabelBase    
import random
from ComputerServer.UdpServer import UdpServer
from MainComputerServer import ImageDetection
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
import sys

import pygame

from pygame.locals import *

import multiprocessing

from multiprocessing import shared_memory

import subprocess

import time

SPEED: int = 5
SHOOT_BUTTON: int = 10 # R1
pygame.init()
pygame.joystick.init()

PORT: int = 8888
CODE_LEN: int = 5
STEP_SIZE: int = 1

# Load font 
LabelBase.register(name= "txt_font",
    fn_regular= "Graphics\\assets\\font.ttf")

def server_up_popup():
    """
    Popup if server waiting for client
    """
    pop = Popup(title='Waiting on client',
                  content=Label(text='Waiting on client. Server Up...'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()



kv = Builder.load_file("Graphics\\assets\\graphics.kv")

def change_window(window_name):
    window_manger.current = window_name

class WindowManager(ScreenManager):
    pass
window_manger = WindowManager()

class Gui(App):
    """
    Main app
    """
    def build(self):
        return window_manger

def startApp():
    """
    Starts the app
    """
    Gui().run()

class StartScreen(Screen):
    """
    Start screen class is the graphic presention
    of the start screen 
    """
    def NextWindow(self):
        """
        When the user presses enter it goes to the next window
        """
        change_window("OptionsScreen")

class AuthenticationScreen(Screen):
    """
    AuthenticationScreen is a class that will handle 
    sending and receiving email authentication
    """
    
    user_mail = ObjectProperty(None)
    user_code = ObjectProperty(None)
    code = 0 

    def check_code(self):
        if self.user_code.text == str(self.code):
            self.code = 0
            change_window("OptionsScreen")
        
    def send_code(self):
        self.code = random.randint(100000, 999999)
        pass

class OptionsScreen(Screen):
    """
    Options Screen class is in charge of 
    graphic presentition of the avalibale options for the user 
    """
    def auto_control_screen(self):
        """
        Switches to the Auto control screen 
        """
        change_window("AutoControlScreen")

    def human_control_screen(self):
        """
        Switches to the Human control screen 
        """
        change_window("HumanControlScreen")

class AutoControlScreen(Screen):
    """
    AutoControl screen class is for the gui 
    of the user when not in control
    """
    def update_frame(self, dt):
        frame = self.image_detection.frame
        if frame is None:
            return
        # Flip the frame 180 degrees
        frame = cv2.flip(frame, -1)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def on_enter(self, *args):

        # Start server 
        udp_server = UdpServer(PORT, CODE_LEN)
        udp_server.start_server()

        # Pop up
        server_up_popup()

        # Start Image detection class
        self.image_detection = ImageDetection(udp_server, STEP_SIZE)

        image_detection_thread = threading.Thread(target = self.image_detection.handle_recv)
        image_detection_thread.start()

        

        # Set image widget
        self.img = Image()
        self.add_widget(self.img)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

        return super().on_enter(*args)
    
    def on_leave(self, *args):
        self.image_detection.running = False

        # Remove image widget
        Clock.unschedule(self.update_frame)
        self.capture.release()
        self.remove_widget(self.img)
        
        return super().on_leave(*args)
    
class HumanControlScreen(Screen):
    """
    HumanControl screen class is for the gui 
    of the user when he is in control
    """

    def __init__(self, **kw):
        global joystick
        self.clock = pygame.time.Clock()

        self.motion = [0, 0]

        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)

        else:
            raise Exception("Controller is not connected. Please connect controller")
        
        super().__init__(**kw)

    def send_steps(self):
        """
        Handels all of the pygame events. Button press and joystick move
        """

        while True:
            try:
                data, addr = self.image_detection.server.recv_frame()
                self.image_detection.set_frame(data)
                steps_horizntal, steps_vertical = self.shm[0], self.shm[1]
                self.move(steps_horizntal, steps_vertical, addr)
                self.shot(addr)
            except:
                print("error")
            
    def shot(self, addr: tuple):
        """
        When R1 is preesed send the client an order to shot
        
        Args:
            addr (tuple): address of the client
        """
        if self.shm[2] == 1:
            print("Shot")

    def move(self, steps_horizntal: int, steps_vertical: int, addr: tuple):
        """
        When joystick moved send the client num of steps in each diraction

        Args:
            steps_horizntal (int): stpes on the horizontal axis. Negative left, positive right.
            steps_vertical (int): stpes on the vertical axis. Negative up, positive down.
            addr (tuple): address of the client
        """
        # If they are both 0 it means there is no need to move
        # So no need to send new location to the client
        
        self.image_detection.send_steps(addr , (steps_horizntal, steps_vertical))

    def update_frame(self, dt):
        frame = self.image_detection.frame
        if frame is None:
            return
        # Flip the frame 180 degrees
        frame = cv2.flip(frame, -1)
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def on_enter(self, *args):
        # Start server 
        udp_server = UdpServer(PORT, CODE_LEN)
        udp_server.start_server()

        # Pop up
        server_up_popup()

        # Start Image detection class
        self.image_detection = ImageDetection(udp_server, STEP_SIZE)

        controller_proc = subprocess.Popen(["python","Graphics\\ControllerEvents.py"])

        time.sleep(2)

        self.shm = shared_memory.ShareableList(name="controller_mem")  # TOO SLOW 

        # Start steps sending thread
        steps_thread = threading.Thread(target=self.send_steps)
        steps_thread.start()

        # Set image widget
        self.img = Image()
        self.add_widget(self.img)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

        return super().on_enter(*args)
    
    def on_leave(self, *args):
        self.image_detection.running = False

        # Remove image widget
        Clock.unschedule(self.update_frame)
        self.capture.release()
        self.remove_widget(self.img)
        
        return super().on_leave(*args)
        
screens = [StartScreen(name="StartScreen"), AuthenticationScreen(name="AuthenticationScreen"), OptionsScreen(name="OptionsScreen"), AutoControlScreen(name="AutoControlScreen"), HumanControlScreen(name="HumanControlScreen")]
for screen in screens:
    window_manger.add_widget(screen)

window_manger.current = "HumanControlScreen"
if __name__ == "__main__":
    startApp()

     
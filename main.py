from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast

from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.spinner import MDSpinner

import io
import zipfile
from itertools import cycle

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

from gpshelper import GpsHelper
from homepage import HomePage
from formpage import FormPage
from routepage import RoutePage

from kivy.core.window import Window
Window.fullscreen = 'auto'

class UserInfo:
    # FIELDS:
    # lat                 (Float)
    # lon                 (Float)
    # interests           (Array of strings) available inputs:
    #                     Attractions, Museums, Shopping, Hiking, Monuments
    # food                (Array of Strings) e.g. ['restaurant', 'bar']
    # trip_length         (int)
    # budget              (int) range: 0 to 4
    # transportation      (String) 4 possible strings: 'transit', 'driving', 'walking', 'cycling'
    def __init__(self):
        self.gps_lat = 42.360674
        self.gps_lon = -71.065140
        self.lat = self.gps_lat   # Davis location as default (easter egg lol)
        self.lon = self.gps_lon
        self.radius = 400
        self.interests = ["bowling_alley", "amusement_park", "casino", "spa", "night_club", \
                        "movie_theater" , "tourist_attraction", "art_gallery", "aquarium", \
                        "zoo", "university", "library",\
                        "clothing_store",  "marketplace", "shopping_mall", "shoe_store",\
                        "museum", "history", "art",\
                        "hiking", "park", "campground", "wildlife", "beach"]
        self.food = ['restaurant', 'bar', 'cafe']
        self.trip_length = 4 * 60       # 4 hours in minutes
        self.budget = 2
        self.transportation = 'walking'
    pass

class ContentNavigationDrawer(BoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.text_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.text_color

class PageToolbar(MDToolbar):
    pass

class HelpPage(Screen):
    pass

class DetailsPage(Screen):
    pass

class LoadingPage(Screen):
    pass

class WindowManager(ScreenManager):
    def return_homepage(self, direction):
            self.current = "HomePage"
            if direction == "right":
                self.current_screen.manager.transition.direction = "right"
            else:
                self.current_screen.manager.transition.direction = "left"

class MainScreen(Screen):
    nav_drawer = ObjectProperty(None)
    windows = ObjectProperty(None)
    homepage = ObjectProperty(None)
    routepage = ObjectProperty(None)
    loadingpage = ObjectProperty(None)

class TripRouletteApp(MDApp): 
    user_info = UserInfo()

    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"

    def on_start(self):
        icons_item = {
            "account": "How It Works",
            "city-variant-outline": "Personalize",
            "help": "Help"
        }

        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
    
        # Initialize GPS
        GpsHelper().run()

app = TripRouletteApp()
import bugs
bugs.fixBugs()
app.run()

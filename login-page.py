import hashlib
import string

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, RiseInTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.graphics import *
from kivy.metrics import dp


#Font management

LabelBase.register(name = "AlexBrush", fn_regular = "fonts/AlexBrush-Regular.ttf")
LabelBase.register(name = "Quicksand-Bold", fn_regular = "fonts/Quicksand-Bold.otf")
LabelBase.register(name = "OstrichSans-Bold", fn_regular = "fonts/OstrichSans-Bold.otf", fn_bold = "fonts/OstrichSans-Black.otf")
LabelBase.register(name = "OpenSans", fn_regular = "fonts/OpenSans-Regular.ttf", fn_bold = "fonts/OpenSans-Semibold.ttf")
LabelBase.register(name = "CamingoCode", fn_regular = "fonts/CamingoCode-Regular.ttf")
LabelBase.register(name = "CooperHewitt", fn_regular = "fonts/CooperHewitt-Medium.otf")
LabelBase.register(name = "FiraSans", fn_regular = "fonts/FiraSans-Book.otf")


#Username and password validation

username_acceptable = string.ascii_letters + string.digits + "@_"
password_acceptable = username_acceptable + "$#*-"


class WindowsManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowsManager, self).__init__(**kwargs)
        self.add_widget(StartingPage(name = "starting"))
        self.add_widget(LoginPage(name = "login"))
        self.add_widget(MapPage(name = "map"))


class StartingPage(Screen):
    def __init__(self, **kwargs):
        super(StartingPage, self).__init__(**kwargs)

        self.layout = FloatLayout()

        self.layout.add_widget(Image(source = "images/logo.jpg", keep_ratio = True))
        
        with self.layout.canvas:
            Color(0, 0, 0, 0.8)
            Rectangle(size = (10000, 10000))

        self.layout.add_widget(Label(text = "Event Mapper", font_name = "AlexBrush", font_size = 130, pos_hint = {"x":0, "y": 0.5}, size_hint = (1, 0.5)))
        self.button_visitor = Button(text = "Visitor", font_name = "Quicksand-Bold", background_color = (0.3, 0.3, 0.3, 1), font_size = 35, pos_hint = {"x":0.35, "y":0.26}, size_hint = (0.3, 0.125))
        self.button_organizer = Button(text = "Organizer", font_name = "Quicksand-Bold", background_color = (0.3, 0.3, 0.3, 1), font_size = 35, pos_hint = {"x":0.35, "y":0.1}, size_hint = (0.3, 0.125))
        self.button_visitor.bind(on_press = self.pressed_visitor, on_release = self.released_visitor)
        self.button_organizer.bind(on_press = self.pressed_organizer, on_release = self.released_organizer)
        self.layout.add_widget(self.button_visitor)
        self.layout.add_widget(self.button_organizer)

        self.add_widget(self.layout)

    

    def pressed_visitor(self, instance):
        self.button_visitor.background_color = (1, 1, 1, 1)
        self.button_visitor.color = (0, 0, 0, 1)
    

    def released_visitor(self, instance):
        self.button_visitor.background_color = (0.3, 0.3, 0.3, 1)
        self.button_visitor.color = (1, 1, 1, 1)
        self.manager.transition = RiseInTransition()
        self.manager.current = "map"

    
    def pressed_organizer(self, instance):
        self.button_organizer.background_color = (1, 1, 1, 1)
        self.button_organizer.color = (0, 0, 0, 1)
    

    def released_organizer(self, instance):
        self.button_organizer.background_color = (0.3, 0.3, 0.3, 1)
        self.button_organizer.color = (1, 1, 1, 1)
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "up"
        self.manager.current = "login"


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.361, 0.847, 0.584, 1)
            self.background_rect = Rectangle(size = self.size, source = "images/marine-background.jpg")
        
        self.layout.add_widget(Label(text = "Log In", font_name = "OstrichSans-Bold", bold = True, font_size = 85, color = (0.02, 0.22, 0.42, 1), pos_hint = {"x":0, "y":0.78}, size_hint = (1, 0.2)))
        self.layout.add_widget(Label(text = "Username", font_name = "OpenSans", bold = True, font_size = 38, color = (0.02, 0.22, 0.42, 1), pos_hint = {"right":0.4, "center_y":0.6}, size_hint = (None, None)))
        self.layout.add_widget(Label(text = "Password", font_name = "OpenSans", bold = True, font_size = 38, color = (0.02, 0.22, 0.42, 1), pos_hint = {"right":0.4, "center_y":0.45}, size_hint = (None, None)))
        
        self.username_input = TextInput(multiline = False, font_size = 23, font_name = "CamingoCode", pos_hint = {"x":0.5, "center_y":0.6}, size = (dp(300), dp(45)), size_hint = (None, None))
        self.password_input = TextInput(multiline = False, font_size = 23, font_name = "CamingoCode", password = True, pos_hint = {"x":0.5, "center_y":0.45}, size = (dp(300), dp(45)), size_hint = (None, None))
        self.username_input.bind(text = self.validate_username)
        self.password_input.bind(text = self.validate_password)
        self.button_sign_in = Button(text = "Sign in", font_name = "CooperHewitt", font_size = 35, background_color = (0.3, 0.7, 0.7, 1), color = (0.93, 0.96, 0.88, 1), pos_hint = {"right":0.48, "y": 0.13}, size = (dp(250), dp(65)), size_hint = (None, None))
        self.button_sign_up = Button(text = "Sign up", font_name = "CooperHewitt", font_size = 35, background_color = (0.3, 0.7, 0.7, 1), color = (0.93, 0.96, 0.88, 1), pos_hint = {"x":0.52, "y": 0.13}, size = (dp(250), dp(65)), size_hint = (None, None))
        self.button_sign_in.bind(on_press = self.pressed_sign_in, on_release = self.released_sign_in)
        self.button_sign_up.bind(on_press = self.pressed_sign_up, on_release = self.released_sign_up)
        self.button_instructions = Button(text = "i", font_name = "CamingoCode", font_size = 25, color = (0.1, 0.1, 0.1, 1), background_color = (0, 0, 0, 0), pos_hint = {"right":0.97, "top":0.97}, size = (dp(40), dp(40)), size_hint = (None, None))
        self.button_instructions.bind(on_press = self.pressed_instructions, on_release = self.released_instructions)

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.button_sign_in)
        self.layout.add_widget(self.button_sign_up)
        self.layout.add_widget(self.button_instructions)

        self.add_widget(self.layout)

    
    def on_size(self, *args):
        self.background_rect.size = self.size

    
    def pressed_instructions(self, instance):
        self.button_instructions.background_color = (0.2, 0.2, 0.2, 1)
        self.button_instructions.color = (1, 1, 1, 1)
    

    def released_instructions(self, instance):
        self.button_instructions.background_color = (0, 0, 0, 0)
        self.button_instructions.color = (0.1, 0.1, 0.1, 1)
        multiline_instructions = Label(text = '''
        Instructions for username :
        
        -  Minimum allowed length is 4
        -  Allowed characters : Alphanumeric (A-Z, a-z, 0-9) and symbols (@_)
                                       

        Instructions for password :
                                       
        -  Minimum allowed length is 4
        -  Allowed characters : Alphanumeric (A-Z, a-z, 0-9) and symbols (@_$#*-)
        -  We recommend a password that is arround 6 characters in length
        ''',
        font_name = "FiraSans", font_size = 20)
        instructions_popup = Popup(title = "Instructions", content = multiline_instructions, size = (dp(750), dp(500)), size_hint = (None, None))
        instructions_popup.open()


    def validate_username(self, instance, value):
        if self.username_input.text[-1:] not in username_acceptable:
            self.username_input.text = self.username_input.text[:-1]
    

    def validate_password(self, instance, value):
        if self.password_input.text[-1:]  not in password_acceptable:
            self.password_input.text = self.password_input.text[:-1]
    

    def pressed_sign_in(self, instance):
        self.button_sign_in.background_color = (1, 1, 1, 1)
        self.button_sign_in.color = (0.15, 0.35, 0.35, 1)
    
    
    def released_sign_in(self, instance):
        self.button_sign_in.background_color = (0.3, 0.7, 0.7, 1)
        self.button_sign_in.color = (0.93, 0.96, 0.88, 1)

        username = self.username_input.text
        password = self.password_input.text

        if len(username) < 4:
            self.show_error_message("Username must be at least 4 characters in length")
        elif len(password) < 4:
            self.show_error_message("Password must be at least 4 characters in length")
        else:
            with open("credentials", 'r') as credentials_file:
                credentials_dict = self.get_credentials_dict(credentials_file)   

            if username not in credentials_dict.keys(): #Username doesn't exist
                self.show_error_message("This username does not exist, please sign up")
            else:
                if credentials_dict[username] == hashlib.sha512(password.encode()).hexdigest():
                    self.manager.transition = RiseInTransition()
                    self.manager.current = "map"
                else:
                    self.show_error_message("Incorrect password, please try again")
                    self.password_input.text = ""
    

    def pressed_sign_up(self, instance):
        self.button_sign_up.background_color = (1, 1, 1, 1)
        self.button_sign_up.color = (0.15, 0.35, 0.35, 1)
        

    def released_sign_up(self, instance):
        self.button_sign_up.background_color = (0.3, 0.7, 0.7, 1)
        self.button_sign_up.color = (0.93, 0.96, 0.88, 1)
    
        username = self.username_input.text
        password = self.password_input.text

        with open("credentials", 'r+') as credentials_file:
            credentials_dict = self.get_credentials_dict(credentials_file)    
            if len(username) < 4:
                self.show_error_message("Username must be at least 4 characters in length")
            elif len(password) < 4:
                self.show_error_message("Password must be at least 4 characteres in length")
            elif username in credentials_dict.keys():
                self.show_error_message("This username is taken, please try again")
                self.username_input.text = ""
                self.password_input.text = ""
            else:
                credentials_file.write(username + ":" + hashlib.sha512(password.encode()).hexdigest() + "\n")
                self.manager.transition = RiseInTransition()
                self.manager.current = "map"


    def get_credentials_dict(self, file_object):
        sample_dict = {}
        for entry in file_object.readlines():
            entry_split = entry.split(":")
            sample_dict[entry_split[0]] = entry_split[1].strip()
        return sample_dict


    def show_error_message(self, error_message):
        Popup(title = "Error", content = Label(text = error_message, font_name = "FiraSans", font_size = 23), size_hint = (None, None), size = (dp(700), dp(200))).open()


class MapPage(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.layout = GridLayout()
        
        self.add_widget(Label(text = "Map window"))


class EventMapperApp(App):
    def build(self):
        return WindowsManager()


if __name__ == "__main__":
    EventMapperApp().run()
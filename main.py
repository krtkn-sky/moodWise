from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
import json, glob, random
from datetime import datetime
from pathlib import Path

Builder.load_file('style.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pwd):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pwd:
            self.manager.current = "content_screen"
            self.ids.username.text = ""  # Clear username input
            self.ids.password.text = ""  # Clear password input
        else:
            self.ids.login_wrong.text = "Wrong username/password"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pwd):
        with open("users.json") as file:
            users = json.load(file)
        users[uname] = {'username': uname,
                        'password': pwd,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", "w") as file:
            json.dump(users, file)
        self.manager.current = "sign_up_success"
        self.ids.username.text = ""  # Clear username input
        self.ids.password.text = ""  # Clear password input  


class SignUpSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        # Clear username and password inputs on returning to login screen
        self.manager.get_screen("login_screen").ids.username.text = ""
        self.manager.get_screen("login_screen").ids.password.text = ""

class ContentScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        self.ids.feel.text = ""  # Clear "How do you feel?" input field after logout

    def get_quote(self, feel):
        feel = feel.lower()
        feels = glob.glob("quotes/*txt")
        feels = [Path(filename).stem for filename in feels]
        if feel in feels:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
            self.ids.feel.text = ""  # Clear "How do you feel?" input field after getting a quote
        else:
            self.ids.quote.text = "Oops not a valid prompt :( "


class MainApp(App):
    def build(self):
        self.title = "Mood Wise"
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
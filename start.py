import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1

        self.topgrid = GridLayout()
        self.topgrid.cols = 2 

        self.topgrid.add_widget(Label(text='User Name:'))
        self.username = TextInput(multiline=False)
        self.topgrid.add_widget(self.username)

        self.topgrid.add_widget(Label(text='Password:'))
        self.password = TextInput(password=True, multiline=False)
        self.topgrid.add_widget(self.password)

        self.topgrid.add_widget(Label(text='Email:'))
        self.email = TextInput(multiline=False)
        self.topgrid.add_widget(self.username)

        self.add_widget(self.topgrid)
        self.submit = Button(text = 'Submit', font_size = 40)
        self.submit.bind(on_press = self.pressed)
        self.add_widget(self.submit)


    def pressed(self, instance):
        name = self.username.text
        password = self.username.text
        email = self.email.text

        self.username.text = ""
        self.username.text = ""
        self.email.text    = ""


        
class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    MyApp().run()
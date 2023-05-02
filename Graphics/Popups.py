from kivy.uix.popup import Popup
from kivy.uix.label import Label
def server_up_popup():
    """
    Popup if server waiting for client
    """
    pop = Popup(title='Waiting on client',
                  content=Label(text='Waiting on client. Server Up...'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def sent_email_popup():
    """
    Popup if email was sent to the user
    """
    pop = Popup(title='Sent email successfully!',
                  content=Label(text='Sent email! Please check your inbox\n(this could take a couple of minutes)'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def wrong_code_popup():
    """
    Popup if wrong code was enterd
    """
    pop = Popup(title='Bad Code!',
                  content=Label(text='Code is not correct please try again...'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

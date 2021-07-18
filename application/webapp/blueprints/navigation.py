from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link

nav = Nav()

menu = Navbar("Smart Animon")
menu.items = [View('Monitored Animals','frontend.monitored')]
menu.items.append(View('Identified Animals','frontend.identified'))
menu.items.append(View('Not Identified Animals','frontend.not_identified'))
#menu.items.append(Link('Ajuda','https://www.google.com'))

nav.register_element("inicial", menu)

def init_app(app):
    nav.init_app(app)
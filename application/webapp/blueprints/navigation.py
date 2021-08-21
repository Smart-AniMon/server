from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link

nav = Nav()

menu = Navbar(View('Smart Animon', 'frontend.index'))
menu.items.append(Subgroup('Animais', View('Monitorados','frontend.monitored'), 
                                  View('Identificados','frontend.identified'),
                                  View('Não Identificados','frontend.not_identified')))
menu.items.append(Subgroup('Notificações', View('Não Lidas','frontend.notification'),
                                           View('Flags','frontend.flag'),
                                           View('Histórico','frontend.history'))) 

#menu.items.append(Subgroup('Labels', View('Listar',''), View('Cadastrar')))
#menu.items.append(Link('Github','https://github.com/Smart-AniMon'))

nav.register_element("inicial", menu)

def init_app(app):
    nav.init_app(app)
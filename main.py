from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
import certifi
from kivymd.uix.dialog import MDDialog


KV= """
NavigationLayout:

    ScreenManager:

        Screen:

            BoxLayout:
                orientation: 'vertical'

                MDToolbar:
                    title: "Wikipedia Reader"
                    elevation: 10
                    left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

                GridLayout:
                    rows: 4

                    MDTextField:
                        id: mdtext
                        hint_text: "Cosa stai cercando?"
                        mode: "rectangle"
                            
                    MDRaisedButton:
                        text: "AVVIA RICERCA"
                        size_hint_x: 1
                        size_hint_y: 0.1
                        on_press: app.normal_search()

                    ScrollView:
                        MDLabel:
                            id: mdlab
                            text: "Benvenuto su Wikipedia Reader!"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None

                    MDRaisedButton:
                        text: "CERCA ARTICOLO CASUALE"
                        size_hint_x: 1
                        size_hint_y: 0.1
                        on_press: app.random_search()

    MDNavigationDrawer:
        id: nav_drawer

        BoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
                height: avatar.height

                Image:
                    id: avatar
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "wikipedia.png"

            MDLabel:
                text: "WikiReader App 1.0"
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "https://github.com/11dome11"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:

                MDList:

                    OneLineAvatarListItem:
                        text: "Info App"
                        on_press: app.show_app_info_dialog()

                        IconLeftWidget:
                            icon: "information-outline"

                    OneLineAvatarListItem:
                        text: "Contatti"
                        on_press: app.show_contact_info_dialog()

                        IconLeftWidget:
                            icon: "contact-mail-outline"
"""

class WikiReaderapp(MDApp):
    
    info_dialog = None
    contact_dialog = None
    
    def build(self):
        self.title="WikipediaReader by @11dome11"
        self.theme_cls.primary_palette="Teal"
        self.theme_cls.primary_hue= "300"
        self.icon= 'wikipedia.png'
        return Builder.load_string(KV)
    
    def normal_search(self):
        query= self.root.ids["mdtext"].text
        self.get_data(title=query)
        
    def random_search(self):
        endpoint="https://it.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json"
        self.root.ids["mdlab"].text="Caricamento in corso..." 
        self.rs_request = UrlRequest(endpoint,on_success=self.get_data,ca_file=certifi.where())
    
    def get_data(self, *args, title=None):
        if title == None:
            response=args[1]
            random_article=response["query"]["random"][0]
            title=random_article["title"]
        endpoint= f"https://it.wikipedia.org/w/api.php?prop=extracts&explaintext&exintro&format=json&action=query&titles={title.replace(' ', '%20')}"
        self.data_request = UrlRequest(endpoint,on_success=self.set_text_area,ca_file=certifi.where())

    def set_text_area(self, request, response):
        page_info=response["query"]["pages"]
        page_id=next(iter(page_info))
        page_title=page_info[page_id]["title"]
        try:
            page_extract=page_info[page_id]["extract"]
        except KeyError:
            page_extract=f"Mi dispiace, ma la ricerca '{page_title}' non ha prodotto alcun risultato \n\n Riprova!"
        self.root.ids["mdlab"].text=f"{page_title}\n\n{page_extract}"
        
    def show_app_info_dialog(self):
        app_info = "Wikipedia Reader\n\nMade with Kivy"
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                title = "Informazioni App",
                text = app_info,
                auto_dismiss = True
            )
        self.info_dialog.open()

    def show_contact_info_dialog(self):
        app_info = "Sviluppatore: \n\ndomenico.morabito88@gmail.com"
        if not self.contact_dialog:
            self.contact_dialog = MDDialog(
                title = "Contatti",
                text = app_info,
                auto_dismiss = True
            )
        self.contact_dialog.open()
        
WikiReaderapp().run()
        
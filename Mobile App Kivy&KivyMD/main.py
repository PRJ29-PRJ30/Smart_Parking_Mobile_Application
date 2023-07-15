from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
import pypyodbc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import time
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
Window.size = (350,600)

kv = '''

MDScreen:
    name: "Ekran"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        
        MovingRoad:
            id: moving_road
            canvas.before:
                Color:
                    rgb: 1, 1, 1, 1
                Rectangle :
                    size: 360, 150
                    pos: 0, 470
                    texture: self.road_texture
        Image:
            source: "car.png"
            size_hint: .3, .3
            pos_hint: {"center_x": .5, "center_y": .90}
    
    MDFloatLayout:
        md_bg_color: rgba(172,212,115,255)
        pos_hint:{"center_y":0.32}
        Image:
            source: "wh.jpg"
            size_hint: .99, .99
            pos_hint: {"center_x": .5, "center_y": .23}

        MDLabel:
            text: "WELCOME"
            pos_hint: {"center_x": 0.58, "center_y": .96}
            haling: "center"
            color: 0, 0, 0, 100
            font_size: "70sp"
            font_name: "kont"
        MDLabel:
            text: "If you have exceeded the checking out time in your reservation, please fill in the blanks below and click the button to retrieve your vehicle.           If you have arrived before the check-out time of your reservation, please enter the check-out time from your reservation in the 'Time' section."
            pos_hint: {"center_x": 0.51, "center_y": .37}
            
            font_size: "11sp"
        MDTextField:
            id: plaka
            hint_text: "License Plate:"
            helper_text: "Ex: 26 ESTU 27"
            helper_text_mode: "persistent"
            line_color_focus: 0, 0, 0, 100
            mode: "rectangle"
            size_hint: .7, .1
            pos_hint: {"center_x": 0.5, "center_y": .87}
            required: True
            font_name: "font"
        MDTextField:
            id: tarih
            hint_text: "Date:"
            helper_text: "Ex: 13/12/2022"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .7, .1
            pos_hint: {"center_x": 0.5, "center_y": .75}
            required: True
            max_text_length: 10
            min_text_length: 10
            validator: "date"
            date_format: "dd/mm/yyyy"
            date_interval: "01/01/2023", "01/01/2100"
            font_name: "font"
        MDTextField:
            id: saat1
            hint_text: "Check-in:"
            helper_text: "Ex: 11:30"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .3, .1
            pos_hint: {"center_x": 0.3, "center_y": .63}
            required: True
            validator: "time"
            time_format: "hh:mm"
            font_name: "font"
        MDTextField:
            id: saat2
            hint_text: "Check-out:"
            helper_text: "Ex: 15:00"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .3, .1
            pos_hint: {"center_x": 0.70, "center_y": .63}
            required: True
            validator: "time"
            time_format: "hh:mm"
            font_name: "font"
        MDTextField:
            id: cikis1
            hint_text: "Your Slot:"
            helper_text: "Ex: A1"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .3, .1
            pos_hint: {"center_x": 0.2, "center_y": .27}
        MDTextField:
            id: cikis2
            hint_text: "Time:"
            helper_text: "Ex: 15:00"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .3, .1
            pos_hint: {"center_x": 0.55, "center_y": .27}
        MDTextField:
            id: park
            hint_text: "Parking Slot"
            helper_text: "Ex: A1"
            helper_text_mode: "persistent"
            mode: "rectangle"
            size_hint: .3, .1
            pos_hint: {"center_x": 0.3, "center_y": .51}
            required: True
            font_name: "font"
        MDIconButton:
            icon: "reserved.png"
            pos_hint: {"center_x": .7, "center_y": .49}
            icon_size: "70sp"
            on_release:
                app.show_alert(plaka.text,tarih.text,saat1.text,saat2.text,park.text)
                
                
        MDIconButton:
            icon: "desktop-calendar.png"
            icon_size: "50sp"
            pos_hint: {"center_x": .75, "center_y": .75}
            on_release: app.show()

        MDFlatButton:
            text: "GO OUT!!"
            font_name: "font"
            font_size: "18sp"
            pos_hint: {'center_x': .85, 'center_y': .26}
            on_release: app.show_alert_dialog(cikis1.text,cikis2.text)
'''

class MovingRoad(MDFloatLayout):
    road_texture = ObjectProperty()

    def __init__(self, **kwargs):
        super(MovingRoad, self).__init__(**kwargs)
        self.road_texture = Image(source="road.jpg").texture
        self.road_texture.wrap = "repeat"
        self.road_texture.uvsize = (Window.width / self.road_texture.width, -1)
    def scroll(self, time):
        self.road_texture.uvpos = ((self.road_texture.uvpos[0] + time/3) % Window.width, self.road_texture.uvpos[1])
        textue = self.property("road_texture")
        textue.dispatch(self)

class PaymentPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title_label = Label(text="3D Secure")
        card_number_label = Label(text="Enter Card Number")
        card_number_input = TextInput(multiline=False)
        expiry_date_label = Label(text="Enter Expiry Date")
        expiry_date_spinner = Spinner(text="MM/YYYY", values=["01/2022", "02/2022", "03/2022"])  # Örnek değerler
        cvv_label = Label(text="Enter CVV")
        cvv_input = TextInput(multiline=False)
        confirm_button = Button(text="Complete", on_release=self.dismiss)

        content_layout = BoxLayout(orientation="vertical")
        content_layout.add_widget(title_label)
        content_layout.add_widget(card_number_label)
        content_layout.add_widget(card_number_input)
        content_layout.add_widget(expiry_date_label)
        content_layout.add_widget(expiry_date_spinner)
        content_layout.add_widget(cvv_label)
        content_layout.add_widget(cvv_input)
        content_layout.add_widget(confirm_button)

        # Düzeni popup içeriğine ayarlayın
        self.content = content_layout



class ParkingApp(MDApp):
    dialog = None
    refff = None
    def on_start(self):
        Clock.schedule_interval(self.root.ids.moving_road.scroll, .01)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(kv)

    def show(self):
        DatePicker = MDDatePicker(year=2023,month=5,day=13,radius=[27, 27, 27, 26],primary_color="lightgreen",selector_color="lightgreen")
        DatePicker.bind(on_save=self.on_save,on_cancel=self.on_cancel)
        DatePicker.open()

    def on_save(self,instance,value,data_range):
        self.root.ids.tarih.text=str(value)


    def on_cancel(self, instance,value):
        self.root.ids.tarih.text="sellect a date"

    def send_data1(self, cikis1, cikis2):
        cred = credentials.Certificate('*****************************************')     # add here your json file of firebase project
        firebase_admin.initialize_app(cred, {'databaseURL': "*************************************************"})   # add here your firebase path
        reff = db.reference(f"/Plaka/{cikis1}")
        plaka3 = reff.get()
        self.refff = db.reference(f"/Rezervasyon/{plaka3}/Durum")
        reff2 = db.reference(f"/Rezervasyon/{plaka3}/Çıkış Saati")
        saat5 = reff2.get()
        saat1 = datetime.strptime(saat5, "%H:%M")
        saat2 = datetime.strptime(cikis2, "%H:%M")
        fark = saat2 - saat1
        fark_dakika = fark.total_seconds() // 60
        print(fark_dakika)

        return fark_dakika

    def show_alert_dialog(self,cikis1,cikis2):
        if not self.dialog:
            fark2 = self.send_data1(cikis1,cikis2)
            if fark2 == 0 or fark2 < 0:
                text = "You're an early bird :) No payment is required.\nPlease follow the steps below in order.\n\nNOTE: You don't need to click the 'Pay' and 'Bar-down' buttons. Pass them.\n\n1) Make sure you have removed your vehicle from the parking area and click on the 'Bar-up' button.\n2) Click the 'Cancel' button and continue your way."
            else:
                text = f"YOU ARE LATE FOR {fark2} MINUTES.\nYOU HAVE TO PAY {fark2 * 2}$\n\n1) Click the 'Pay' button and make your payment.\n2) To remove your vehicle from the parking area, click on the 'Bar-down' button.\n3) Make sure you have removed your vehicle from the parking area and click on the 'Bar-up' button.\n4) Click the 'Cancel' button and continue your way."

            self.dialog = MDDialog(
                text=text,
                buttons=[
                    MDFlatButton(
                        text="Pay",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.payment
                    ),
                    MDFlatButton(
                        text="Bar-down",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release = lambda x: self.refff.set('T')
                    ),
                    MDFlatButton(
                        text="Bar-up",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.refff.set('F')
                    ),

                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )


        self.dialog.open()

    def show_alert(self, plaka, tarih, saat1, saat2, park):
        if not self.dialog:
            saat11 = datetime.strptime(saat1, "%H:%M")
            saat22 = datetime.strptime(saat2, "%H:%M")
            saatd = saat22 + timedelta(minutes=2)
            saatdd = datetime.strftime(saatd, "%H:%M")
            print(saatdd)
            print(saat22)
            saat1_dakika = saat11.hour * 60 + saat11.minute
            saat2_dakika = saat22.hour * 60 + saat22.minute
            fark_dakika = saat2_dakika - saat1_dakika
            print(fark_dakika)
            # Send data to Firebase
            cred = credentials.Certificate('***********************************')   # add here your json file of firebase project
            firebase_admin.initialize_app(cred,
                                          {'*****************************************************"})  # add here your firebase path
            ref = db.reference("/Rezervasyon")



            data = {
                'Plaka': plaka,
                'Tarih': tarih,
                'Giriş Saati': saat1,
                'Çıkış Saati': saat2,
                'Park Yeri': park,
                'Durum': 'F',
                'Sensör Bariyer': 'F',
                'Sensör Yer': 'F',
                'Çıkış Delay': saatdd
            }
            ref.child(plaka).set(data)
            reff = db.reference("/Plaka")
            reff.child(park).set(plaka)

            self.dialog = MDDialog(
                text=f"You have reserved for {fark_dakika} minutes.\n Your reservation fee is {(fark_dakika) * 0.15}$",
                buttons=[
                    MDFlatButton(
                        text="PAY",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.payment
                    ),
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def payment(self, *args):
        payment_popup = PaymentPopup()
        payment_popup.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()


    def send_data(self, plaka, tarih, saat1, saat2, park):
        from firebase import firebase
        saat11 = datetime.strptime(saat1, "%H:%M")
        saat22 = datetime.strptime(saat2, "%H:%M")

        saatd = saat22 + timedelta(minutes=2)
        print(saatd)
        cred = credentials.Certificate('***************************************') # add here your json file of firebase project
        firebase_admin.initialize_app(cred, {'databaseURL': "*******************************"}) # add here your firebase path

        data = {'Plaka': plaka, 'Tarih': tarih, 'Giriş Saati': saat1, 'Cıkıs Saati': saat2, 'Park Yeri': park, 'Durum':'F','Sensör Bariyer':'F','Sensör Yer':'F'}
        ref = db.reference("/Rezervasyon")
        ref.child(plaka).set(data)
        ref = db.reference("/Plaka")
        ref.child(park).set(plaka)

        pass


if __name__ == "__main__":
    LabelBase.register(name="font", fn_regular="C:\\Users\\MSI-NB\\PycharmProjects\\pythonProject8\\THEBOLDFONT.ttf")
    LabelBase.register(name="kont",fn_regular="C:\\Users\\MSI-NB\\PycharmProjects\\pythonProject8\\DESIGNER.otf")
    ParkingApp().run()


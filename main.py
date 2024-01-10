import re
from pytube import YouTube
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from functools import partial                                               ## important for partial-method to use
from kivy.core.window import Window
Window.size=(500, 600)                                                      ## sets widget size in pixels


class MyApp(MDApp):

    def getLinkInfo(self,event,layout):
        self.link=self.linkField.text                                        ## the first step to acquire the link from the link-field
        self.checkLink=re.match("^https://www.youtube.com/.*", self.link)

        if (self.checkLink):
            print("Valid Link")
            self.errorLabel.text=""
            self.errorLabel.pos_hint={"center_x":0.5, "center_y":20}


            self.errorLabel.text=""
            self.errorLabel.pos_hint={"center_x":0.5, "center_y":20}
            self.yt=YouTube(self.link)                                         ## the second - assign link to YouTube module
            self.title=str(self.yt.title)                                         ##the third - we assign to title what we want to get from YouTube
            self.titelLabel.text="Title: " + self.title
            self.titelLabel.pos_hint={"center_x":0.5, "center_y":0.4}
            self.titelLabel.color=('#23d420')
            self.titelLabel.split_str=" "
            self.linkButton.text="Link Info"
            self.linkButton.pos_hint={"center_x":0.2, "center_y":0.5}
            self.convertButton.text="Convert"
            self.convertButton.pos_hint={"center_x":0.5, "center_y":0.15}
            self.convertButton.size_hint=(.3, .1)
            self.videoButton.text="Download"
            self.videoButton.pos_hint={"center_x":0.18, "center_y":0.15}
            self.videoButton.size_hint=(.3, .1)
            self.audio = self.yt.streams.get_audio_only()     ## here we use a particular method from PyTube library to get audio
            print(self.audio)
            self.video=self.yt.streams.filter(file_extension="mp4").order_by('resolution').desc()      ## here we use a particlar method from PyTube library to get video
            print(self.video)
            print("Title: " + self.title)

            self.dropDown = DropDown()                                  ## ths function is for choosing video resolution
            for video in self.video:
                    button = Button(text=video.resolution, size_hint_y=None, height=30)
                    button.bind(on_release=lambda button:self.dropDown.select(button.text))
                    self.dropDown.add_widget(button)
            self.main_Button=Button(text="144p", size_hint=(None, None), pos=(510,105), height=50)
            self.main_Button.bind(on_release=self.dropDown.open)
            self.dropDown.bind(on_select=lambda instance, x:setattr(self.main_Button, 'text',x))
            layout.add_widget(self.main_Button)

        else:
            self.errorLabel.text="Something's wrong with the link!"
            self.errorLabel.adaptive_size
            self.errorLabel.pos_hint={"center_x":0.5, "center_y":0.35}

    def convert(self,event,layout):
        self.ys = self.yt.streams.get_audio_only()
        print("Convertion in progress!")
        if self.ys.download("C:/Users/dns/Desktop/applications/YouTube AudioGrabber/audio_files"):
            self.prog=self.progress.value
            self.prog+=100
            self.progress.value=self.prog
            self.acom.text="Download's been completed!"
            self.acom.pos_hint={'center_x':0.5, "center_y":0.25}
            print("Convertion is acomplished!")
        else:
            print("Fail!")



    def vidDownload(self,event,layout):
        self.ys2=self.yt.streams.filter(file_extension="mp4").filter(resolution=self.main_Button.text).first()
        print("Video-downloading in process!")
        self.ys2.download("C:/Users/dns/Desktop/applications/YouTube AudioGrabber/video_files")
        self.prog=self.progress.value
        self.prog+=100
        self.progress.value=self.prog
        self.acom.text="Download's been completed!"
        self.acom.pos_hint={'center_x':0.5, "center_y":0.25}
        print("Download is complete!")




    def build(self):
        layout = MDRelativeLayout(md_bg_color = [79/255, 74/255, 74/255])
        self.img=Image(source="C:/Users/dns/Desktop/applications/YouTube AudioGrabber/YT1.jpg", size_hint=(.7, .7), pos_hint={"center_x": 0.5, "center_y": 0.85})

        self.fileLink=MDLabel(text="Enter the link to the video", size_hint=(1,1),  font_size=30, theme_text_color="Custom", text_color="#e02222", pos_hint={"center_x":0.5, "center_y":.60})

        self.linkField=MDTextField(text="", hint_text="Enter your link", helper_text_mode="on_focus", size_hint=(1, None), height=48, font_size=29, foreground_color=(0, .5, 0),
        font_name='Comic', pos_hint={"center_x":0.5, "center_y":0.66})

        self.linkButton=Button(text="Link Info", size_hint=(.2, .1), font_name='Comic',  font_size=24,
        color=('#332424'), pos_hint={"center_x":0.2, "center_y":0.5})
        self.linkButton.bind(on_press=partial(self.getLinkInfo,layout))
        #self.linkButton.bind(on_press=partial(self.on_state,layout))

        self.convertButton=Button(text="Convert", size_hint=(.2,.1), font_name="Comic", font_size=23, color=('#332424'),
        pos_hint={"center_x":0.5, "center_y":0.5})
        self.convertButton.bind(on_press=partial(self.convert,layout))

        self.videoButton=Button(text="Download \n Video", size_hint=(.2,.1), font_name="Comic", font_size=23, color=('#332424'),
        pos_hint={"center_x":0.8, "center_y":0.5})
        self.videoButton.bind(on_press=partial(self.vidDownload,layout))

        self.myLabel=MDLabel(text="developed by Arefkin R", size_hint=(0.2,0.2),
        font_size=15, theme_text_color="Custom", text_color="#e02222", text_size=(0.2,0.2), pos_hint={"center_x":0.9, "center_y":.05} )

        self.progress=MDProgressBar( value=(0), color="red", pos_hint={"center_x":0.3, "center_y":0.3})
        self.acom=MDLabel(text="", size_hint=(1,1), font_size=30, theme_text_color="Custom",text_color="#e02222",
        pos_hint={"center_x":0.5, "center_y":20})

        self.errorLabel=MDLabel(text="", size_hint=(1,1), font_size=30, theme_text_color="Custom",text_color="#e02222", pos_hint={"center_x":0.5, "center_y":20})

        self.titelLabel=MDLabel(text="", size_hint=(1,1), font_size=25, theme_text_color="Custom", text_color="#e02222", pos_hint={"center_x":0.5, "center_y":20})



        layout.add_widget(self.fileLink)
        layout.add_widget(self.img)
        layout.add_widget(self.linkField)
        layout.add_widget(self.linkButton)
        layout.add_widget(self.convertButton)
        layout.add_widget(self.videoButton)
        layout.add_widget(self.titelLabel)
        layout.add_widget(self.errorLabel)
        layout.add_widget(self.myLabel)
        layout.add_widget(self.progress)
        layout.add_widget(self.acom)
        return layout


if __name__ =="__main__":
    MyApp().run()
from kivy.app import App
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.uix.textinput import TextInput

import Characterization.Linearity as lin
import Sullivan_Thomas.Thomas as th
import Characterization.Detectors.Rate_and_Efficiencies_scripts.PlotAll as pa
import Characterization.Detectors.Rate_and_Efficiencies_scripts.Plot3D as p3d
import Common_Utilities.OpenPickle as op


class Thomas(Screen):
    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'muons'
        self.manager.get_screen('muons')

    def init(self, infoDict):
        for key, val in self.ids.items():
            val.text = str(infoDict[key]) + ' +/- ' + str(infoDict['Err_{}'.format(key)]) if infoDict else ''

    def plot(self):
        th.show()


class Muons(Screen):

    def thomas(self):
        infoDict = th.main()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'thomas'
        self.manager.get_screen('thomas').init(infoDict)

    def linearity(self):
        lin.main()

    def plotAll(self):
        pa.main()

    def plot3D(self):
        p3d.main()

    def openPickle(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'openPickle'
        self.manager.get_screen('openPickle')


class OpenPickle(Screen):

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'muons'
        self.manager.get_screen('muons')

    def choice(self, opt):
        op.openPickle(opt)


class MuonsApp(App):

    def build(self):
        manager = ScreenManager()
        manager.add_widget(Muons(name='muons'))
        manager.add_widget(OpenPickle(name='openPickle'))
        manager.add_widget(Thomas(name='thomas'))
        return manager


if __name__ == '__main__':
    MuonsApp().run()

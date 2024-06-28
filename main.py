import os
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

class MusicApp(App):

    title = 'M-music'

    def build(self):
        # Добавляем Label с Instagram
        self.instagram_label = Label(
            text="@murid.py",
            size_hint=(1, 0.1),
            color=(1, 1, 1, 0.5),  # Белый цвет с 50% прозрачностью
            font_size='18sp',
            halign='center'
        )

        self.label = Label(
            text="Select track",
            size_hint=(.5, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        self.label_M = Label(
            text="M-music",
            size_hint=(1, 0.2),
            font_size='24sp',
            bold=True,
            padding_y=50
        )

        main_layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            padding=(0, 20, 0, 0)
        )

        top_layout.add_widget(self.label_M)

        boxlayout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9),
            pos_hint={'center_x': 0.5, 'y': 0}
        )

        scroll_view = ScrollView()

        grid_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            padding=(5, 5, 5, 3),
            spacing=(10, 5)
        )
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        audio_files = self.get_audio_files()
        if not audio_files:
            self.label.text = "No available audio!"
        else:
            for audio_file in audio_files:
                btn = Button(
                    text=audio_file,
                    size_hint=(1, None),
                    height=40,
                    background_color=[.28, .24, .99, 1],
                    background_normal='',
                    halign='center',  # Оставляем выравнивание по центру
                    valign='middle',
                    font_size='13sp',
                    text_size=(None, None),
                    padding=(10, 0)  # Отступ слева (10 пикселей)
                )

                btn.bind(on_press=self.play_audio)
                btn.bind(on_size=lambda instance, size: setattr(instance, 'text_size', (size[0], None)))
                grid_layout.add_widget(btn)

        self.current_sound = None

        # Create a horizontal BoxLayout for the buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            spacing=10,
            padding=(10, 10)
        )

        self.play_button = Button(text='Play', size_hint=(0.5, 1))
        self.play_button.bind(on_press=self.play_pause_audio)

        self.stop_button = Button(text='Stop', size_hint=(0.5, 1))
        self.stop_button.bind(on_press=self.stop_audio)

        button_layout.add_widget(self.play_button)
        button_layout.add_widget(self.stop_button)

        boxlayout.add_widget(self.label)
        scroll_view.add_widget(grid_layout)
        boxlayout.add_widget(scroll_view)

        main_layout.add_widget(self.instagram_label)  # Add Instagram label at the top
        main_layout.add_widget(top_layout)
        main_layout.add_widget(boxlayout)
        main_layout.add_widget(button_layout)  # Add the button layout

        return main_layout

    def play_audio(self, instance):
        audio_file = instance.text
        self.label.text = f"playing: {audio_file}"

        # Используем относительный путь к аудиофайлам
        audio_folder = os.path.join(os.path.dirname(__file__), 'audio')
        sound_path = os.path.join(audio_folder, audio_file)

        if self.current_sound:
            self.current_sound.stop()
            self.play_button.disabled = False

        self.current_sound = SoundLoader.load(sound_path)
        if self.current_sound:
            self.current_sound.play()
            self.play_button.disabled = True
        else:
            self.label.text = f"failed to load: {audio_file}"

    def play_pause_audio(self, instance):
        if self.current_sound:
            if self.current_sound.state == 'play':
                self.current_sound.pause()
                self.play_button.disabled = False
            else:
                self.current_sound.play()
                self.play_button.disabled = True

    def stop_audio(self, instance):
        if self.current_sound:
            self.current_sound.stop()
            self.play_button.disabled = False

    def get_audio_files(self):
        audio_files = []

        # Используем относительный путь к аудиофайлам
        audio_folder = os.path.join(os.path.dirname(__file__), 'audio')
        if os.path.exists(audio_folder):
            for file in os.listdir(audio_folder):
                if file.endswith('.mp3'):
                    audio_files.append(file)
        else:
            self.label.text = f"folder is not found"
        return audio_files

if __name__ == '__main__':
    MusicApp().run()

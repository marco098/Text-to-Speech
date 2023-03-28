import os
import eyed3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
from gtts import gTTS

class TextToSpeech(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 500, 200)
        self.setWindowTitle('Text-to-Speech')
        
        # Label per il percorso del file di testo
        self.label_file_path = QLabel(self)
        self.label_file_path.setGeometry(20, 20, 200, 30)
        self.label_file_path.setText('File di testo:')
        
        # LineEdit per il percorso del file di testo
        self.edit_file_path = QLineEdit(self)
        self.edit_file_path.setGeometry(120, 20, 300, 30)
        
        # Pulsante per selezionare il file di testo
        self.btn_select_file = QPushButton(self)
        self.btn_select_file.setGeometry(430, 20, 60, 30)
        self.btn_select_file.setText('...')
        self.btn_select_file.clicked.connect(self.selectFile)
        
        # ComboBox per selezionare la lingua
        self.combo_language = QComboBox(self)
        self.combo_language.setGeometry(20, 70, 200, 30)
        self.combo_language.addItem('Inglese', 'en')
        self.combo_language.addItem('Italiano', 'it')
        
        # Pulsante per generare l'audio
        self.btn_generate_audio = QPushButton(self)
        self.btn_generate_audio.setGeometry(20, 120, 200, 30)
        self.btn_generate_audio.setText('Genera audio')
        self.btn_generate_audio.clicked.connect(self.generateAudio)
        
        # Label per lo stato del processo di generazione audio
        self.label_status = QLabel(self)
        self.label_status.setGeometry(240, 120, 250, 30)
        self.label_status.setAlignment(Qt.AlignRight)
        self.label_status.setText('')

    def selectFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleziona file di testo", "", "File di testo (*.txt)", options=options)
        if file_name:
            self.edit_file_path.setText(file_name)
    
    def generateAudio(self):
        file_path = self.edit_file_path.text()
        if not os.path.exists(file_path):
            self.label_status.setText('File non trovato')
            return
        
        language = self.combo_language.currentData()
        audio_file_path = os.path.splitext(file_path)[0] + '.mp3'
        tts = gTTS(text=open(file_path, 'r').read(), lang=language)
        
        self.label_status.setText('Generazione audio in corso...')
        tts.save(audio_file_path)

        # Scrivi le informazioni avanzate del file audio MP3
        audio_file = eyed3.load(audio_file_path)
        audio_file.initTag()
        audio_file.tag.artist = "marco098 on GITHUB!"
        audio_file.tag.title = os.path.splitext(os.path.basename(file_path))[0]
        audio_file.tag.save()

        self.label_status.setText('Audio generato correttamente')

if __name__ == '__main__':
    app = QApplication([])
    window = TextToSpeech()
    window.show()
    app.exec_()

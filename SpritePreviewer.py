import math
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


# Function to load sprite images form a folder
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    # Calculate the padding needed for filenames
    padding = math.ceil(math.log10(number_of_frames))
    for frame in range(number_of_frames):
        # Create the file name for each frame and load it as a QPixmap
        file_name = f"{sprite_folder_name}/sprite_{str(frame).zfill(padding)}.png"
        frames.append(QPixmap(file_name))
    return frames


class SpritePreview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")

        # Basic sprite Setup
        self.num_frames = 12   # Total number of frames in the animation
        self.frames = load_sprite("spriteImages", self.num_frames)   # Load the sprite images
        self.current_frame = 0   # Start with the first frame
        self.is_playing = False   # Animations starts in a paused state
        self.fps = 10   # Default FPS

        # Timer for controlling the animation speed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sprite)   # Call update_sprite repeatedly

        # Build the user interface
        self.setupUI()

    def setupUI(self):
        # Create the central widget and set its layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Label to display the sprite images
        self.sprite_label = QLabel("No Sprite loaded")
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)   # center align the sprite
        self.sprite_label.setFixedSize(200, 200)   # set a fixed size for the display
        main_layout.addWidget(self.sprite_label)

        # Layout for the slider and FPS controls
        slider_layout = QHBoxLayout()

        # Label showing the current FPS controls
        self.fps_label = QLabel(f"FPS: {self.fps}")
        slider_layout.addWidget(self.fps_label)


        # Slider to control FPS (frames per second)
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setRange(1, 60)  # Allow FPS to be adjusted between 1 and 60
        self.fps_slider.setValue(self.fps)   # start with the default FPS
        self.fps_slider.valueChanged.connect(self.update_fps)   # Connect slider changes to update_fps

        # 슬라이더 눈금 추가
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(10)
        slider_layout.addWidget(self.fps_slider)

        fps_text_label = QLabel("Frames per second")
        slider_layout.addWidget(fps_text_label)
        main_layout.addLayout(slider_layout)

        # Start/Stop 버튼
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)
        main_layout.addWidget(self.start_stop_button)

        # 메뉴 추가
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)
        file_menu.addAction(pause_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # 스프라이트 이미지를 업데이트
    def update_sprite(self):
        if self.frames:
            pixmap = self.frames[self.current_frame]
            self.sprite_label.setPixmap(pixmap)
            self.current_frame = (self.current_frame + 1) % self.num_frames

    # FPS 슬라이더 변경
    def update_fps(self, value):
        self.fps = value
        self.fps_label.setText(f"FPS: {self.fps}")
        if self.is_playing:
            self.timer.setInterval(1000 // self.fps)

    # Start/Stop 버튼 기능
    def toggle_animation(self):
        if self.is_playing:
            self.timer.stop()
            self.start_stop_button.setText("Start")
        else:
            self.timer.start(1000 // self.fps)
            self.start_stop_button.setText("Stop")
        self.is_playing = not self.is_playing

    # Pause 메뉴 동작
    def pause_animation(self):
        self.timer.stop()
        self.is_playing = False
        self.start_stop_button.setText("Start")


def main():
    app = QApplication([])
    window = SpritePreview()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

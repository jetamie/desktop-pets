import sys
import random
import os
import json
from datetime import datetime, time
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtCore import (Qt, QTimer, QPoint, QRect, QEvent, QObject)

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.screen_geometry = QApplication.desktop().availableGeometry()
        self.pet_size = 256
        self.setGeometry(QRect(0, 0, self.pet_size, self.pet_size))
        
        self.current_state = 'idle'
        self.current_frame = 0
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_frame)
        
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.auto_move)
        
        self.is_moving = False
        self.move_target_x = 0
        self.move_target_y = 0
        
        self.load_greetings_config()
        self.load_frames()
        self.init_greeting_label()
        self.move_to_corner()
        
        self.show()
    
    def load_greetings_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'greetings.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.greetings = config.get('greetings', [])
                self.greeting_interval = config.get('interval_seconds', 30) * 1000
                self.greeting_duration = config.get('display_duration_seconds', 5) * 1000
                self.move_speed = config.get('move_speed', 3)
                self.idle_timeout = config.get('idle_timeout_seconds', 5) * 1000
                self.current_pet = config.get('current_pet', 'cat')
                self.pet_size = config.get('pet_size', 64)
                self.animation_interval = config.get('animation_interval_ms', 150)
        except Exception as e:
            print(f"加载问候语配置失败: {e}")
            self.greetings = ["你好！", "今天过得怎么样？"]
            self.greeting_interval = 30000
            self.greeting_duration = 5000
            self.move_speed = 3
            self.idle_timeout = 5000
            self.current_pet = 'cat'
            self.pet_size = 64
            self.animation_interval = 150
        
        print(f"当前宠物: {self.current_pet}")
        if isinstance(self.greetings, dict):
            print(f"问候语时段: {list(self.greetings.keys())}")
        else:
            print(f"问候语列表: {self.greetings}")
        print(f"问候间隔: {self.greeting_interval}ms")
        print(f"显示时长: {self.greeting_duration}ms")
        print(f"移动速度: {self.move_speed}")
        print(f"空闲超时: {self.idle_timeout}ms")
        print(f"宠物大小: {self.pet_size}x{self.pet_size}")
        print(f"动画间隔: {self.animation_interval}ms")
        
        self.animation_timer.start(self.animation_interval)
        
        self.greeting_timer = QTimer(self)
        self.greeting_timer.timeout.connect(self.show_random_greeting)
        self.greeting_timer.start(self.greeting_interval)
        
        self.idle_timer.start(self.idle_timeout)
    
    def init_greeting_label(self):
        self.greeting_label = QLabel()
        self.greeting_label.setFont(QFont("Microsoft YaHei", 12))
        self.greeting_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.7);
                color: #333333;
                padding: 4px 6px;
                border-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        self.greeting_label.setWordWrap(True)
        self.greeting_label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.greeting_label.hide()
        
        self.greeting_hide_timer = QTimer(self)
        self.greeting_hide_timer.setSingleShot(True)
        self.greeting_hide_timer.timeout.connect(self.hide_greeting)
    
    def get_time_period(self):
        now = datetime.now().time()
        # 夜间：20:00 - 05:00（跨天）
        if now >= time(20, 0) or now < time(5, 0):
            return "night"
        elif now < time(11, 30):
            return "morning"
        elif now < time(13, 30):
            return "noon"
        elif now < time(18, 0):
            return "afternoon"
        else:
            return "evening"
    
    def show_random_greeting(self):
        if not self.greetings:
            print("没有问候语")
            return
        
        time_period = self.get_time_period()
        period_greetings = self.greetings.get(time_period, [])
        
        if not period_greetings:
            period_greetings = self.greetings.get('morning', [])
        
        if not period_greetings:
            print("没有问候语")
            return
        
        greeting = random.choice(period_greetings)
        print(f"显示问候语 ({time_period}): {greeting}")
        
        self.greeting_label.setText(greeting)
        self.greeting_label.adjustSize()
        
        pet_x = self.x()
        pet_y = self.y()
        label_width = self.greeting_label.width()
        label_height = self.greeting_label.height()
        
        label_x = pet_x - label_width + self.pet_size // 2
        label_y = pet_y - label_height - 10
        
        if label_x < 0:
            label_x = pet_x + self.pet_size
        if label_y < 0:
            label_y = pet_y + self.pet_size + 10
        
        self.greeting_label.move(label_x, label_y)
        self.greeting_label.show()
        
        self.greeting_hide_timer.start(self.greeting_duration)
    
    def hide_greeting(self):
        self.greeting_label.hide()
    
    def load_frames(self):
        self.frames = {}
        self.pet_name = '默认宠物'
        
        pets_base_path = os.path.join(os.path.dirname(__file__), 'assets', 'pets')
        pet_path = os.path.join(pets_base_path, self.current_pet)
        config_path = os.path.join(pet_path, 'config.json')
        
        default_path = os.path.join(os.path.dirname(__file__), 'assets', 'images')
        
        pet_config = None
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    pet_config = json.load(f)
                    self.pet_name = pet_config.get('name', '默认宠物')
                    if not hasattr(self, 'pet_size') or self.pet_size == 64:
                        self.pet_size = pet_config.get('size', 64)
                    self.setGeometry(QRect(0, 0, self.pet_size, self.pet_size))
            except Exception as e:
                print(f"加载宠物配置失败: {e}")
        
        load_path = pet_path if os.path.exists(pet_path) else default_path
        
        default_frames_config = {
            'idle': ['idle_0.png', 'idle_1.png', 'idle_2.png'],
            'walk': ['walk_0.png', 'walk_1.png', 'walk_2.png', 'walk_3.png'],
            'jump': ['jump_0.png', 'jump_1.png', 'jump_2.png', 'jump_3.png']
        }
        
        frames_config = {}
        if pet_config and 'frames' in pet_config:
            frames_config = pet_config['frames']
        else:
            frames_config = default_frames_config
        
        for state, frame_files in frames_config.items():
            frames = []
            for frame_file in frame_files:
                path = os.path.join(load_path, frame_file)
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    frames.append(pixmap)
            self.frames[state] = frames
        
        if pet_config and 'frames' in pet_config:
            print(f"帧配置: 从宠物配置文件加载")
        else:
            print(f"帧配置: 使用默认配置")
        
        print(f"加载宠物: {self.pet_name}")
        print(f"宠物尺寸: {self.pet_size}x{self.pet_size}")
    
    def update_frame(self):
        frames = self.frames.get(self.current_state, self.frames['idle'])
        if frames:
            self.current_frame = (self.current_frame + 1) % len(frames)
        self.update()
        
        if self.is_moving:
            self.move_towards_target()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        frames = self.frames.get(self.current_state, self.frames['idle'])
        if frames:
            current_pixmap = frames[self.current_frame % len(frames)]
            painter.drawPixmap(0, 0, self.pet_size, self.pet_size, current_pixmap)
    
    def move_to_corner(self):
        x = self.screen_geometry.width() - self.pet_size - 20
        y = self.screen_geometry.height() - self.pet_size - 100
        self.move(x, y)
    
    def move_towards_target(self):
        old_x = self.x()
        old_y = self.y()
        dx = self.move_target_x - old_x
        dy = self.move_target_y - old_y
        
        step = self.move_speed
        new_x = old_x
        new_y = old_y
        
        if abs(dx) > step:
            new_x += step * (1 if dx > 0 else -1)
        if abs(dy) > step:
            new_y += step * (1 if dy > 0 else -1)
        
        self.move(new_x, new_y)
        
        if self.greeting_label.isVisible():
            offset_x = new_x - old_x
            offset_y = new_y - old_y
            self.greeting_label.move(
                self.greeting_label.x() + offset_x,
                self.greeting_label.y() + offset_y
            )
        
        if abs(dx) <= step and abs(dy) <= step:
            self.is_moving = False
            self.current_state = 'idle'
            self.idle_timer.start(self.idle_timeout)
    
    def auto_move(self):
        if self.is_moving or self.current_state == 'jump':
            return
        
        padding = 50
        max_x = self.screen_geometry.width() - self.pet_size - padding
        max_y = self.screen_geometry.height() - self.pet_size - padding
        
        self.move_target_x = random.randint(padding, max_x)
        self.move_target_y = random.randint(padding, max_y)
        
        self.is_moving = True
        self.current_state = 'walk'
        self.idle_timer.stop()
    
    def do_jump(self):
        if self.current_state == 'jump':
            return
        
        padding = 50
        max_x = self.screen_geometry.width() - self.pet_size - padding
        max_y = self.screen_geometry.height() - self.pet_size - padding
        
        self.move_target_x = random.randint(padding, max_x)
        self.move_target_y = random.randint(padding, max_y)
        
        self.current_state = 'jump'
        self.idle_timer.stop()
        
        jump_complete_timer = QTimer(self)
        jump_complete_timer.setSingleShot(True)
        jump_complete_timer.timeout.connect(self.on_jump_complete)
        jump_complete_timer.start(600)
    
    def on_jump_complete(self):
        self.is_moving = True
        self.current_state = 'walk'

class EventFilter(QObject):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                global_pos = event.globalPos()
                pet_rect = QRect(self.pet.pos(), self.pet.size())
                if pet_rect.contains(global_pos):
                    self.pet.do_jump()
                    self.pet.idle_timer.start(self.pet.idle_timeout)
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    event_filter = EventFilter(pet)
    app.installEventFilter(event_filter)
    sys.exit(app.exec_())
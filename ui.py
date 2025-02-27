import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel, QComboBox,
    QPushButton, QListWidget, QTabWidget, QDateEdit, QHBoxLayout, QSplitter, QFrame, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import json
from PyQt5.QtCore import Qt, QSize
from PyQt6.QtCore import Qt, QSize

class StudyManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("个人学习管理工具")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_study_notes_tab()
        self.create_mistakes_tab()
        self.create_key_points_tab()
        self.create_mood_diary_tab()
        self.create_schedule_tab()

    def create_study_notes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("学习笔记 - 选择学科"))
        self.notes_subject = QComboBox()
        self.notes_subject.addItems(["数学", "物理", "化学", "英语", "编程", "其他"])
        layout.addWidget(self.notes_subject)

        self.notes_text = QTextEdit()
        layout.addWidget(self.notes_text)

        self.save_notes_button = QPushButton("保存笔记")
        self.save_notes_button.clicked.connect(self.save_note)
        layout.addWidget(self.save_notes_button)

        self.notes_list = QListWidget()
        layout.addWidget(self.notes_list)
        self.load_notes()

        self.delete_notes_button = QPushButton("删除选中笔记")
        self.delete_notes_button.clicked.connect(self.delete_note)
        layout.addWidget(self.delete_notes_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "学习笔记")

    def save_note(self):
        subject = self.notes_subject.currentText()
        note = self.notes_text.toPlainText()
        if note.strip():
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO study_notes (subject, note, date) VALUES (?, ?, DATE('now'))", (subject, note))
            conn.commit()
            conn.close()
            self.load_notes()
            QMessageBox.information(self, "成功", "学习笔记已保存！")

    def load_notes(self):
        self.notes_list.clear()
        conn = sqlite3.connect("study_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, subject, note, date FROM study_notes")
        self.notes_data = cursor.fetchall()
        for row in self.notes_data:
            self.notes_list.addItem(f"[{row[3]}] {row[1]}: {row[2]}")
        conn.close()

    def delete_note(self):
        selected_item = self.notes_list.currentRow()
        if selected_item != -1:
            note_id = self.notes_data[selected_item][0]
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM study_notes WHERE id = ?", (note_id,))
            conn.commit()
            conn.close()
            self.load_notes()
            QMessageBox.information(self, "成功", "学习笔记已删除！")

    def create_mistakes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("错题整理 - 选择学科"))
        self.mistake_subject = QComboBox()
        self.mistake_subject.addItems(["数学", "物理", "化学", "英语", "编程", "其他"])
        layout.addWidget(self.mistake_subject)

        self.mistake_text = QTextEdit()
        layout.addWidget(self.mistake_text)

        self.save_mistake_button = QPushButton("保存错题")
        self.save_mistake_button.clicked.connect(self.save_mistake)
        layout.addWidget(self.save_mistake_button)

        self.mistakes_list = QListWidget()
        layout.addWidget(self.mistakes_list)
        self.load_mistakes()

        self.delete_mistake_button = QPushButton("删除选中错题")
        self.delete_mistake_button.clicked.connect(self.delete_mistake)
        layout.addWidget(self.delete_mistake_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "错题整理")

    def save_mistake(self):
        subject = self.mistake_subject.currentText()
        mistake = self.mistake_text.toPlainText()
        if mistake.strip():
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mistakes (subject, mistake) VALUES (?, ?)", (subject, mistake))
            conn.commit()
            conn.close()
            self.load_mistakes()
            QMessageBox.information(self, "成功", "错题已保存！")

    def load_mistakes(self):
        self.mistakes_list.clear()
        conn = sqlite3.connect("study_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, subject, mistake FROM mistakes")
        self.mistakes_data = cursor.fetchall()
        for row in self.mistakes_data:
            self.mistakes_list.addItem(f"{row[1]}: {row[2]}")
        conn.close()

    def delete_mistake(self):
        selected_item = self.mistakes_list.currentRow()
        if selected_item != -1:
            mistake_id = self.mistakes_data[selected_item][0]
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mistakes WHERE id = ?", (mistake_id,))
            conn.commit()
            conn.close()
            self.load_mistakes()
            QMessageBox.information(self, "成功", "错题已删除！")

    def create_key_points_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("主要知识点 - 选择学科"))
        self.key_point_subject = QComboBox()
        self.key_point_subject.addItems(["数学", "物理", "化学", "英语", "编程", "其他"])
        layout.addWidget(self.key_point_subject)

        self.key_point_text = QTextEdit()
        layout.addWidget(self.key_point_text)

        self.save_key_point_button = QPushButton("保存知识点")
        self.save_key_point_button.clicked.connect(self.save_key_point)
        layout.addWidget(self.save_key_point_button)

        self.key_points_list = QListWidget()
        layout.addWidget(self.key_points_list)
        self.load_key_points()

        self.delete_key_point_button = QPushButton("删除选中知识点")
        self.delete_key_point_button.clicked.connect(self.delete_key_point)
        layout.addWidget(self.delete_key_point_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "主要知识点")

    def save_key_point(self):
        subject = self.key_point_subject.currentText()
        key_point = self.key_point_text.toPlainText()
        if key_point.strip():
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO key_points (subject, key_point) VALUES (?, ?)", (subject, key_point))
            conn.commit()
            conn.close()
            self.load_key_points()
            QMessageBox.information(self, "成功", "知识点已保存！")

    def load_key_points(self):
        self.key_points_list.clear()
        conn = sqlite3.connect("study_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, subject, key_point FROM key_points")
        self.key_points_data = cursor.fetchall()
        for row in self.key_points_data:
            self.key_points_list.addItem(f"{row[1]}: {row[2]}")
        conn.close()

    def delete_key_point(self):
        selected_item = self.key_points_list.currentRow()
        if selected_item != -1:
            key_point_id = self.key_points_data[selected_item][0]
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM key_points WHERE id = ?", (key_point_id,))
            conn.commit()
            conn.close()
            self.load_key_points()
            QMessageBox.information(self, "成功", "知识点已删除！")

    def create_mood_diary_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("个人情绪日记 - 选择日期"))
        self.date_picker = QDateEdit()
        layout.addWidget(self.date_picker)

        self.mood_text = QTextEdit()
        layout.addWidget(self.mood_text)

        self.save_mood_button = QPushButton("保存日记")
        self.save_mood_button.clicked.connect(self.save_mood)
        layout.addWidget(self.save_mood_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "个人情绪日记")

    def save_mood(self):
        mood = self.mood_text.toPlainText()
        date = self.date_picker.text()
        if mood.strip():
            conn = sqlite3.connect("study_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mood_diary (mood, date) VALUES (?, ?)", (mood, date))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "成功", "情绪日记已保存！")

    def create_schedule_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.schedule_label = QLabel("暂无课程表图片")
        layout.addWidget(self.schedule_label)

        self.upload_schedule_button = QPushButton("导入课程表图片")
        self.upload_schedule_button.clicked.connect(self.upload_schedule_image)
        layout.addWidget(self.upload_schedule_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "课程表")

        # 加载之前保存的图片（如果有）
        self.load_schedule_image()

    def upload_schedule_image(self):
        try:
            # 弹出文件对话框选择图片
            file_path, _ = QFileDialog.getOpenFileName(self, "选择课程表图片", "",
                                                       "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

            if not file_path:
                return  # 如果没有选择文件，直接返回

            # 保存图片路径到文件
            self.save_schedule_image_path(file_path)

            # 加载并显示图片
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "错误", "无法加载图片，请选择有效的图片文件！")
                return

            # 将图片自适应 QLabel
            label_size = self.schedule_label.size()  # 获取 QLabel 当前的大小
            scaled_pixmap = pixmap.scaled(QSize(label_size.width(), label_size.height()),
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)  # 使用 QSize 和正确的模式
            self.schedule_label.setPixmap(scaled_pixmap)
            self.schedule_label.setText("")  # 清空文本提示

        except Exception as e:
            QMessageBox.critical(self, "异常", f"发生错误: {str(e)}")

    def save_schedule_image_path(self, file_path):
        try:
            # 将图片的路径保存到本地文件
            with open("schedule_image.json", "w") as file:
                json.dump({"image_path": file_path}, file)
        except Exception as e:
            QMessageBox.warning(self, "保存错误", f"无法保存图片路径: {str(e)}")

    def load_schedule_image(self):
        # 加载图片路径，并显示图片
        if os.path.exists("schedule_image.json"):
            try:
                with open("schedule_image.json", "r") as file:
                    data = json.load(file)
                    image_path = data.get("image_path")

                    if image_path and os.path.exists(image_path):
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            # 将图片自适应 QLabel
                            label_size = self.schedule_label.size()  # 获取 QLabel 当前的大小
                            scaled_pixmap = pixmap.scaled(QSize(label_size.width(), label_size.height()),
                                                          Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)
                            self.schedule_label.setPixmap(scaled_pixmap)
                            self.schedule_label.setText("")  # 清空文本提示
            except Exception as e:
                QMessageBox.warning(self, "加载错误", f"无法加载图片路径: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyManager()
    window.show()
    sys.exit(app.exec())

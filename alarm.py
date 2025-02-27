from apscheduler.schedulers.background import BackgroundScheduler
from PyQt6.QtWidgets import QMessageBox

def reminder():
    """显示学习提醒"""
    msg = QMessageBox()
    msg.setWindowTitle("学习提醒")
    msg.setText("提醒：该学习了！")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

def start_alarm():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reminder, 'interval', minutes=30)  # 每 30 分钟提醒
    scheduler.start()

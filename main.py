import sys
from PyQt6.QtWidgets import QApplication
from ui import StudyManager
import database
import alarm

if __name__ == "__main__":
    database.init_db()  # 初始化数据库
    alarm.start_alarm()  # 启动闹钟提醒

    app = QApplication(sys.argv)
    window = StudyManager()
    window.show()
    sys.exit(app.exec())

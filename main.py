from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QColor
import sys

class TimeTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemClicked.connect(self.log_time)

        self.setColumnCount(7)
        self.setRowCount(24)

        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.hours = [str(i) for i in range(24)]

        # 헤더 아이템 생성
        for i in range(7):
            day_item = QTableWidgetItem(self.days[i])
            self.setHorizontalHeaderItem(i, day_item)

        for i in range(24):
            hour_item = QTableWidgetItem(self.hours[i])
            self.setVerticalHeaderItem(i, hour_item)

        # 각 셀에 기본 QTableWidgetItem 생성
        for i in range(24):
            for j in range(7):
                self.setItem(i, j, QTableWidgetItem())

        # 불가능한 시간을 저장하는 리스트
        self.unavailable_hours = []

    def log_time(self, item):
        column = item.column()
        row = item.row()
        # Check if the header items for the given indexes exist
        day_item = self.horizontalHeaderItem(column)
        hour_item = self.verticalHeaderItem(row)
        if day_item is not None and hour_item is not None:
            day = day_item.text()
            hour = hour_item.text()

            selected_time = (day, hour)
            if selected_time not in self.unavailable_hours:
                self.unavailable_hours.append(selected_time)
                item.setBackground(QColor('blue'))  # Change the cell color to blue
            else:
                self.unavailable_hours.remove(selected_time)  # If the time is clicked again, make it available
                item.setBackground(QColor('white'))  # Restore the cell color

            # print(f"Unavailable hours: {self.unavailable_hours}")
        else:
            print(f"Invalid index: column {column}, row {row}")

    def available_hours(self):
        available_hours_dict = {day: list(self.hours) for day in self.days}
        for (day, hour) in self.unavailable_hours:
            available_hours_dict[day].remove(hour)
        
        for day in available_hours_dict:
            print(f"Available hours on {day}: {available_hours_dict[day]}")

app = QApplication(sys.argv)

# Create TimeTable widget
table = TimeTable()

# Create QPushButton and connect it to the table's available_hours method
button = QPushButton("Show Available Hours")
button.clicked.connect(table.available_hours)

# Create a QVBoxLayout and add the table and the button to it
layout = QVBoxLayout()
layout.addWidget(table)
layout.addWidget(button)

# Create a QWidget, set its layout and show it
window = QWidget()
window.setLayout(layout)
window.resize(1280, 720)  # Set the window size to 1280x720 pixels
window.show()

sys.exit(app.exec_())

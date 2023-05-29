from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import sys

class TimeTable(QTableWidget):
    # Signal to emit when unavailable_hours changes
    unavailable_hours_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 아이템 클릭 발생 시, log_time 메소드 호출
        self.itemClicked.connect(self.log_time)

        # col, row 설정
        self.setColumnCount(7)
        self.setRowCount(24)

        # 날짜, 시간 설정
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.hours = [str(i) for i in range(24)]

        # 표 생성
        # 날짜
        for i in range(7):
            day_item = QTableWidgetItem(self.days[i])
            self.setHorizontalHeaderItem(i, day_item)

        # 시간
        for i in range(24):
            hour_item = QTableWidgetItem(self.hours[i])
            self.setVerticalHeaderItem(i, hour_item)

        # 각 셀에 기본 QTableWidgetItem 생성
        for i in range(24):
            for j in range(7):
                # 행, 열, QTableWidgetItem을 입력 받아 초기 테이블 비워둠
                self.setItem(i, j, QTableWidgetItem())

        # 불가능한 시간을 저장하는 리스트
        self.unavailable_hours = []
        self.last_clicked_item = None

        # QPushButton 생성
        self.btn_get_available_hours = QPushButton("Show Available Hours")
        self.btn_get_available_hours.clicked.connect(self.available_hours)

        self.btn_clear_available_hours = QPushButton("Clear")
        self.btn_clear_available_hours.clicked.connect(self.handle_item_clear)

    def log_time(self, item):
        # 현재 눌린 키를 확인,
        modifiers = QApplication.keyboardModifiers()
        # 쉬프트 키와 다른 키가 같이 눌렸는지 확인
        if modifiers == Qt.ShiftModifier and self.last_clicked_item is not None:
            # 시작 값
            start_row = min(item.row(), self.last_clicked_item.row())
            # 끝 값
            end_row = max(item.row(), self.last_clicked_item.row())

            # 현재 클릭 셀과 이전 클릭 셀의 열이 같은 열인가?
            if item.column() == self.last_clicked_item.column():
                # start부터 end까지 반복하면서 메소드 호출
                # 선택한 시간 처리 및 색상 변경
                for row in range(start_row, end_row + 1):
                    self.handle_item_click(self.item(row, item.column()))
        # 단일 셀을 눌렀을 때 실행
        else:
            self.handle_item_click(item)

        # 변수 업데이트, 이전에 클릭한 셀을 현재 클릭한 셀로 설정
        self.last_clicked_item = item
        self.unavailable_hours_changed.emit()

    # 클릭한 셀 처리
    def handle_item_click(self, item):
        # 클릭 행 인덱스 가져옴
        column = item.column()
        row = item.row()

        day_item = self.horizontalHeaderItem(column)
        hour_item = self.verticalHeaderItem(row)
        # 열과 행에 해당하는 헤더 아이템이 있는지 확인
        if day_item is not None and hour_item is not None:
            day = day_item.text()
            hour = hour_item.text()

            selected_time = (day, hour)

            # 선택한 시간 목록이 이전 선택 목록에 해당하는가?
            if selected_time not in self.unavailable_hours:
                self.unavailable_hours.append(selected_time)
                item.setBackground(QColor('blue'))  # 셀 색상을 파란색으로 변경
            else:
                self.unavailable_hours.remove(selected_time)  # 시간이 다시 클릭되면 가능한 시간으로 변경
                item.setBackground(QColor('white'))  # 셀 색상 복원
        self.unavailable_hours_changed.emit()


    # 셀 초기화
    def handle_item_clear(self):
        self.unavailable_hours = []
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item = self.item(row, column)
                item.setBackground(QColor('white'))
        self.unavailable_hours_changed.emit()  # Signal that unavailable_hours has changed

    # 가능 시간 조회
    def available_hours(self):
        # key : 요일, value : 모든 시간
        available_hours_dict = {day: list(self.hours) for day in self.days}
        # 불가능한 시간을 순회하며 dic에서 제거
        for (day, hour) in self.unavailable_hours:
            available_hours_dict[day].remove(hour)

        # 출력부
        for day in available_hours_dict:
            print(f"Available hours on {day}: {available_hours_dict[day]}")

    def load_unavailable_hours(self):
        for (day, hour) in self.unavailable_hours:
            column = self.days.index(day)
            row = self.hours.index(hour)

            item = self.item(row, column)
            item.setBackground(QColor('blue'))  # 셀 색상을 파란색으로 변경
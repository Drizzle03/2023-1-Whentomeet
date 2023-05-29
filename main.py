# 필요한 모듈을 임포트합니다.
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel, QStackedWidget
from PyQt5.QtCore import Qt, QItemSelectionModel
from api import TimeTable

class ListWidget(QWidget):
    def __init__(self):
        super().__init__()

        #윈도우 설정 (제목, 크기)
        self.setWindowTitle("When to meet")
        self.resize(1280, 720)  
        self.layout = QVBoxLayout() 

        self.saved_unavailable_hours = {} # 각 아이템의 불가능 시간 저장 dic
        self.new_windows = []  # 모든 새 창 참조 보관

        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(400)

        # place holder
        self.add_line_edit = QLineEdit()
        self.add_line_edit.setPlaceholderText("Enter an item")  # 새로운 리스트 이름 추가
        self.add_button = QPushButton("Add")  # Add 버튼
        self.add_button.clicked.connect(self.add_item)  # Add 버튼 클릭 시 add_item 메서드 호출

        # 선택된 리스트 삭제 버튼
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_item)  # remove_selected_item 메서드 호출
        self.remove_button.setMaximumHeight(50)  # 최대 높이 설정

        # 페이지 이동 버튼
        self.move_button = QPushButton("Move to Page")
        self.move_button.clicked.connect(self.move_to_page)  # move_to_page 메서드 호출
        self.move_button.setMaximumHeight(50)  # 최대 높이 설정

        # Stacked Widget 생성, 다른 위젯들을 스택처럼 쌓아놓음
        # 현재 페이지가 바뀔 때마다 update_current_page 메서드 호출
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.currentChanged.connect(self.update_current_page) 

        # 레이아웃 위젯 추가 (첫 번째 수평, place holder, add창 추가)
        self.layout.addWidget(self.list_widget)
        add_layout = QHBoxLayout() 
        add_layout.addWidget(self.add_line_edit) 
        add_layout.addWidget(self.add_button)  
        self.layout.addLayout(add_layout) 

        # 레이아웃 위젯 추가 (두 번째 수평, 삭제, 페이지 이동 창 추가)
        remove_move_layout = QHBoxLayout() 
        remove_move_layout.addWidget(self.remove_button)
        remove_move_layout.addWidget(self.move_button)
        self.layout.addLayout(remove_move_layout)

        self.layout.addWidget(self.stacked_widget)  # stacked_widget을 메인 레이아웃 추가

        self.setLayout(self.layout)

    def add_item(self):
        item_text = self.add_line_edit.text()  # 아이템 추가 입력창 텍스트 가져옴
        if item_text:  # 텍스트가 비어있지 않다면,
            self.list_widget.addItem(item_text)  # 텍스트를 리스트 위젯에 아이템으로 추가
            self.add_line_edit.clear()  # 아이템 추가 후 입력창을 비움

            page_label = QLabel() 
            self.stacked_widget.addWidget(page_label)  # stacked_widget에 페이지로 추가

            # 새 아이템의 사용 불가 시간 초기화
            self.saved_unavailable_hours[item_text] = []

    def remove_selected_item(self):
        selected_items = self.list_widget.selectedItems()  # 현재 선택된 아이템들을 가져옴
        for item in selected_items:  # 각 선택된 아이템에 대해
            row = self.list_widget.row(item)  # 아이템의 행 번호를 가져옴

            # 아이템을 삭제할 때 사용 불가 시간도 삭제
            del self.saved_unavailable_hours[item.text()]

            self.list_widget.takeItem(row)  # 아이템을 리스트 위젯에서 제거
            self.stacked_widget.removeWidget(self.stacked_widget.widget(row))  # 해당 아이템의 페이지를 stacked_widget에서 제거

    def move_to_page(self):
        selected_items = self.list_widget.selectedItems()  # 현재 선택된 아이템들을 가져옴
        if selected_items:  # 선택된 아이템이 있다면
            selected_item = selected_items[0]  # 첫 번째 선택된 아이템을 가져옴
            row = self.list_widget.row(selected_item)  # 선택된 아이템의 행 번호를 가져옴

            timetable_widget = TimeTable()  # TimeTable 위젯을 생성

            # 선택된 아이템에 대해 저장된 사용 불가 시간을 로드
            timetable_widget.unavailable_hours = self.saved_unavailable_hours[selected_item.text()]
            timetable_widget.load_unavailable_hours()

            # timetable_widget가 생성된 후에 신호를 연결합니다.
            timetable_widget.unavailable_hours_changed.connect(
                lambda: self.save_unavailable_hours(selected_item.text(), timetable_widget))

            # "Show Available Hours" 버튼을 생성하고, 이 버튼이 클릭되면 timetable_widget의 available_hours 메소드를 호출하도록 연결합니다.
            btn_get_available_hours = QPushButton("Show Available Hours")
            btn_get_available_hours.clicked.connect(timetable_widget.available_hours)

            # "Clear" 버튼을 생성하고, 이 버튼이 클릭되면 timetable_widget의 handle_item_clear 메소드를 호출하도록 연결합니다.
            btn_clear_available_hours = QPushButton("Clear")
            btn_clear_available_hours.clicked.connect(timetable_widget.handle_item_clear)

            new_window = QWidget()  # 새로운 윈도우를 생성합니다.
            layout = QVBoxLayout()  # 새로운 윈도우에 사용할 QVBoxLayout을 생성합니다.
            layout.addWidget(timetable_widget)  # timetable_widget을 레이아웃에 추가합니다.
            layout.addWidget(btn_get_available_hours)  # "Show Available Hours" 버튼을 레이아웃에 추가합니다.
            layout.addWidget(btn_clear_available_hours)  # "Clear" 버튼을 레이아웃에 추가합니다.
            new_window.setLayout(layout)  # 새로운 윈도우의 레이아웃을 방금 생성한 레이아웃으로 설정합니다.
            new_window.setWindowTitle(f"Timetable for {selected_item.text()}")  # 새로운 윈도우의 제목을 설정합니다.

            # 새 윈도우의 크기와 위치를 메인 윈도우와 동일하게 설정합니다.
            new_window.setGeometry(self.geometry())

            new_window.show()  # 새로운 윈도우를 보여줍니다.

            self.new_windows.append(new_window)  # 가비지 컬렉션을 방지하기 위해 새 윈도우에 대한 참조를 유지합니다.

    def update_current_page(self, index):
        self.list_widget.clearSelection()  # 리스트 위젯의 선택을 모두 해제합니다.
        if index >= 0:  # 인덱스가 유효하다면
            selection_model = self.list_widget.selectionModel()  # 리스트 위젯의 선택 모델을 가져옵니다.
            selection_model.select(self.list_widget.model().index(index, 0), QItemSelectionModel.Select)  # 새로운 페이지에 해당하는 아이템을 선택합니다.

    def save_unavailable_hours(self, item_text, timetable_widget):
            # 선택한 아이템에 대한 사용 불가능한 시간을 저장합니다.
            # timetable_widget의 사용 불가능한 시간 리스트를 복사하여 저장합니다.
            self.saved_unavailable_hours[item_text] = list(timetable_widget.unavailable_hours)


if __name__ == "__main__":
    app = QApplication([])  # QApplication 객체를 생성합니다. 이 객체는 프로그램 실행에 필요한 많은 것들을 관리합니다.
    widget = ListWidget()  # 사용자 정의 ListWidget 객체를 생성합니다.
    widget.show()  # ListWidget을 보여줍니다.
    app.exec_()  # 이벤트 루프를 시작합니다. 이는 사용자의 입력을 처리하고 GUI를 실행합니다.
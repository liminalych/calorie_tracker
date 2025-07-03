from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QLineEdit, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy, QComboBox, QToolButton, QFormLayout, QLabel
)
from PyQt6.QtCore import Qt

class MainWindowUI(QWidget):
    def __init__(self):
        super().__init__()

        # Основной лэйаут окна
        main_layout = QHBoxLayout(self)
        
        # Левая панель — продукты
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 2)  # Пропорция ширины

        self.list_products = QListWidget()
        left_layout.addWidget(QLabel("Продукты"))
        left_layout.addWidget(self.list_products)

        # Правая панель — дневной приём
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 3)  # Пропорция ширины

        # Верхняя часть — выбор даты и профиля
        top_row = QHBoxLayout()
        right_layout.addLayout(top_row)

        top_row.addWidget(QLabel("Дата:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDateTime(self.date_edit.dateTime().currentDateTime())
        top_row.addWidget(self.date_edit)

        # Добавим селектор профиля и кнопку (если надо, из твоих доработок)
        self.profile_selector = QComboBox()
        top_row.addWidget(QLabel("Профиль:"))
        top_row.addWidget(self.profile_selector)
        self.btn_add_profile = QToolButton()
        self.btn_add_profile.setText("+")
        top_row.addWidget(self.btn_add_profile)

        top_row.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Таблица дневного приёма — занимает всё оставшееся место
        self.table_daily = QTableWidget()
        right_layout.addWidget(self.table_daily)

        # В нужном месте, например, после self.table_daily:
        self.label_summary = QLabel("Итого: калории: 0, белки: 0, жиры: 0, углеводы: 0")
        self.label_summary.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.label_summary)

        # Важно: чтобы таблица растягивалась вместе с окном — 
        # она должна занимать всё доступное место в вертикальном лэйауте right_layout

        # Инициализация таблицы (заголовки)
        self.table_daily.setColumnCount(6)
        self.table_daily.setHorizontalHeaderLabels(["Продукт", "Кол-во (г)", "Ккал", "Белки", "Жиры", "Углеводы"])

        # Включаем адаптивное растяжение столбцов
        header = self.table_daily.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Для вертикального размера строк можно настроить ResizeToContents
        self.table_daily.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Настройки минимальных размеров, если надо
        self.table_daily.setMinimumWidth(400)
        self.table_daily.setMinimumHeight(300)

        # Левая панель - поля добавления продукта (пример)
        form_layout = QFormLayout()
        left_layout.addLayout(form_layout)
        self.input_name = QLineEdit()
        self.input_calories = QLineEdit()
        self.input_protein = QLineEdit()
        self.input_fat = QLineEdit()
        self.input_carbs = QLineEdit()

        form_layout.addRow("Название", self.input_name)
        form_layout.addRow("Калории (на 100г)", self.input_calories)
        form_layout.addRow("Белки (г)", self.input_protein)
        form_layout.addRow("Жиры (г)", self.input_fat)
        form_layout.addRow("Углеводы (г)", self.input_carbs)

        self.btn_add_product = QPushButton("Добавить продукт")
        left_layout.addWidget(self.btn_add_product)

        # Панель добавления в дневной приём
        intake_layout = QHBoxLayout()
        right_layout.addLayout(intake_layout)

        self.combo_products = QComboBox()
        self.input_quantity = QLineEdit()
        self.input_quantity.setPlaceholderText("Количество (г)")
        self.btn_add_entry = QPushButton("Добавить в дневной приём")

        intake_layout.addWidget(self.combo_products)
        intake_layout.addWidget(self.input_quantity)
        intake_layout.addWidget(self.btn_add_entry)

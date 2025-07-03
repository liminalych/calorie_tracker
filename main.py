from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QListWidgetItem,
    QInputDialog, QMenu, QHeaderView, QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QDialog
)
from PyQt6.QtCore import Qt
import sys
from database import Database
from ui_main import MainWindowUI

class ProductEditDialog(QDialog):
    def __init__(self, db, product_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.product_id = product_id
        self.setWindowTitle("Редактировать продукт")

        # Поля ввода
        self.input_name = QLineEdit()
        self.input_calories = QLineEdit()
        self.input_protein = QLineEdit()
        self.input_fat = QLineEdit()
        self.input_carbs = QLineEdit()

        # Разметка
        form = QFormLayout()
        form.addRow("Название", self.input_name)
        form.addRow("Калории (на 100г)", self.input_calories)
        form.addRow("Белки (г)", self.input_protein)
        form.addRow("Жиры (г)", self.input_fat)
        form.addRow("Углеводы (г)", self.input_carbs)

        # Кнопки
        btn_save = QPushButton("Сохранить")
        btn_cancel = QPushButton("Отмена")
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        form.addRow(btns)

        self.setLayout(form)
        self.load_product()

    def load_product(self):
        product = self.db.get_product(self.product_id)
        if product:
            _, name, cal, prot, fat, carb = product
            self.input_name.setText(name)
            self.input_calories.setText(str(cal))
            self.input_protein.setText(str(prot))
            self.input_fat.setText(str(fat))
            self.input_carbs.setText(str(carb))

    def save(self):
        name = self.input_name.text().strip()
        try:
            cal = float(self.input_calories.text())
            prot = float(self.input_protein.text())
            fat = float(self.input_fat.text())
            carb = float(self.input_carbs.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")
            return

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым.")
            return

        if self.db.update_product(self.product_id, name, cal, prot, fat, carb):
            self.accept()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.current_profile_id = None
        self.editing_product_id = None

        self.ui = MainWindowUI()
        self.setCentralWidget(self.ui)

        self.setup_profiles()
        self.load_products()
        self.setup_signals()
        self.update_daily_table()
        

        # Адаптивное растяжение столбцов таблицы дневного приёма
        self.ui.table_daily.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.table_daily.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def setup_profiles(self):
        self.reload_profiles()
        self.ui.profile_selector.currentIndexChanged.connect(self.on_profile_change)
        self.ui.btn_add_profile.clicked.connect(self.add_new_profile_inline)

    def reload_profiles(self):
        self.ui.profile_selector.blockSignals(True)
        self.ui.profile_selector.clear()
        profiles = self.db.get_profiles()
        for pid, name in profiles:
            self.ui.profile_selector.addItem(name, pid)
        if profiles:
            self.current_profile_id = profiles[0][0]
            self.ui.profile_selector.setCurrentIndex(0)
            self.update_daily_table()
        self.ui.profile_selector.blockSignals(False)

    def on_profile_change(self, index):
        profile_id = self.ui.profile_selector.itemData(index)
        if profile_id:
            self.current_profile_id = profile_id
            self.update_daily_table()

    def add_new_profile_inline(self):
        name, ok = QInputDialog.getText(self, "Новый профиль", "Введите имя профиля:")
        if ok and name.strip():
            if self.db.add_profile(name.strip()):
                self.reload_profiles()
                index = self.ui.profile_selector.findText(name.strip())
                if index != -1:
                    self.ui.profile_selector.setCurrentIndex(index)
            else:
                QMessageBox.warning(self, "Ошибка", "Профиль с таким именем уже существует.")

    def setup_signals(self):
        self.ui.btn_add_product.clicked.connect(self.add_product)
        self.ui.btn_add_entry.clicked.connect(self.add_entry)
        self.ui.date_edit.dateChanged.connect(self.update_daily_table)
        self.ui.list_products.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_products.customContextMenuRequested.connect(self.product_context_menu)
        self.ui.table_daily.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table_daily.customContextMenuRequested.connect(self.entry_context_menu)

    def load_products(self):
        self.ui.list_products.clear()
        self.ui.combo_products.clear()
        self.products = self.db.get_products()
        for product_id, name in self.products:
            item = QListWidgetItem(name)
            font = item.font()
            font.setPointSize(12)  # увеличиваем шрифт названия продукта
            item.setFont(font)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
            item.setData(Qt.ItemDataRole.UserRole, product_id)
            self.ui.list_products.addItem(item)
            self.ui.combo_products.addItem(name, product_id)

    def add_product(self):
        name = self.ui.input_name.text()
        try:
            calories = float(self.ui.input_calories.text())
            protein = float(self.ui.input_protein.text())
            fat = float(self.ui.input_fat.text())
            carbs = float(self.ui.input_carbs.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные значения.")
            return

        if self.db.add_product(name, calories, protein, fat, carbs):
            self.load_products()
        else:
            QMessageBox.warning(self, "Ошибка", "Продукт с таким именем уже существует.")
            
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название продукта не может быть пустым.")
        return
    

    def add_entry(self):
        product_id = self.ui.combo_products.currentData()
        date = self.ui.date_edit.date().toString("yyyy-MM-dd")
        try:
            quantity = float(self.ui.input_quantity.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите количество в граммах.")
            return

        self.db.add_daily_entry(date, product_id, quantity, self.current_profile_id)
        self.update_daily_table()

    def update_daily_table(self):
        self.ui.table_daily.setRowCount(0)
        date = self.ui.date_edit.date().toString("yyyy-MM-dd")
        entries = self.db.get_daily_entries_with_id(date, self.current_profile_id)
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for row_idx, entry in enumerate(entries):
            entry_id, name, quantity, cal, prot, fat, carb = entry
            self.ui.table_daily.insertRow(row_idx)
            self.ui.table_daily.setItem(row_idx, 0, QTableWidgetItem(name))
            self.ui.table_daily.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))

            kcal = cal * quantity / 100
            p = prot * quantity / 100
            f = fat * quantity / 100
            c = carb * quantity / 100

            self.ui.table_daily.setItem(row_idx, 2, QTableWidgetItem(f"{kcal:.1f}"))
            self.ui.table_daily.setItem(row_idx, 3, QTableWidgetItem(f"{p:.1f}"))
            self.ui.table_daily.setItem(row_idx, 4, QTableWidgetItem(f"{f:.1f}"))
            self.ui.table_daily.setItem(row_idx, 5, QTableWidgetItem(f"{c:.1f}"))

            total_calories += kcal
            total_protein += p
            total_fat += f
            total_carbs += c

        self.ui.label_summary.setText(
            f"Итого: калории: {total_calories:.1f}, белки: {total_protein:.1f}, жиры: {total_fat:.1f}, углеводы: {total_carbs:.1f}"
        )

    def product_context_menu(self, pos):
        item = self.ui.list_products.itemAt(pos)
        if not item:
            return

        product_id = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu()
        delete_action = menu.addAction("Удалить продукт")
        edit_action = menu.addAction("Редактировать продукт")
        action = menu.exec(self.ui.list_products.mapToGlobal(pos))

        if action == delete_action:
            self.db.delete_product(product_id)
            self.load_products()
            self.update_daily_table()
        elif action == edit_action:
            self.edit_product(product_id)

    def entry_context_menu(self, pos):
        row = self.ui.table_daily.rowAt(pos.y())
        if row == -1:
            return

        entry_id = self.db.get_daily_entries_with_id(
            self.ui.date_edit.date().toString("yyyy-MM-dd"), self.current_profile_id
        )[row][0]

        menu = QMenu()
        delete_action = menu.addAction("Удалить запись")
        action = menu.exec(self.ui.table_daily.mapToGlobal(pos))

        if action == delete_action:
            self.db.delete_daily_entry(entry_id)
            self.update_daily_table()

    def edit_product(self, product_id):
        dialog = ProductEditDialog(self.db, product_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()
            self.update_daily_table()

        
        self.editing_product_id = product_id

    def edit_entry(self, entry_id):
        entry = self.db.get_daily_entry(entry_id)
        if not entry:
            return
        _, date, product_id, quantity, profile_id = entry
        self.ui.input_quantity.setText(str(quantity))
        self.ui.combo_products.setCurrentIndex(
            self.ui.combo_products.findData(product_id)
        )
        self.db.delete_daily_entry(entry_id)
        self.update_daily_table()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

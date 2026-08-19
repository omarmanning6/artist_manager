import sqlite3
import sys
from pathlib import Path

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "artist_manager.db"


class ExpenseRepository:
    """Read and write expense records in SQLite."""

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = str(db_path)
        self.create_expenses_table()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_expenses_table(self):
        """Create the table the first time the application is run."""
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_date TEXT NOT NULL,
                    vendor_item TEXT NOT NULL,
                    cost REAL NOT NULL CHECK (cost >= 0),
                    tax_category TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_expense(self, transaction_date, vendor_item, cost, tax_category):
        """Insert one expense and return its generated ID."""
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO expenses (
                    transaction_date,
                    vendor_item,
                    cost,
                    tax_category
                )
                VALUES (?, ?, ?, ?)
                """,
                (transaction_date, vendor_item, cost, tax_category),
            )
            return cursor.lastrowid

    def get_expenses(self):
        """Return all expenses, newest first."""
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT
                    expense_id,
                    transaction_date,
                    vendor_item,
                    cost,
                    tax_category
                FROM expenses
                ORDER BY transaction_date DESC, expense_id DESC
                """
            ).fetchall()


class AddExpenseDialog(QDialog):
    """Dialog used to validate and collect a new expense."""

    CATEGORIES = ("Materials", "Rent", "Marketing", "Fees", "Other")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Expense")
        self.setModal(True)
        self.setMinimumWidth(380)

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("MM/dd/yyyy")

        self.vendor_input = QLineEdit()
        self.vendor_input.setPlaceholderText("Example: Blick Art Materials")

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setRange(0.01, 999_999_999.99)
        self.cost_input.setDecimals(2)
        self.cost_input.setPrefix("$")

        self.category_input = QComboBox()
        self.category_input.addItems(self.CATEGORIES)

        form_layout = QFormLayout()
        form_layout.addRow("Transaction date:", self.date_input)
        form_layout.addRow("Vendor / item:", self.vendor_input)
        form_layout.addRow("Cost:", self.cost_input)
        form_layout.addRow("Tax category:", self.category_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)

    def validate_and_accept(self):
        if not self.vendor_input.text().strip():
            QMessageBox.warning(
                self,
                "Missing Information",
                "Enter a vendor or item name.",
            )
            self.vendor_input.setFocus()
            return

        if self.cost_input.value() <= 0:
            QMessageBox.warning(
                self,
                "Invalid Cost",
                "The expense cost must be greater than $0.00.",
            )
            self.cost_input.setFocus()
            return

        self.accept()

    def expense_data(self):
        """Return validated values in the format expected by SQLite."""
        return {
            "transaction_date": self.date_input.date().toString("yyyy-MM-dd"),
            "vendor_item": self.vendor_input.text().strip(),
            "cost": round(self.cost_input.value(), 2),
            "tax_category": self.category_input.currentText(),
        }


class SummaryCard(QFrame):
    """Reusable card for displaying one dashboard statistic."""

    def __init__(self, title, value="$0.00"):
        super().__init__()

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

        self.setObjectName("summaryCard")

    def set_value(self, value):
        """Update the value displayed on the card."""
        self.value_label.setText(str(value))


class ExpensesPage(QWidget):
    expense_added = pyqtSignal(int)

    def __init__(self, db_path=DEFAULT_DB_PATH):
        super().__init__()

        self.expense_repository = ExpenseRepository(db_path)

        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.apply_styles()
        self.refresh_expenses_table()

    def create_widgets(self):
        """Create the dashboard controls and display widgets."""
        self.title_label = QLabel("Financial Tracker")
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(
            "Running revenue, expenses, and tax-ready totals"
        )
        self.subtitle_label.setObjectName("pageSubtitle")

        self.add_expense_button = QPushButton("+ Add Expense")

        # These cards will be connected to calculated database totals next.
        self.revenue_card = SummaryCard("Gross Revenue")
        self.expenses_card = SummaryCard("Expenses")
        self.net_profit_card = SummaryCard("Net Profit")

        # These temporary images will be replaced with live charts later.
        self.expenses_chart = QLabel("Expenses by Category")
        self.expenses_chart.setObjectName("sectionTitle")
        self.expenses_chart_image = QLabel()
        self.expenses_chart_image.setPixmap(
            QPixmap("images/expensesChartTemp.png")
        )

        self.expenses_sliders = QLabel("Monthly Cash Flow")
        self.expenses_sliders.setObjectName("sectionTitle")
        self.expenses_sliders_image = QLabel()
        self.expenses_sliders_image.setPixmap(
            QPixmap("images/expensesSliderTemp.png")
        )

        self.expenses_title = QLabel("Recent Expenses")
        self.expenses_title.setObjectName("sectionTitle")

        self.expenses_headers = [
            "Date",
            "Vendor/Item",
            "Cost",
            "Tax Category",
        ]
        self.expenses_table = QTableWidget(0, len(self.expenses_headers))
        self.expenses_table.setHorizontalHeaderLabels(self.expenses_headers)
        self.expenses_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.expenses_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

    def create_layout(self):
        """Place the widgets on the page."""
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout = QHBoxLayout()
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.add_expense_button)

        cards_layout = QGridLayout()
        cards_layout.addWidget(self.revenue_card, 0, 0)
        cards_layout.addWidget(self.expenses_card, 0, 1)
        cards_layout.addWidget(self.net_profit_card, 0, 2)

        charts_layout = QGridLayout()
        charts_layout.addWidget(self.expenses_chart, 0, 0)
        charts_layout.addWidget(self.expenses_sliders, 0, 1)
        
        charts_layout.addWidget(self.expenses_sliders_image, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(cards_layout)
        main_layout.addLayout(charts_layout)
        main_layout.addWidget(self.expenses_title)
        main_layout.addWidget(self.expenses_table)

    def connect_signals(self):
        """Connect button actions to page methods."""
        self.add_expense_button.clicked.connect(self.open_add_expense_dialog)

    def open_add_expense_dialog(self):
        """Open the form, save valid data, and update the table."""
        dialog = AddExpenseDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        expense = dialog.expense_data()

        try:
            expense_id = self.expense_repository.add_expense(**expense)
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"The expense could not be saved.\n\n{error}",
            )
            return

        self.refresh_expenses_table()
        self.expense_added.emit(expense_id)

    def refresh_expenses_table(self):
        """Reload the table from SQLite so previously saved rows appear."""
        try:
            expenses = self.expense_repository.get_expenses()
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Expenses could not be loaded.\n\n{error}",
            )
            return

        self.expenses_table.setRowCount(len(expenses))

        for row_index, expense in enumerate(expenses):
            date_item = QTableWidgetItem(expense["transaction_date"])
            vendor_item = QTableWidgetItem(expense["vendor_item"])
            cost_item = QTableWidgetItem(f'${expense["cost"]:,.2f}')
            category_item = QTableWidgetItem(expense["tax_category"])

            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            cost_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.expenses_table.setItem(row_index, 0, date_item)
            self.expenses_table.setItem(row_index, 1, vendor_item)
            self.expenses_table.setItem(row_index, 2, cost_item)
            self.expenses_table.setItem(row_index, 3, category_item)

    def showEvent(self, event):
        """Refresh whenever the user navigates back to this page."""
        super().showEvent(event)
        self.refresh_expenses_table()

    def apply_styles(self):
        """Apply styles that belong to the dashboard widgets."""
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f5f5f5;
                color: #222222;
                font-size: 14px;
            }

            #pageTitle {
                font-size: 28px;
                font-weight: bold;
            }

            #pageSubtitle {
                color: #666666;
            }

            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
            }

            #summaryCard {
                background-color: white;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 15px;
            }

            #cardTitle {
                color: #666666;
                font-size: 13px;
            }

            #cardValue {
                font-size: 25px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #3f6654;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 18px;
            }

            QPushButton:hover {
                background-color: #315143;
            }

            QLineEdit, QDateEdit, QDoubleSpinBox, QComboBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpensesPage()
    window.resize(1100, 750)
    window.show()
    sys.exit(app.exec())
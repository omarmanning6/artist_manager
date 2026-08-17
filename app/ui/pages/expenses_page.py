import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QHeaderView,
)


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
    add_expense_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.apply_styles()

    def create_widgets(self):
        """Create the dashboard controls and display widgets."""

        self.title_label = QLabel("Financial Tracker")
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(
            "Running revenue, expenses, and tax-ready totals"
        )
        self.subtitle_label.setObjectName("pageSubtitle")

        self.add_expense_button = QPushButton("+ Add Expense")

        # Will need to change to match actual values
        self.revenue_card = SummaryCard("Gross Revenue","$216,357.23",)
        self.expenses_card = SummaryCard("Expenses","$122,716.87",)
        self.net_profit_card = SummaryCard("Net Profit","$93,640.36",)

        #Will need to go back in and edit the expense by category and
        #monthly cash flow diagrams
        self.expenses_chart = QLabel("Expenses by Category")
        self.expenses_chart.setObjectName("sectionTitle")
        self.expenses_chart_image = QLabel()
        pixmap = QPixmap("images/expensesChartTemp.png")
        self.expenses_chart_image.setPixmap(pixmap)

        self.expenses_sliders_image = QLabel()
        pixmap2 = QPixmap("images/expensesSliderTemp.png")
        self.expenses_sliders_image.setPixmap(pixmap2)
        

        
        self.expenses_sliders = QLabel("Monthly Cash Flow")
        self.expenses_sliders.setObjectName("sectionTitle")

        self.expenses_title = QLabel("Recent Expenses")
        self.expenses_title.setObjectName("sectionTitle")
        self.expenses_headers = [
            "Date",
            "Vendor/Item",
            "Cost",
            "Tax Category"
        ]
        self.expenses_table = QTableWidget(0,len(self.expenses_headers))
        self.expenses_table.setHorizontalHeaderLabels(self.expenses_headers)
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)





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

        expenses_layout = QGridLayout()
        expenses_layout.addWidget(self.expenses_chart,0,0)
        expenses_layout.addWidget(self.expenses_sliders,0,1)
        expenses_layout.addWidget(self.expenses_chart_image,1,0)
        expenses_layout.addWidget(self.expenses_sliders_image,1,1)



        main_layout = QVBoxLayout(self)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(cards_layout)
        
        main_layout.addWidget(self.expenses_title)
        main_layout.addLayout(expenses_layout)
        main_layout.addStretch()

        main_layout.addWidget(self.expenses_title)
        main_layout.addWidget(self.expenses_table)

    def connect_signals(self):
        """Connect button actions to page signals."""

        self.add_expense_button.clicked.connect(
            self.add_expense_requested.emit
        )

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
            """
        )


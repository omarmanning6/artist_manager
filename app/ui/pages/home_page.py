"""Dashboard page for the Artist Manager application."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SummaryCard(QFrame):
    """Reusable card for displaying one dashboard statistic."""

    def __init__(self, title: str, value: str = "0"):
        super().__init__()

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

        self.setObjectName("summaryCard")

    def set_value(self, value):
        self.value_label.setText(str(value))


class HomePage(QWidget):
    """Main dashboard displayed when the application opens."""

    add_artwork_requested = pyqtSignal()
    record_sale_requested = pyqtSignal()
    add_expense_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.apply_styles()

    def create_widgets(self):
        """Create dashboard controls and display widgets."""

        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(
            "Welcome back. Here is an overview of your art business."
        )
        self.subtitle_label.setObjectName("pageSubtitle")

        self.total_artworks_card = SummaryCard("Total Artworks")
        self.available_artworks_card = SummaryCard("Available Artworks")
        self.total_sales_card = SummaryCard("Total Sales", "$0.00")
        self.net_profit_card = SummaryCard("Net Profit", "$0.00")

        self.add_artwork_button = QPushButton("+ Add Artwork")
        self.record_sale_button = QPushButton("+ Record Sale")
        self.add_expense_button = QPushButton("+ Add Expense")

        self.activity_title = QLabel("Artwork")
        self.activity_title.setObjectName("sectionTitle")

        self.artwork_headers = [
            "Title",
            "Medium",
            "Creation Year",
            "Retail Price",
            "Inventory Number",
            "Status",
            "Image Path",
        ]

        self.activity_table = QTableWidget(0, len(self.artwork_headers))
        self.activity_table.setHorizontalHeaderLabels(self.artwork_headers)
        self.activity_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.activity_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.verticalHeader().setVisible(False)

        self.exhibition_title = QLabel("Upcoming Exhibitions")
        self.exhibition_title.setObjectName("sectionTitle")

        self.exhibition_message = QLabel("No upcoming exhibition deadlines.")

    def create_layout(self):
        """Arrange dashboard widgets on the page."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(self.total_artworks_card, 0, 0)
        cards_layout.addWidget(self.available_artworks_card, 0, 1)
        cards_layout.addWidget(self.total_sales_card, 0, 2)
        cards_layout.addWidget(self.net_profit_card, 0, 3)

        main_layout.addLayout(cards_layout)

        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.add_artwork_button)
        actions_layout.addWidget(self.record_sale_button)
        actions_layout.addWidget(self.add_expense_button)
        actions_layout.addStretch()

        main_layout.addLayout(actions_layout)

        main_layout.addWidget(self.activity_title)
        main_layout.addWidget(self.activity_table)

        main_layout.addWidget(self.exhibition_title)
        main_layout.addWidget(self.exhibition_message)

    def connect_signals(self):
        """Forward quick-action button clicks to the main window."""

        self.add_artwork_button.clicked.connect(
            lambda: self.add_artwork_requested.emit()
        )
        self.record_sale_button.clicked.connect(
            lambda: self.record_sale_requested.emit()
        )
        self.add_expense_button.clicked.connect(
            lambda: self.add_expense_requested.emit()
        )

    def update_summary(
        self,
        total_artworks,
        available_artworks,
        total_sales,
        net_profit,
    ):
        """Update the dashboard cards with database values."""

        self.total_artworks_card.set_value(total_artworks)
        self.available_artworks_card.set_value(available_artworks)
        self.total_sales_card.set_value(f"${total_sales:,.2f}")
        self.net_profit_card.set_value(f"${net_profit:,.2f}")

    def add_activity(
        self,
        title,
        medium="",
        creation_year="",
        retail_price="",
        inventory_number="",
        status="",
        image_path="",
    ):
        """Add one artwork record to the dashboard table."""

        row = self.activity_table.rowCount()
        self.activity_table.insertRow(row)

        values = (
            title,
            medium,
            creation_year,
            retail_price,
            inventory_number,
            status,
            image_path,
        )

        for column, value in enumerate(values):
            self.activity_table.setItem(
                row,
                column,
                QTableWidgetItem(str(value)),
            )

    def refresh(self):
        """Refresh dashboard information from the data layer."""

        # Temporary values until the SQLite repository is connected.
        self.update_summary(
            total_artworks=12,
            available_artworks=8,
            total_sales=4250.00,
            net_profit=2875.50,
        )

    def apply_styles(self):
        """Apply styles that belong to dashboard widgets."""

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

            QTableWidget {
                background-color: white;
                alternate-background-color: #f0f3f1;
                border: 1px solid #dddddd;
            }
            """
        )
import sys
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QGridLayout,
)


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "artist_manager.db"


class SummaryCard(QFrame):
    """Reusable card for displaying one dashboard statistic."""

    def __init__(self, title, value="$0.00", subfield=""):
        super().__init__()

        self.setObjectName("summaryCard")
        self.setMinimumHeight(115)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        self.subfield_label = QLabel(subfield)
        self.subfield_label.setObjectName("cardField")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(5)

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subfield_label)

    def set_value(self, value, subfield=None):
        """Update the values displayed on the card."""
        self.value_label.setText(str(value))

        if subfield is not None:
            self.subfield_label.setText(str(subfield))


class SalesPage(QWidget):
    sales_added = pyqtSignal(int)

    def __init__(self, db_path=DEFAULT_DB_PATH):
        super().__init__()

        self.db_path = db_path
        self.setObjectName("salesPage")

        self.create_widgets()
        self.create_layout()
        self.apply_styles()

    def create_widgets(self):
        """Create the sales page controls and display widgets."""
        self.title_label = QLabel("Sales & Customers")
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(
            "Transactions, buyers, and artwork sales history"
        )
        self.subtitle_label.setObjectName("pageSubtitle")

        self.add_log_button = QPushButton("+ Log Sale")

        # Three cards matching your example
        self.revenue_card = SummaryCard(
            "Lifetime revenue", "$31,870", "19 artworks sold",
        )
        self.average_sale_card = SummaryCard(
            "Average sale",    "$1,677",  "Before tax",
        )
        self.customers_card = SummaryCard(
            "Customers",  "16",  "3 repeat buyers",
        )

        self.sales_chart = QLabel("Monthly sales")
        self.sales_chart.setObjectName("sectionTitle")


        self.payment_slider = QLabel("Payment method")
        self.payment_slider.setObjectName("sectionTitle")
    def create_layout(self):
        """Place the widgets on the page."""
        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout = QHBoxLayout()
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.add_log_button)

        cards_layout = QGridLayout()
        cards_layout.setHorizontalSpacing(12)
        cards_layout.setVerticalSpacing(12)

        cards_layout.addWidget(self.revenue_card, 0, 0)
        cards_layout.addWidget(self.average_sale_card, 0, 1)
        cards_layout.addWidget(self.customers_card, 0, 2)

        # Give every card equal width
        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)
        cards_layout.setColumnStretch(2, 1)

        charts_layout = QGridLayout()
        charts_layout.addWidget(self.sales_chart,0,0)
        charts_layout.addWidget(self.payment_slider,0,1)
        

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(18)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(cards_layout)
        main_layout.addLayout(charts_layout)


        main_layout.addStretch()

    def apply_styles(self):
        """Apply styles to the sales page."""
        self.setStyleSheet(
            """
            QWidget#salesPage {
                background-color: #111111;
                color: #F5F5F5;
                font-size: 14px;
            }

            QLabel {
                background-color: transparent;
            }

            #pageTitle {
                color: #FFFFFF;
                font-size: 28px;
                font-weight: bold;
            }

            #pageSubtitle {
                color: #A0A0A0;
            }
            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
            }

            QPushButton {
                background-color: #ECECEC;
                color: #111111;
                border: none;
                border-radius: 5px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #BDBDBD;
            }

            QFrame#summaryCard {
                background-color: #1F1F1F;
                border: 1px solid #353535;
                border-radius: 20px;
            }

            QFrame#summaryCard QLabel {
                background-color: transparent;
                border: none;
            }

            #cardTitle {
                color: #B3B3B3;
                font-size: 15px;
            }

            #cardValue {
                color: #FFFFFF;
                font-size: 25px;
                font-weight: bold;
            }

            #cardField {
                color: #A0A0A0;
                font-size: 13px;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SalesPage()
    window.resize(1100, 750)
    window.show()

    sys.exit(app.exec())
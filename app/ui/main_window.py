"""Main application window and sidebar navigation."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.pages.home_page import HomePage
from app.ui.pages.expenses_page import ExpensesPage

class PlaceholderPage(QWidget):
    """Temporary page used until a feature page is implemented."""

    def __init__(self, page_name: str):
        super().__init__()

        title = QLabel(page_name)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            color: #222222;
            """
        )

        layout = QVBoxLayout(self)
        layout.addWidget(title)


class MainWindow(QMainWindow):
    """Top-level window that owns the sidebar and application pages."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Artist Manager")
        self.resize(1200, 750)

        self.create_pages()
        self.create_sidebar()
        self.create_main_layout()
        self.connect_navigation()
        self.apply_styles()

        self.navigation_list.setCurrentRow(0)
        self.home_page.refresh()

    def create_pages(self):
        """Create every page displayed in the application."""

        self.page_stack = QStackedWidget()

        self.home_page = HomePage()

        # Temporary pages; replace these as each feature is implemented.
        self.artwork_page = PlaceholderPage("Artwork Inventory")
        self.supplies_page = PlaceholderPage("Supply Inventory")
        self.customer_page = PlaceholderPage("Customers")
        self.sales_page = PlaceholderPage("Sales")
        self.expenses_page = ExpensesPage()
        self.exhibitions_page = PlaceholderPage("Exhibitions")
        self.reports_page = PlaceholderPage("Reports")

        # This order must match the sidebar item order.
        self.pages = [
            self.home_page,
            self.artwork_page,
            self.supplies_page,
            self.customer_page,
            self.sales_page,
            self.expenses_page,
            self.exhibitions_page,
            self.reports_page,
        ]

        for page in self.pages:
            self.page_stack.addWidget(page)

    def create_sidebar(self):
        """Create the navigation menu displayed on the left."""

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(20)

        app_title = QLabel("Artist Manager")
        app_title.setObjectName("appTitle")

        self.navigation_list = QListWidget()
        self.navigation_list.setObjectName("navigationList")
        self.navigation_list.addItems(
            [
                "Home",
                "Artwork Inventory",
                "Supply Inventory",
                "Customers",
                "Sales",
                "Expenses",
                "Exhibitions",
                "Reports",
            ]
        )

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(self.navigation_list)

    def create_main_layout(self):
        """Place the sidebar and page stack in the central widget."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.page_stack, 1)

    def connect_navigation(self):
        """Connect sidebar selections and dashboard shortcuts to pages."""

        self.navigation_list.currentRowChanged.connect(self.switch_page)

        self.home_page.add_artwork_requested.connect(
            lambda: self.navigation_list.setCurrentRow(1)
        )
        self.home_page.record_sale_requested.connect(
            lambda: self.navigation_list.setCurrentRow(4)
        )
        self.home_page.add_expense_requested.connect(
            lambda: self.navigation_list.setCurrentRow(5)
        )

    def switch_page(self, page_index: int):
        """Display the page that matches the selected sidebar row."""

        if 0 <= page_index < self.page_stack.count():
            self.page_stack.setCurrentIndex(page_index)

            if page_index == 0:
                self.home_page.refresh()

    def apply_styles(self):
        """Apply styling that belongs to the application shell."""

        self.setStyleSheet(
            """
            #sidebar {
                background-color: #263f35;
            }

            #appTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            #navigationList {
                color: white;
                background-color: transparent;
                border: none;
                outline: none;
                font-size: 14px;
            }

            #navigationList::item {
                border-radius: 5px;
                padding: 11px 8px;
            }

            #navigationList::item:hover {
                background-color: #315143;
            }

            #navigationList::item:selected {
                background-color: #3f6654;
            }
            """
        )
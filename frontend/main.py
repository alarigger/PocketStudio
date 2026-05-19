import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QLabel
)

from PyQt5.QtCore import QTimer


class AssetWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.job_id = None

        self.setWindowTitle("Asset Manager")

        self.layout = QVBoxLayout()

        self.label = QLabel("Ready")

        self.scan_button = QPushButton("Scan Assets")
        self.scan_button.clicked.connect(self.start_scan)

        self.asset_list = QListWidget()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.asset_list)

        self.setLayout(self.layout)

        # timer for polling backend
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_job_status)

    # -----------------------------------
    # BUTTON CLICK
    # -----------------------------------

    def start_scan(self):

        self.label.setText("Starting scan...")

        response = requests.post(
            "http://127.0.0.1:8000/scan"
        )

        data = response.json()

        self.job_id = data["job_id"]

        self.label.setText(f"Job: {self.job_id}")

        # start polling every second
        self.timer.start(1000)

    # -----------------------------------
    # CHECK JOB STATUS
    # -----------------------------------

    def check_job_status(self):

        if not self.job_id:
            return

        response = requests.get(
            f"http://127.0.0.1:8000/job/{self.job_id}"
        )

        data = response.json()

        status = data["status"]

        self.label.setText(f"Status: {status}")

        if status == "finished":

            self.timer.stop()

            self.asset_list.clear()

            for asset in data["result"]:
                self.asset_list.addItem(asset)

            self.label.setText("Scan complete")


app = QApplication(sys.argv)

window = AssetWindow()
window.resize(400, 300)
window.show()

sys.exit(app.exec_())
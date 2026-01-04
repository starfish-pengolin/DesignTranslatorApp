from PyQt6 import QtWidgets, QtCore
import os

from core.blender_export import export_highpoly
from core.blender_script_export import generate_blender_script
from core.blender_to_freecad import import_blender_script

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design Translator")
        self.setGeometry(100, 100, 500, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # --- Input CAD file ---
        self.from_label = QtWidgets.QLabel("1️⃣ Select CAD File (.fcstd):")
        self.from_input = QtWidgets.QLineEdit()
        self.from_btn = QtWidgets.QPushButton("Browse CAD File")
        self.from_btn.clicked.connect(self.select_file)
        layout.addWidget(self.from_label)
        layout.addWidget(self.from_input)
        layout.addWidget(self.from_btn)

        # --- Output folder ---
        self.to_label = QtWidgets.QLabel("2️⃣ Select Output Folder:")
        self.to_input = QtWidgets.QLineEdit()
        self.to_btn = QtWidgets.QPushButton("Browse Output Folder")
        self.to_btn.clicked.connect(self.select_output)
        layout.addWidget(self.to_label)
        layout.addWidget(self.to_input)
        layout.addWidget(self.to_btn)

        # --- Buttons ---
        self.export_stl_btn = QtWidgets.QPushButton("Export FreeCAD → High-Poly STL")
        self.export_stl_btn.clicked.connect(self.export_stl)
        layout.addWidget(self.export_stl_btn)

        self.export_blender_btn = QtWidgets.QPushButton("Export FreeCAD → Blender Script")
        self.export_blender_btn.clicked.connect(self.export_blender_script)
        layout.addWidget(self.export_blender_btn)

        self.import_blender_btn = QtWidgets.QPushButton("Import Blender Script → FreeCAD")
        self.import_blender_btn.clicked.connect(self.import_blender)
        layout.addWidget(self.import_blender_btn)

        self.setLayout(layout)

    # --- Select CAD file ---
    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select CAD File", filter="FreeCAD Files (*.fcstd)")
        if file_path:
            self.from_input.setText(file_path)

    # --- Select output folder ---
    def select_output(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.to_input.setText(folder_path)

    # --- Export STL ---
    def export_stl(self):
        fcstd = self.from_input.text()
        out_dir = self.to_input.text()
        if fcstd and out_dir:
            try:
                export_highpoly(fcstd, out_dir)
                QtWidgets.QMessageBox.information(self, "Done", "High-poly STL exported successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    # --- Export Blender Script ---
    def export_blender_script(self):
        fcstd = self.from_input.text()
        out_dir = self.to_input.text()
        if fcstd and out_dir:
            try:
                generate_blender_script(fcstd, out_dir)
                QtWidgets.QMessageBox.information(self, "Done", "Blender Python script generated successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    # --- Import Blender Script ---
    def import_blender(self):
        blender_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Blender Python Script", filter="Python Files (*.py)")
        output_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder for FreeCAD")
        if ble


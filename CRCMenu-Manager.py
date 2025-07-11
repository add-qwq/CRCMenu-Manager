import sys
import json
import os
import hashlib
import re
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QFileDialog, QListWidget, QWidget, 
                             QLabel, QMessageBox, QProgressBar, QStatusBar, QTextEdit,
                             QComboBox)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPalette

class ProcessThread(QThread):
    progress_updated = Signal(int)
    file_processed = Signal(str, bool)
    operation_completed = Signal(bool)
    
    def __init__(self, file_list, font_awesome_code, css_code, js_code, html_code, mode):
        super().__init__()
        self.file_list = file_list
        self.font_awesome_code = font_awesome_code
        self.css_code = css_code
        self.js_code = js_code
        self.html_code = html_code
        self.mode = mode
        
        self.common_timestamp = time.time()
        
    def run(self):
        success_count = 0
        total_files = len(self.file_list)
        
        for i, file_path in enumerate(self.file_list):
            result = self._process_file(file_path)
            self.file_processed.emit(file_path, result)
            if result:
                success_count += 1
            self.progress_updated.emit(int((i + 1) / total_files * 100))
        
        self.operation_completed.emit(success_count == total_files)
    
    def _process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            backup_path = file_path + '.bak'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.mode == "update":
                return self._update_version(content, file_path)
            elif self.mode == "inject":
                return self._inject_content(content, file_path)
            elif self.mode == "delete":
                return self._delete_content(content, file_path)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def _update_version(self, content, file_path):
        try:
            hash_value = hashlib.md5(str(self.common_timestamp).encode()).hexdigest()[:8]
            
            css_pattern = r'(<link[^>]*href=["\'][^"\']*CRCMenu\.css)(?:\?v=[^"\']*)?(["\'][^>]*)>'
            new_css = r'\1?v=' + hash_value + r'\2>'
            new_content = re.sub(css_pattern, new_css, content, flags=re.IGNORECASE)
            
            js_pattern = r'(<script[^>]*src=["\'][^"\']*CRCMenu\.js)(?:\?v=[^"\']*)?(["\'][^>]*)>'
            new_js = r'\1?v=' + hash_value + r'\2>'
            new_content = re.sub(js_pattern, new_js, new_content, flags=re.IGNORECASE)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error updating versions {file_path}: {e}")
            return False
    
    def _inject_content(self, content, file_path):
        try:
            head_index = content.lower().rfind('</head>')
            if head_index == -1:
                return False
                
            body_start = content.lower().find('<body')
            body_end = content.lower().rfind('</body>')
            if body_start == -1 or body_end == -1:
                return False
                
            body_tag_end = content.find('>', body_start)
            if body_tag_end == -1:
                return False

            font_awesome_pattern = r'<link[^>]*href=["\'][^"\']*font-awesome[^"\']*["\'][^>]*>'
            font_awesome_insert = self.font_awesome_code + '\n' if self.font_awesome_code and not re.search(font_awesome_pattern, content, re.IGNORECASE) else ''

            html_insert_pos = body_tag_end + 1
            js_insert_pos = body_end
            
            new_content = (content[:head_index] + font_awesome_insert + self.css_code + '\n' + 
                          content[head_index:html_insert_pos] + '\n' + self.html_code + '\n' + 
                          content[html_insert_pos:js_insert_pos] + '\n' + self.js_code + '\n' + 
                          content[js_insert_pos:])
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error injecting content {file_path}: {e}")
            return False

    def _delete_content(self, content, file_path):
        try:
            if self.font_awesome_code:
                content = content.replace(self.font_awesome_code, '')
            if self.css_code:
                content = content.replace(self.css_code, '')
            if self.js_code:
                content = content.replace(self.js_code, '')
            if self.html_code:
                content = content.replace(self.html_code, '')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error deleting content {file_path}: {e}")
            return False

class CRCMenuManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.file_list_path = "CRCMenu-Manager_file_list.json"
        self.language = "zh"
        self.font_awesome_code = ''
        self.css_code = ''
        self.js_code = ''
        self.html_code = ''
        self.last_json_mtime = 0
        
        self.is_saving = False
        self.is_loading = False
        self.pending_save = False
        
        self.save_timer = QTimer(self)
        self.save_timer.setInterval(500)
        self.save_timer.timeout.connect(self.perform_save)

        self.texts = {
            "zh": {
                "title": "CRCMenu 管理工具",
                "file_list_label": "已选择的文件：",
                "add_file_btn": "选择文件",
                "remove_file_btn": "移除选中文件",
                "clear_files_btn": "清空文件列表",
                "execute_btn": "执行操作",
                "no_files_msg": "请先选择要处理的文件",
                "confirm_update_msg": "确定要更新 {} 个文件的版本吗？\n操作前会自动创建备份文件。",
                "confirm_inject_msg": "确定要在 {} 个文件中引入右键菜单吗？\n操作前会自动创建备份文件。",
                "confirm_delete_msg": "确定要在 {} 个文件中删除指定内容吗？\n操作前会自动创建备份文件。",
                "success_msg": "所有文件处理成功！",
                "partial_fail_msg": "部分文件处理失败，请查看状态栏信息",
                "load_error_msg": "无法加载配置：{}",
                "processing_msg": "开始处理文件...",
                "file_processed_msg": "处理 {}：{}",
                "success_status": "成功",
                "fail_status": "失败",
                "toggle_lang_btn": "Switch to English",
                "confirm_title": "确认操作",
                "complete_title": "完成",
                "partial_fail_title": "部分失败",
                "load_error_title": "加载错误",
                "font_awesome_label": "Font Awesome 引入代码：",
                "css_code_label": "CSS 引入代码：",
                "js_code_label": "JS 引入代码：",
                "html_code_label": "右键菜单 HTML 代码：",
                "save_success_msg": "配置已保存",
                "invalid_config_msg": "配置文件格式不正确，已重置",
                "mode_labels": {
                    "update": "更新版本",
                    "inject": "引入项目",
                    "delete": "删除项目"
                }
            },
            "en": {
                "title": "CRCMenu Manager",
                "file_list_label": "Selected Files:",
                "add_file_btn": "Select Files",
                "remove_file_btn": "Remove Selected Files",
                "clear_files_btn": "Clear File List",
                "execute_btn": "Execute Operation",
                "no_files_msg": "Please select files to process first",
                "confirm_update_msg": "Are you sure you want to update versions for {} files?\nBackup files will be created automatically.",
                "confirm_inject_msg": "Are you sure you want to inject right-click menu into {} files?\nBackup files will be created automatically.",
                "confirm_delete_msg": "Are you sure you want to delete specified content from {} files?\nBackup files will be created automatically.",
                "success_msg": "All files processed successfully!",
                "partial_fail_msg": "Some files failed to process, please check the status bar for details",
                "load_error_msg": "Failed to load configuration: {}",
                "processing_msg": "Starting file processing...",
                "file_processed_msg": "Processing {}: {}",
                "success_status": "Success",
                "fail_status": "Failed",
                "toggle_lang_btn": "切换到中文",
                "confirm_title": "Confirm Operation",
                "complete_title": "Completed",
                "partial_fail_title": "Partial Failure",
                "load_error_title": "Load Error",
                "font_awesome_label": "Font Awesome Include Code:",
                "css_code_label": "CSS Include Code:",
                "js_code_label": "JS Include Code:",
                "html_code_label": "Right-Click Menu HTML Code:",
                "save_success_msg": "Configuration saved",
                "invalid_config_msg": "Invalid configuration format, resetting",
                "mode_labels": {
                    "update": "Update Version",
                    "inject": "Inject Project",
                    "delete": "Delete Project"
                }
            }
        }
        
        self.init_ui()
        self.load_json()
        self.load_file_list()
        self.start_json_watcher()
        
        QTimer.singleShot(0, self.showMaximized)
    
    def init_ui(self):
        self.setWindowTitle(self.texts[self.language]["title"])

        app = QApplication.instance()
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 245, 245))
        palette.setColor(QPalette.WindowText, QColor(33, 33, 33))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.Text, QColor(33, 33, 33))
        palette.setColor(QPalette.Button, QColor(220, 220, 220))
        palette.setColor(QPalette.ButtonText, QColor(33, 33, 33))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(0, 120, 215))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        app.setPalette(palette)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.title_label = QLabel(self.texts[self.language]["title"])
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #212121; margin-bottom: 10px;")
        main_layout.addWidget(self.title_label)

        self.mode_combobox = QComboBox()
        self.update_mode_combobox_items()
        self.mode_combobox.currentTextChanged.connect(self.update_input_labels)
        main_layout.addWidget(self.mode_combobox)

        self.font_awesome_label = QLabel(self.get_mode_specific_label("font_awesome"))
        self.font_awesome_label.setStyleSheet("color: #555555; margin-bottom: 5px;")
        main_layout.addWidget(self.font_awesome_label)
        
        self.font_awesome_edit = QTextEdit()
        self.font_awesome_edit.setPlaceholderText(self.texts[self.language]["font_awesome_label"].split("：")[1] if self.language == "zh" else self.texts[self.language]["font_awesome_label"].split(":")[1])
        self.font_awesome_edit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
                color: #212121;
            }
        """)
        self.font_awesome_edit.setText(self.font_awesome_code)
        self.font_awesome_edit.textChanged.connect(self.schedule_save)
        main_layout.addWidget(self.font_awesome_edit)

        self.css_code_label = QLabel(self.get_mode_specific_label("css"))
        self.css_code_label.setStyleSheet("color: #555555; margin-bottom: 5px;")
        main_layout.addWidget(self.css_code_label)
        
        self.css_code_edit = QTextEdit()
        self.css_code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
                color: #212121;
            }
        """)
        self.css_code_edit.setText(self.css_code)
        self.css_code_edit.textChanged.connect(self.schedule_save)
        main_layout.addWidget(self.css_code_edit)

        self.js_code_label = QLabel(self.get_mode_specific_label("js"))
        self.js_code_label.setStyleSheet("color: #555555; margin-bottom: 5px;")
        main_layout.addWidget(self.js_code_label)
        
        self.js_code_edit = QTextEdit()
        self.js_code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
                color: #212121;
            }
        """)
        self.js_code_edit.setText(self.js_code)
        self.js_code_edit.textChanged.connect(self.schedule_save)
        main_layout.addWidget(self.js_code_edit)

        self.html_code_label = QLabel(self.get_mode_specific_label("html"))
        self.html_code_label.setStyleSheet("color: #555555; margin-bottom: 5px;")
        main_layout.addWidget(self.html_code_label)
        
        self.html_code_edit = QTextEdit()
        self.html_code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
                color: #212121;
            }
        """)
        self.html_code_edit.setText(self.html_code)
        self.html_code_edit.textChanged.connect(self.schedule_save)
        main_layout.addWidget(self.html_code_edit)

        self.list_label = QLabel(self.texts[self.language]["file_list_label"])
        self.list_label.setStyleSheet("color: #555555; margin-bottom: 5px;")
        main_layout.addWidget(self.list_label)
        
        self.file_list_widget = QListWidget()
        self.file_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 10px;
                color: #212121;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 3px;
                margin: 2px 0;
                background-color: transparent;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
                border: none;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #f0f5ff;
            }
            QListWidget::item:selected:hover {
                background-color: #006ab3;
            }
        """)
        main_layout.addWidget(self.file_list_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_file_btn = QPushButton(self.texts[self.language]["add_file_btn"])
        self.add_file_btn.clicked.connect(self.select_files)
        self.style_button(self.add_file_btn)
        button_layout.addWidget(self.add_file_btn)
        
        self.remove_file_btn = QPushButton(self.texts[self.language]["remove_file_btn"])
        self.remove_file_btn.clicked.connect(self.remove_selected_files)
        self.style_button(self.remove_file_btn)
        button_layout.addWidget(self.remove_file_btn)
        
        self.clear_files_btn = QPushButton(self.texts[self.language]["clear_files_btn"])
        self.clear_files_btn.clicked.connect(self.clear_file_list)
        self.style_button(self.clear_files_btn)
        button_layout.addWidget(self.clear_files_btn)
        
        self.toggle_lang_btn = QPushButton(self.texts[self.language]["toggle_lang_btn"])
        self.toggle_lang_btn.clicked.connect(self.toggle_language)
        self.style_button(self.toggle_lang_btn)
        button_layout.addWidget(self.toggle_lang_btn)
        
        main_layout.addLayout(button_layout)

        self.execute_btn = QPushButton(self.texts[self.language]["execute_btn"])
        self.execute_btn.clicked.connect(self.process_files)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 14px;
                padding: 12px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #005ba1;
            }
            QPushButton:pressed {
                background-color: #003087;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        main_layout.addWidget(self.execute_btn)

        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                color: #555555;
            }
        """)
        self.setStatusBar(self.statusBar)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                background-color: #ffffff;
                text-align: center;
                color: #212121;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 3px;
            }
        """)
        self.statusBar.addPermanentWidget(self.progress_bar, 1)
        
        self.update_input_labels()

    def update_mode_combobox_items(self):
        current_mode = self.get_current_mode()
        self.mode_combobox.clear()
        mode_labels = self.texts[self.language]["mode_labels"]
        self.mode_combobox.addItems([
            mode_labels["update"],
            mode_labels["inject"],
            mode_labels["delete"]
        ])
        reverse_map = {v: k for k, v in mode_labels.items()}
        if current_mode in reverse_map.values():
            for i in range(3):
                if reverse_map.get(self.mode_combobox.itemText(i)) == current_mode:
                    self.mode_combobox.setCurrentIndex(i)
                    break

    def get_current_mode(self):
        if self.mode_combobox.count() == 0:
            return "update"
        current_text = self.mode_combobox.currentText()
        mode_labels = self.texts[self.language]["mode_labels"]
        reverse_map = {v: k for k, v in mode_labels.items()}
        return reverse_map.get(current_text, "update")

    def get_mode_specific_label(self, code_type):
        mode = self.get_current_mode()

        base_labels = {
            "font_awesome": {
                "update": "Font Awesome 引入代码：",
                "inject": "Font Awesome 引入代码：",
                "delete": "要删除的 Font Awesome 引入代码："
            },
            "css": {
                "update": "CSS 引入代码：",
                "inject": "CSS 引入代码：",
                "delete": "要删除的 CSS 引入代码："
            },
            "js": {
                "update": "JS 引入代码：",
                "inject": "JS 引入代码：",
                "delete": "要删除的 JS 引入代码："
            },
            "html": {
                "update": "右键菜单 HTML 代码：",
                "inject": "右键菜单 HTML 代码：",
                "delete": "要删除的右键菜单 HTML 代码："
            }
        }
        
        if self.language == "en":
            en_labels = {
                "font_awesome": {
                    "update": "Font Awesome Include Code:",
                    "inject": "Font Awesome Include Code:",
                    "delete": "Font Awesome Include Code to Delete:"
                },
                "css": {
                    "update": "CSS Include Code:",
                    "inject": "CSS Include Code:",
                    "delete": "CSS Include Code to Delete:"
                },
                "js": {
                    "update": "JS Include Code:",
                    "inject": "JS Include Code:",
                    "delete": "JS Include Code to Delete:"
                },
                "html": {
                    "update": "Right-Click Menu HTML Code:",
                    "inject": "Right-Click Menu HTML Code:",
                    "delete": "Right-Click Menu HTML Code to Delete:"
                }
            }
            return en_labels[code_type][mode]
        
        return base_labels[code_type][mode]
    
    def update_input_labels(self):
        self.font_awesome_label.setText(self.get_mode_specific_label("font_awesome"))
        self.css_code_label.setText(self.get_mode_specific_label("css"))
        self.js_code_label.setText(self.get_mode_specific_label("js"))
        self.html_code_label.setText(self.get_mode_specific_label("html"))
    
    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #212121;
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #b0b0b0;
            }
        """)
        button.clicked.connect(lambda: self.animate_button(button))
    
    def animate_button(self, button):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(100)
        original_geometry = button.geometry()
        anim.setStartValue(original_geometry)
        anim.setEndValue(original_geometry.adjusted(2, 2, -2, -2))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()

    def toggle_language(self):
        current_mode = self.get_current_mode()
        self.language = "en" if self.language == "zh" else "zh"
        self.update_ui_text()
        self.update_mode_combobox_items()
        self.set_mode_by_code(current_mode)
        self.update_input_labels()

    def set_mode_by_code(self, mode_code):
        mode_labels = self.texts[self.language]["mode_labels"]
        target_text = mode_labels.get(mode_code)
        if target_text:
            index = self.mode_combobox.findText(target_text)
            if index != -1:
                self.mode_combobox.setCurrentIndex(index)
    
    def update_ui_text(self):
        self.setWindowTitle(self.texts[self.language]["title"])
        self.title_label.setText(self.texts[self.language]["title"])
        self.list_label.setText(self.texts[self.language]["file_list_label"])
        self.add_file_btn.setText(self.texts[self.language]["add_file_btn"])
        self.remove_file_btn.setText(self.texts[self.language]["remove_file_btn"])
        self.clear_files_btn.setText(self.texts[self.language]["clear_files_btn"])
        self.execute_btn.setText(self.texts[self.language]["execute_btn"])
        self.toggle_lang_btn.setText(self.texts[self.language]["toggle_lang_btn"])
        self.font_awesome_edit.setPlaceholderText(self.texts[self.language]["font_awesome_label"].split("：")[1] if self.language == "zh" else self.texts[self.language]["font_awesome_label"].split(":")[1])
    
    def schedule_save(self):
        self.font_awesome_code = self.font_awesome_edit.toPlainText().strip()
        self.css_code = self.css_code_edit.toPlainText().strip()
        self.js_code = self.js_code_edit.toPlainText().strip()
        self.html_code = self.html_code_edit.toPlainText().strip()
        
        if self.is_saving:
            self.pending_save = True
        else:
            if not self.save_timer.isActive():
                self.save_timer.start()
    
    def perform_save(self):
        self.save_timer.stop()
        
        if self.is_loading:
            self.schedule_save()
            return
            
        self.is_saving = True
        
        try:
            data = {
                "files": [self.file_list_widget.item(i).text() for i in range(self.file_list_widget.count())],
                "font_awesome_code": self.font_awesome_code,
                "css_code": self.css_code,
                "js_code": self.js_code,
                "html_code": self.html_code
            }
            
            with open(self.file_list_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            self.last_json_mtime = os.path.getmtime(self.file_list_path)
            self.statusBar.showMessage(self.texts[self.language]["save_success_msg"], 2000)
            
        except Exception as e:
            print(f"保存配置文件出错: {e}")
        finally:
            self.is_saving = False
            if self.pending_save:
                self.pending_save = False
                self.perform_save()
    
    def load_json(self):
        self.is_loading = True
        
        try:
            if os.path.exists(self.file_list_path):
                with open(self.file_list_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.font_awesome_code = data.get("font_awesome_code", '')
                    self.css_code = data.get("css_code", '')
                    self.js_code = data.get("js_code", '')
                    self.html_code = data.get("html_code", '')
                    
                    self.font_awesome_edit.textChanged.disconnect()
                    self.css_code_edit.textChanged.disconnect()
                    self.js_code_edit.textChanged.disconnect()
                    self.html_code_edit.textChanged.disconnect()
                    
                    self.font_awesome_edit.setText(self.font_awesome_code)
                    self.css_code_edit.setText(self.css_code)
                    self.js_code_edit.setText(self.js_code)
                    self.html_code_edit.setText(self.html_code)
                    
                    self.font_awesome_edit.textChanged.connect(self.schedule_save)
                    self.css_code_edit.textChanged.connect(self.schedule_save)
                    self.js_code_edit.textChanged.connect(self.schedule_save)
                    self.html_code_edit.textChanged.connect(self.schedule_save)
        except Exception as e:
            print(f"加载配置文件出错: {e}")
            QMessageBox.warning(self, self.texts[self.language]["load_error_title"], 
                              self.texts[self.language]["load_error_msg"].format(str(e)))
        finally:
            self.is_loading = False
    
    def load_file_list(self):
        if os.path.exists(self.file_list_path):
            try:
                with open(self.file_list_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    file_list = data.get("files", [])
                    self.file_list_widget.clear()
                    for file_path in file_list:
                        self.file_list_widget.addItem(file_path)
            except Exception as e:
                QMessageBox.warning(self, self.texts[self.language]["load_error_title"], 
                                  self.texts[self.language]["load_error_msg"].format(str(e)))
    
    def select_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, self.texts[self.language]["add_file_btn"], "", "HTML/PHP Files (*.html *.htm *.php);;All Files (*)"
        )
        
        for file_path in file_paths:
            if file_path not in [self.file_list_widget.item(i).text() for i in range(self.file_list_widget.count())]:
                self.file_list_widget.addItem(file_path)
        
        self.schedule_save()
    
    def remove_selected_files(self):
        for item in self.file_list_widget.selectedItems():
            self.file_list_widget.takeItem(self.file_list_widget.row(item))
        
        self.schedule_save()
    
    def clear_file_list(self):
        self.file_list_widget.clear()
        self.schedule_save()
    
    def process_files(self):
        mode = self.get_current_mode()
        file_count = self.file_list_widget.count()
        
        if file_count == 0:
            QMessageBox.information(self, self.texts[self.language]["complete_title"], 
                                  self.texts[self.language]["no_files_msg"])
            return
        
        if mode == "inject" and (not self.css_code or not self.js_code or not self.html_code):
            QMessageBox.warning(self, self.texts[self.language]["partial_fail_title"], 
                              "请提供完整的CSS、JS和HTML代码" if self.language == "zh" else 
                              "Please provide complete CSS, JS, and HTML code")
            return
        
        confirm_msg_key = {
            "update": "confirm_update_msg",
            "inject": "confirm_inject_msg",
            "delete": "confirm_delete_msg"
        }[mode]
        confirm_msg = self.texts[self.language][confirm_msg_key]
        reply = QMessageBox.question(
            self, self.texts[self.language]["confirm_title"], 
            confirm_msg.format(file_count),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            file_list = [self.file_list_widget.item(i).text() for i in range(file_count)]

            self.process_thread = ProcessThread(
                file_list, 
                self.font_awesome_code, 
                self.css_code, 
                self.js_code, 
                self.html_code, 
                mode
            )
            self.process_thread.progress_updated.connect(self.update_progress)
            self.process_thread.file_processed.connect(self.on_file_processed)
            self.process_thread.operation_completed.connect(self.on_operation_complete)

            self.execute_btn.setEnabled(False)
            self.add_file_btn.setEnabled(False)
            self.remove_file_btn.setEnabled(False)
            self.clear_files_btn.setEnabled(False)
            self.toggle_lang_btn.setEnabled(False)
            self.font_awesome_edit.setEnabled(False)
            self.css_code_edit.setEnabled(False)
            self.js_code_edit.setEnabled(False)
            self.html_code_edit.setEnabled(False)
            self.statusBar.showMessage(self.texts[self.language]["processing_msg"])
            self.progress_bar.setValue(0)
            
            self.process_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def on_file_processed(self, file_path, success):
        status = self.texts[self.language]["success_status"] if success else self.texts[self.language]["fail_status"]
        self.statusBar.showMessage(self.texts[self.language]["file_processed_msg"].format(os.path.basename(file_path), status))
    
    def on_operation_complete(self, all_success):
        if all_success:
            QMessageBox.information(self, self.texts[self.language]["complete_title"], 
                                  self.texts[self.language]["success_msg"])
        else:
            QMessageBox.warning(self, self.texts[self.language]["partial_fail_title"], 
                              self.texts[self.language]["partial_fail_msg"])

        self.execute_btn.setEnabled(True)
        self.add_file_btn.setEnabled(True)
        self.remove_file_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        self.toggle_lang_btn.setEnabled(True)
        self.font_awesome_edit.setEnabled(True)
        self.css_code_edit.setEnabled(True)
        self.js_code_edit.setEnabled(True)
        self.html_code_edit.setEnabled(True)
        self.schedule_save()

    def start_json_watcher(self):
        self.json_watcher = QTimer(self)
        self.json_watcher.timeout.connect(self.check_json_changes)
        self.json_watcher.start(1000)

    def check_json_changes(self):
        if self.is_saving or self.is_loading:
            return
            
        if os.path.exists(self.file_list_path):
            mtime = os.path.getmtime(self.file_list_path)
            if mtime != self.last_json_mtime:
                print(f"检测到JSON文件变化，重新加载 (当前状态: 保存={self.is_saving}, 加载={self.is_loading})")
                self.last_json_mtime = mtime
                self.load_json()
                self.load_file_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRCMenuManager()
    sys.exit(app.exec())

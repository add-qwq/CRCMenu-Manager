# English:
# CRCMenu Manager

![GitHub release (latest by date)](https://img.shields.io/github/v/release/add-qwq/CRCMenu-Manager?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/add-qwq/CRCMenu-Manager?style=flat-square)
![Python version](https://img.shields.io/badge/Python-3.0%2B-blue?style=flat-square)
![License](https://img.shields.io/github/license/add-qwq/CRCMenu-Manager?style=flat-square)

This project is a GUI tool for managing the [Custom-Right-Click-Menu project](https://github.com/add-qwq/Custom-Right-Click-Menu). Embedding, updating, or removing right-click menus typically requires editing code files one by one, which is impractical for websites with numerous files. Therefore, this project provides three modes to simplify the process:

1. Inject Project
Eliminates the need to add external file references and HTML code to each file individually. Select the target files, input the required codes, and click "Execute Operation" to connect all files to the right-click menu component in one click.

2. Update Version
When the Custom-Right-Click-Menu project has updates, instead of modifying version numbers in each file manually, select the files, input the base code (without version numbers), and click "Execute Operation" to update all version numbers at once, refreshing browser cache.

3. Delete Project
If you need to remove previously added right-click menu code from multiple files, select the files, input the exact codes that were added (including version numbers), and click "Execute Operation" to batch delete them.

If you're interested, read on for detailed instructions.

---

This tool enables batch processing of HTML/PHP files, offering features like version updating, content injection, and content deletion. It automatically creates backup files with the .bak extension before making any modifications, ensuring data security. The bilingual interface allows users to switch between English and Simplified Chinese for easier use.

## Key Features
- Batch Processing: Handle multiple HTML/.htm/.php files simultaneously.
- Auto Backup: Create .bak backups of original files before modification.
- Version Update: Automatically update version numbers of CSS and JS files to refresh browser cache.
- Project Injection: Batch add external resource references (Font Awesome, CSS, JS) and HTML code for the right-click menu.
- Project Deletion: Batch remove previously added resource references and HTML code.
- Bilingual Interface: Switch between English and Simplified Chinese directly in the UI.
- Progress Tracking: Real-time progress bar and status updates for each processed file.
- Persistent Configuration: File list and codes are saved automatically and retained on next launch.

## Quick Start

### Option 1: Download Prebuilt EXE (Recommended)
No Python environment required:
1. Go to the [Releases page](https://github.com/add-qwq/CRCMenu-Manager/releases).
2. Download CRCMenu-Manager-EXE.zip and extract it.
3. Run CRCMenu-Manager.exe (automatically detects system language; use the language toggle in the UI if needed).

Security Note: If you prefer to verify the file, see Option 2 to build from source.

### Option 2: Run from Source Code
For developers or users who prefer local builds:

#### Prerequisites
- Python 3.0+
- Required packages:
  ```bash
  pip install pyside6
  ```

#### Steps
1. Download the source code:
   - Click Code → Download ZIP on the [GitHub repo](https://github.com/add-qwq/CRCMenu-Manager).
   - Extract the ZIP file.

2. Run the program:
   ```bash
   cd CRCMenu-Manager  # Navigate to the project folder
   python CRCMenu-Manager.py  # Launch the application
   ```

## Build EXE from Source (for verification)
If you don't trust prebuilt EXE files, you can compile the source code into an executable yourself:

```bash
pip install pyinstaller  # Install pyinstaller if not already installed
```

```bash
cd CRCMenu-Manager  # Navigate to the project folder
pyinstaller -w -F --name "CRCMenu-Manager.exe" CRCMenu-Manager.py  # Create the EXE for Windows
```

Parameters:
- -w: Hide the console window (GUI mode).
- -F: Generate a single EXE file.
- --name: Set the output file name.

For macOS/Linux: Use the same command, replacing ";" with ":" in file paths if necessary.

## Interface Overview
![English Interface](https://github.com/add-qwq/CRCMenu-Manager/blob/main/CRCMenu-Manager-EN.png?raw=true)
(Switch to Chinese via the "切换到中文" button in the UI.)

## How to Use

### Default Codes
Use the following default values or adjust them according to your needs:

Font Awesome Include Code:
```html
<link href="https://s4.zstatic.net/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

CSS Include Code:
```html
<link rel="stylesheet" href="/cdn/CRCMenu.css?v=4">
```

JS Include Code:
```html
<script src="/cdn/CRCMenu.js?v=8"></script>
```

Right-Click Menu HTML Code:
```html
<div id="custom-menu">
        <div class="menu-header" id="general-menu-header">常规操作</div>
        <div class="menu-item" id="back-item" onclick="backAction()">
            <i class="fa fa-arrow-left"></i>
            <span>返回</span>
        </div>
        <div class="menu-item" id="refresh-item" onclick="refreshAction()">
            <i class="fa fa-refresh"></i>
            <span>刷新</span>
        </div>

        <div class="menu-divider" id="edit-divider"></div>
        <div class="menu-header" id="edit-menu-header">编辑操作</div>
        <div class="menu-item" id="copy-item" onclick="copyAction()">
            <i class="fa fa-copy"></i>
            <span>复制</span>
        </div>
        <div class="menu-item" id="paste-item" onclick="pasteAction()">
            <i class="fa fa-paste"></i>
            <span>粘贴</span>
        </div>

        <div class="menu-divider" id="link-divider"></div>
        <div class="menu-header" id="link-menu-header">链接操作</div>
        <div class="menu-item" id="open-in-new-tab-item" onclick="openInNewTabAction()">
            <i class="fa fa-external-link"></i>
            <span>在新标签页打开</span>
        </div>
        <div class="menu-item" id="copy-link-item" onclick="copyLinkAction()">
            <i class="fa fa-link"></i>
            <span>复制链接地址</span>
        </div>

        <div class="menu-divider" id="image-divider"></div>
        <div class="menu-header" id="image-menu-header">图片操作</div>
        <div class="menu-item" id="open-image-in-new-tab-item" onclick="openImageInNewTabAction()">
            <i class="fa fa-external-link"></i>
            <span>在新标签页打开</span>
        </div>
        <div class="menu-item" id="copy-image-url-item" onclick="copyImageUrlAction()">
            <i class="fa fa-link"></i>
            <span>复制图片地址</span>
        </div>

        <div class="menu-divider" id="other-divider"></div>
        <div class="menu-header" id="other-menu-header">其他操作</div>
        <div class="menu-item" id="back-to-home-item" onclick="backToHomeAction()">
            <i class="fa fa-home"></i>
            <span>返回主页</span>
        </div>
    </div>
```

### 1. Inject Project
1. Select target files (if you have a previous configuration file CRCMenu-Manager_file_list.json, the file list will be retained automatically, no need to reselect).
2. Fill in the code fields with the default values (or your custom codes).
3. Select "Inject Project" from the dropdown menu.
4. Click "Execute Operation" and confirm the action.
5. Monitor progress via the status bar and progress bar.

### 2. Update Version
1. Select target files (if you have a previous configuration file, the file list will be retained automatically).
2. Fill in the code fields with your base codes (without version numbers). For example:
   - If you used `<script src="/cdn/CRCMenu.js?v=8"></script>` when injecting, input `<script src="/cdn/CRCMenu.js"></script>` here.
3. Select "Update Version" from the dropdown menu.
4. Click "Execute Operation" and confirm the action.
5. Monitor progress via the status bar and progress bar.

### 3. Delete Project
1. Select target files (if you have a previous configuration file, the file list will be retained automatically).
2. Fill in the code fields with the exact codes that were added (including version numbers). For example:
   - If you used `<link rel="stylesheet" href="/cdn/CRCMenu.css?v=4">` when injecting, input the same code here.
3. Select "Delete Project" from the dropdown menu.
4. Click "Execute Operation" and confirm the action.
5. Monitor progress via the status bar and progress bar.

### Post-Operation
- A success message will appear if all files are processed successfully.
- For partial failures, check the status bar for details.

Note: Your configuration (file list and codes) is saved automatically in CRCMenu-Manager_file_list.json and will be loaded on next launch.

## License
This project is licensed under the [Apache License 2.0](https://github.com/add-qwq/CRCMenu-Manager/blob/main/LICENSE).

## Feedback
- Issue Tracking: Report bugs or request features on the [Issues page](https://github.com/add-qwq/CRCMenu-Manager/issues).
- Contributions: Fork the repo and submit pull requests for improvements.

---

# 中文：
# CRCMenu 管理工具

![GitHub release (latest by date)](https://img.shields.io/github/v/release/add-qwq/CRCMenu-Manager?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/add-qwq/CRCMenu-Manager?style=flat-square)
![Python version](https://img.shields.io/badge/Python-3.0%2B-blue?style=flat-square)
![License](https://img.shields.io/github/license/add-qwq/CRCMenu-Manager?style=flat-square)

本项目是一个用于管理[Custom-Right-Click-Menu项目](https://github.com/add-qwq/Custom-Right-Click-Menu)的GUI工具。由于右键菜单的嵌入、更新或删除通常需要逐个编辑代码文件，这对于拥有大量文件的网站来说并不现实。因此，该项目提供了三种模式来简化操作：

1. 引入项目
无需逐个在文件中添加外部文件引用和HTML代码，只需选择目标文件，输入所需代码，点击“执行操作”即可一键将所有文件接入右键菜单组件。

2. 更新版本
当Custom-Right-Click-Menu项目有更新时，无需逐个修改文件中的版本号，选择文件，输入基础代码（不含版本号），点击“执行操作”即可一键更新所有版本号，刷新浏览器缓存。

3. 删除项目
如果需要从多个文件中移除之前添加的右键菜单代码，选择文件，输入添加时使用的确切代码（包含版本号），点击“执行操作”即可批量删除。

如果你感兴趣，请继续往下阅读详细介绍。

---

该工具支持批量处理HTML/PHP文件，提供版本更新、内容注入和内容删除等功能。修改文件前会自动创建扩展名为.bak的备份文件，确保数据安全。双语界面支持英文和简体中文切换，方便不同语言用户使用。

## 核心功能
- 批量处理：同时处理多个HTML/.htm/.php文件
- 自动备份：修改前自动创建原文件的.bak备份
- 版本更新：自动更新CSS和JS文件的版本号，以刷新浏览器缓存
- 项目引入：批量添加外部资源引用（Font Awesome、CSS、JS）和右键菜单的HTML代码
- 项目删除：批量移除之前添加的资源引用和HTML代码
- 双语界面：直接在界面中切换英文和简体中文
- 进度监控：实时显示每个文件的处理进度和状态
- 配置持久化：文件列表和代码自动保存，下次启动时自动加载

## 快速开始

### 方式1：下载预编译EXE（推荐）
无需安装Python环境：
1. 前往[Releases页面](https://github.com/add-qwq/CRCMenu-Manager/releases)
2. 下载CRCMenu-Manager-EXE.zip并解压
3. 运行CRCMenu-Manager.exe（自动检测系统语言，也可通过界面中的语言切换按钮调整）

安全说明：如果希望验证文件安全性，可参考方式2从源码构建

### 方式2：从源代码运行
适合开发者或偏好本地构建的用户：

#### 环境要求
- Python 3.0+
- 所需依赖包：
  ```bash
  pip install pyside6
  ```

#### 步骤
1. 下载源代码：
   - 在[GitHub仓库](https://github.com/add-qwq/CRCMenu-Manager)点击Code→Download ZIP
   - 解压ZIP文件

2. 运行程序：
   ```bash
   cd CRCMenu-Manager  # 进入项目文件夹
   python CRCMenu-Manager.py  # 启动应用程序
   ```

## 从源码编译EXE（用于验证）
如果不信任预编译的EXE文件，可自行将源代码编译为可执行文件：

```bash
pip install pyinstaller  # 如未安装pyinstaller，先执行此命令
```

```bash
cd CRCMenu-Manager  # 进入项目文件夹
pyinstaller -w -F --name "CRCMenu-Manager.exe" CRCMenu-Manager.py  # 生成Windows系统的EXE文件
```

参数说明：
- -w：隐藏控制台窗口（图形界面模式）
- -F：生成单个EXE文件
- --name：设置输出文件名称

适用于macOS/Linux：使用相同命令，必要时将文件路径中的“;”替换为“:”

## 界面概览
![中文界面](https://github.com/add-qwq/CRCMenu-Manager/blob/main/CRCMenu-Manager-CN.png?raw=true)
（通过界面中的“Switch to English”按钮切换为英文界面）

## 使用指南

### 默认代码
可使用以下默认值，也可根据需求自行调整：

Font Awesome引入代码：
```html
<link href="https://s4.zstatic.net/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

CSS引入代码：
```html
<link rel="stylesheet" href="/cdn/CRCMenu.css?v=4">
```

JS引入代码：
```html
<script src="/cdn/CRCMenu.js?v=8"></script>
```

右键菜单HTML代码：
```html
<div id="custom-menu">
        <div class="menu-header" id="general-menu-header">常规操作</div>
        <div class="menu-item" id="back-item" onclick="backAction()">
            <i class="fa fa-arrow-left"></i>
            <span>返回</span>
        </div>
        <div class="menu-item" id="refresh-item" onclick="refreshAction()">
            <i class="fa fa-refresh"></i>
            <span>刷新</span>
        </div>

        <div class="menu-divider" id="edit-divider"></div>
        <div class="menu-header" id="edit-menu-header">编辑操作</div>
        <div class="menu-item" id="copy-item" onclick="copyAction()">
            <i class="fa fa-copy"></i>
            <span>复制</span>
        </div>
        <div class="menu-item" id="paste-item" onclick="pasteAction()">
            <i class="fa fa-paste"></i>
            <span>粘贴</span>
        </div>

        <div class="menu-divider" id="link-divider"></div>
        <div class="menu-header" id="link-menu-header">链接操作</div>
        <div class="menu-item" id="open-in-new-tab-item" onclick="openInNewTabAction()">
            <i class="fa fa-external-link"></i>
            <span>在新标签页打开</span>
        </div>
        <div class="menu-item" id="copy-link-item" onclick="copyLinkAction()">
            <i class="fa fa-link"></i>
            <span>复制链接地址</span>
        </div>

        <div class="menu-divider" id="image-divider"></div>
        <div class="menu-header" id="image-menu-header">图片操作</div>
        <div class="menu-item" id="open-image-in-new-tab-item" onclick="openImageInNewTabAction()">
            <i class="fa fa-external-link"></i>
            <span>在新标签页打开</span>
        </div>
        <div class="menu-item" id="copy-image-url-item" onclick="copyImageUrlAction()">
            <i class="fa fa-link"></i>
            <span>复制图片地址</span>
        </div>

        <div class="menu-divider" id="other-divider"></div>
        <div class="menu-header" id="other-menu-header">其他操作</div>
        <div class="menu-item" id="back-to-home-item" onclick="backToHomeAction()">
            <i class="fa fa-home"></i>
            <span>返回主页</span>
        </div>
    </div>
```

### 1. 引入项目
1. 选择目标文件（如果有之前的配置文件CRCMenu-Manager_file_list.json，文件列表会自动保留，无需重新选择）。
2. 在代码输入框中填写默认值（或自定义代码）。
3. 从下拉菜单中选择“引入项目”。
4. 点击“执行操作”并确认。
5. 通过状态栏和进度条监控处理进度。

### 2. 更新版本
1. 选择目标文件（如果有之前的配置文件，文件列表会自动保留）。
2. 在代码输入框中填写基础代码（不含版本号）。例如：
   - 若引入时使用的是`<script src="/cdn/CRCMenu.js?v=8"></script>`，此处输入`<script src="/cdn/CRCMenu.js"></script>`。
3. 从下拉菜单中选择“更新版本”。
4. 点击“执行操作”并确认。
5. 通过状态栏和进度条监控处理进度。

### 3. 删除项目
1. 选择目标文件（如果有之前的配置文件，文件列表会自动保留）。
2. 在代码输入框中填写添加时使用的确切代码（包含版本号）。例如：
   - 若引入时使用的是`<link rel="stylesheet" href="/cdn/CRCMenu.css?v=4">`，此处输入相同代码。
3. 从下拉菜单中选择“删除项目”。
4. 点击“执行操作”并确认。
5. 通过状态栏和进度条监控处理进度。

### 操作完成后
- 若所有文件处理成功，将显示成功提示。
- 若部分文件处理失败，可在状态栏查看详细信息。

注意：你的配置（文件列表和代码）会自动保存在CRCMenu-Manager_file_list.json中，下次启动时会自动加载。

## 许可证
本项目采用[Apache License 2.0](https://github.com/add-qwq/CRCMenu-Manager/blob/main/LICENSE)许可证。

## 反馈与贡献
- 问题反馈：在[Issues页面](https://github.com/add-qwq/CRCMenu-Manager/issues)提交bug或功能请求。
- 代码贡献：Fork仓库并提交拉取请求。

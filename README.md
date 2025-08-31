# English:
# CRCMenu Manager

![GitHub release (latest by date)](https://img.shields.io/github/v/release/add-qwq/CRCMenu-Manager?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/add-qwq/CRCMenu-Manager?style=flat-square)
![Python version](https://img.shields.io/badge/Python-3.0%2B-blue?style=flat-square)
![License](https://img.shields.io/github/license/add-qwq/CRCMenu-Manager?style=flat-square)

This project is a GUI tool for managing the [Custom-Right-Click-Menu project](https://github.com/add-qwq/Custom-Right-Click-Menu). Embedding, updating, or removing right-click menu-related resources (Font Awesome and JS) typically requires editing code files one by one, which is impractical for websites with numerous files. Therefore, this project provides three targeted modes to simplify the process:

1. Inject Content
Eliminates the need to manually add Font Awesome and JS references to each file. Select target files, input the required codes (JS is mandatory, Font Awesome is optional), and click "Execute Operation" to inject Font Awesome into the `<head>` and JS before `</body>` in all files with one click.

2. Update JS Version
When the Custom-Right-Click-Menu's JS file is updated, there’s no need to manually modify version numbers in each file. Select files, input the base JS code (without `?v=` version suffix), and click "Execute Operation"—the tool automatically generates an 8-digit MD5 hash (based on timestamp) as the version number to refresh browser cache.

3. Delete Content
If you need to remove previously added Font Awesome and JS codes from multiple files, select the files, input the **exact same codes** used during injection (including version numbers), and click "Execute Operation" to batch delete them.

If you're interested, read on for detailed instructions.

---

This tool enables batch processing of HTML/PHP files, offering features like JS version updating, content injection, and content deletion. It automatically creates backup files with the `.bak` extension before making any modifications to ensure data security. The bilingual interface (English/Simplified Chinese) and real-time configuration management (auto-save, external change detection) further enhance usability.

## Key Features
- **Batch Processing**: Handle multiple HTML/.htm/.php files simultaneously.
- **Auto Backup**: Create `.bak` backups of original files before modification to prevent data loss.
- **Smart JS Versioning**: Automatically generate an 8-digit MD5 hash (based on timestamp) for JS files to refresh browser cache.
- **Content Injection**: Batch add Font Awesome references (inserted before `</head>`) and JS references (inserted before `</body>`).
- **Content Deletion**: Batch remove previously added Font Awesome and JS codes (requires exact code matching).
- **Bilingual Interface**: Switch directly between English and Simplified Chinese in the UI.
- **Real-Time Progress Tracking**: Monitor processing status of each file via a progress bar and status bar.
- **Persistent Configuration**:
  - Auto-save: Timed save of file lists and input codes when changes occur.
  - External Change Detection: Automatically reload the configuration file if modified externally.

## Quick Start

### Option 1: Download Prebuilt EXE (Recommended)
No Python environment required:
1. Go to the [Releases page](https://github.com/add-qwq/CRCMenu-Manager/releases).
2. Download `CRCMenu-Manager-EXE.zip` and extract it.
3. Run `CRCMenu-Manager.exe` (automatically detects system language; use the language toggle in the UI if needed).

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
   - Click **Code → Download ZIP** on the [GitHub repo](https://github.com/add-qwq/CRCMenu-Manager).
   - Extract the ZIP file.

2. Run the program:
   ```bash
   cd CRCMenu-Manager  # Navigate to the project folder
   python CRCMenu-Manager.py  # Launch the application
   ```

## Build EXE from Source (for verification)
If you don't trust prebuilt EXE files, compile the source code into an executable yourself:

```bash
pip install pyinstaller  # Install pyinstaller if not already installed
```

```bash
cd CRCMenu-Manager  # Navigate to the project folder
pyinstaller -w -F --name "CRCMenu-Manager.exe" CRCMenu-Manager.py  # Create Windows EXE
```

Parameters:
- `-w`: Hide the console window (GUI mode).
- `-F`: Generate a single EXE file.
- `--name`: Set the output file name.

For macOS/Linux: Use the same command, replacing ";" with ":" in file paths if necessary.

## Interface Overview
![English Interface](https://github.com/add-qwq/CRCMenu-Manager/blob/main/CRCMenu-Manager-EN.png?raw=true)
- **Mode Dropdown**: Select "Update JS Version", "Inject Content", or "Delete Content".
- **Input Fields**: Two fields for Font Awesome (optional) and JS (mandatory) codes.
- **File List**: View, add, remove, or clear selected files.
- **Language Toggle**: Switch between English and Simplified Chinese via the "切换到中文" button.
- **Progress Bar**: Track batch processing progress in real time.

(Switch to Chinese via the "切换到中文" button in the UI.)

## How to Use

### Default Codes
Use the following default values or adjust them according to your needs:

#### Font Awesome Include Code (Optional)
```html
<link href="https://s4.zstatic.net/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

#### JS Include Code (Mandatory)
```html
<script src="/cdn/CRCMenu.js?v=8"></script>
```


### 1. Inject Content
Inject Font Awesome (to `<head>`) and JS (to `</body>`) into target files:
1. **Select Files**: Click "Select Files" to add HTML/PHP files. If a previous configuration file (`CRCMenu-Manager_file_list.json`) exists, the file list will load automatically.
2. **Input Codes**:
   - Paste the Font Awesome code (optional) into the first field.
   - Paste the JS code (mandatory) into the second field.
3. **Select Mode**: Choose "Inject Content" from the dropdown menu.
4. **Execute**: Click "Execute Operation" and confirm the action (backups will be created automatically).
5. **Monitor Progress**: Check the status bar for real-time feedback on each file’s processing result.


### 2. Update JS Version
Automatically update the version number of JS files to refresh browser cache:
1. **Select Files**: Load existing files from the configuration or add new ones.
2. **Input Base JS Code**: Paste the JS code **without the version suffix** (e.g., if you injected `<script src="/cdn/CRCMenu.js?v=8"></script>`, input `<script src="/cdn/CRCMenu.js"></script>` here).
3. **Select Mode**: Choose "Update JS Version" from the dropdown menu.
4. **Execute**: Click "Execute Operation"—the tool will generate an 8-digit MD5 hash (based on timestamp) and append it as `?v=xxxxxxx` to the JS code.
5. **Verify**: After processing, JS files will look like `<script src="/cdn/CRCMenu.js?v=a1b2c3d4"></script>`.


### 3. Delete Content
Remove previously injected Font Awesome and JS codes from files:
1. **Select Files**: Load the same files used during injection.
2. **Input Exact Codes**: Paste the **exact same codes** used for injection (including version numbers). For example:
   - Font Awesome: Use the same code as injected (if any).
   - JS: Use the full code with version (e.g., `<script src="/cdn/CRCMenu.js?v=8"></script>`).
3. **Select Mode**: Choose "Delete Content" from the dropdown menu.
4. **Execute**: Click "Execute Operation" and confirm. The tool will remove the exact matching codes from each file.
5. **Check Results**: The status bar will show whether each file was processed successfully.


### Post-Operation Notes
- **Success**: A pop-up will confirm if all files are processed successfully.
- **Partial Failure**: If some files fail, check the status bar for error details (e.g., file permission issues).
- **Configuration Persistence**: Your file list and input codes are automatically saved to `CRCMenu-Manager_file_list.json` and will load on the next launch.


## License
This project is licensed under the [Apache License 2.0](https://github.com/add-qwq/CRCMenu-Manager/blob/main/LICENSE).

## Feedback
- **Issue Tracking**: Report bugs or request features on the [Issues page](https://github.com/add-qwq/CRCMenu-Manager/issues).
- **Contributions**: Fork the repository and submit pull requests to improve the tool.


# 中文：
# CRCMenu 管理工具

![GitHub release (latest by date)](https://img.shields.io/github/v/release/add-qwq/CRCMenu-Manager?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/add-qwq/CRCMenu-Manager?style=flat-square)
![Python version](https://img.shields.io/badge/Python-3.0%2B-blue?style=flat-square)
![License](https://img.shields.io/github/license/add-qwq/CRCMenu-Manager?style=flat-square)

本项目是用于管理[Custom-Right-Click-Menu项目](https://github.com/add-qwq/Custom-Right-Click-Menu)的GUI工具。右键菜单相关资源（Font Awesome和JS）的嵌入、版本更新或删除通常需要逐个编辑代码文件，这对于拥有大量文件的网站来说效率低下。因此，该工具提供三种针对性模式简化操作：

1. 注入内容
无需手动为每个文件添加Font Awesome和JS引用，选择目标文件，输入所需代码（JS为必填，Font Awesome为选填），点击“执行操作”即可一键将Font Awesome注入`<head>`、JS注入`</body>`前。

2. 更新JS版本
当Custom-Right-Click-Menu的JS文件更新时，无需逐个修改文件中的版本号。选择文件，输入不含`?v=`版本后缀的基础JS代码，点击“执行操作”——工具会自动基于时间戳生成8位MD5哈希作为版本号，强制刷新浏览器缓存。

3. 删除内容
若需从多个文件中移除之前注入的Font Awesome和JS代码，选择文件，输入与注入时**完全一致的代码**（含版本号），点击“执行操作”即可批量删除。

如果你感兴趣，请继续阅读详细说明。

---

该工具支持批量处理HTML/PHP文件，提供JS版本更新、内容注入、内容删除等核心功能。修改文件前会自动创建扩展名为`.bak`的备份文件，确保数据安全；同时具备双语界面（英文/简体中文）和实时配置管理（自动保存、外部修改检测），进一步提升使用体验。

## 核心功能
- **批量处理**：同时处理多个HTML/.htm/.php文件
- **自动备份**：修改前为原文件创建`.bak`备份，防止数据丢失
- **智能JS版本**：自动基于时间戳生成8位MD5哈希作为JS版本号，刷新浏览器缓存
- **内容注入**：批量添加Font Awesome引用（插入`<head>`前）和JS引用（插入`</body>`前）
- **内容删除**：批量移除已注入的Font Awesome和JS代码（需完全匹配注入代码）
- **双语界面**：直接在界面中切换英文和简体中文
- **实时进度监控**：通过进度条和状态栏实时查看每个文件的处理状态
- **配置持久化**：
  - 自动保存：输入内容或文件列表变化时定时保存，避免数据丢失
  - 外部修改检测：若配置文件被外部修改，自动重新加载最新内容

## 快速开始

### 方式1：下载预编译EXE（推荐）
无需安装Python环境：
1. 前往[Releases页面](https://github.com/add-qwq/CRCMenu-Manager/releases)
2. 下载`CRCMenu-Manager-EXE.zip`并解压
3. 运行`CRCMenu-Manager.exe`（自动检测系统语言，也可通过界面中的语言切换按钮调整）

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
   - 在[GitHub仓库](https://github.com/add-qwq/CRCMenu-Manager)点击**Code→Download ZIP**
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
- `-w`：隐藏控制台窗口（图形界面模式）
- `-F`：生成单个EXE文件
- `--name`：设置输出文件名称

适用于macOS/Linux：使用相同命令，必要时将文件路径中的“;”替换为“:”

## 界面概览
![中文界面](https://github.com/add-qwq/CRCMenu-Manager/blob/main/CRCMenu-Manager-CN.png?raw=true)
- **模式下拉框**：选择“更新JS版本”“注入内容”或“删除内容”
- **输入框**：两个输入框分别用于Font Awesome（选填）和JS（必填）代码
- **文件列表**：查看、添加、移除或清空已选择的文件
- **语言切换**：通过“Switch to English”按钮切换为英文界面
- **进度条**：实时显示批量处理的进度

（通过界面中的“Switch to English”按钮切换为英文界面）

## 使用指南

### 默认代码
可使用以下默认值，也可根据需求自行调整：

#### Font Awesome引入代码（选填）
```html
<link href="https://s4.zstatic.net/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

#### JS引入代码（必填）
```html
<script src="/cdn/CRCMenu.js?v=8"></script>
```


### 1. 注入内容
向目标文件中注入Font Awesome（到`<head>`）和JS（到`</body>`前）：
1. **选择文件**：点击“选择文件”添加HTML/PHP文件。若存在历史配置文件（`CRCMenu-Manager_file_list.json`），文件列表会自动加载。
2. **输入代码**：
   - 在第一个输入框粘贴Font Awesome代码（可选）。
   - 在第二个输入框粘贴JS代码（必填，不可为空）。
3. **选择模式**：从下拉菜单中选择“注入内容”。
4. **执行操作**：点击“执行操作”并确认（工具会自动为原文件创建备份）。
5. **监控进度**：通过状态栏实时查看每个文件的处理结果（成功/失败）。


### 2. 更新JS版本
自动更新JS文件的版本号，强制刷新浏览器缓存：
1. **选择文件**：从配置中加载历史文件或添加新文件。
2. **输入基础JS代码**：粘贴不含版本后缀的JS代码。例如：若注入时使用`<script src="/cdn/CRCMenu.js?v=8"></script>`，此处需输入`<script src="/cdn/CRCMenu.js"></script>`。
3. **选择模式**：从下拉菜单中选择“更新JS版本”。
4. **执行操作**：点击“执行操作”——工具会基于当前时间戳生成8位MD5哈希，并自动追加为`?v=xxxxxxx`后缀。
5. **验证结果**：处理后JS代码会变为类似`<script src="/cdn/CRCMenu.js?v=a1b2c3d4"></script>`的形式。


### 3. 删除内容
从文件中移除之前注入的Font Awesome和JS代码：
1. **选择文件**：加载与注入时相同的目标文件。
2. **输入完全匹配的代码**：粘贴与注入时**完全一致的代码**（含版本号）。例如：
   - Font Awesome：若注入时使用了相关代码，需输入完全相同的代码。
   - JS：需输入含版本号的完整代码（如`<script src="/cdn/CRCMenu.js?v=8"></script>`）。
3. **选择模式**：从下拉菜单中选择“删除内容”。
4. **执行操作**：点击“执行操作”并确认，工具会从每个文件中移除完全匹配的代码。
5. **查看结果**：状态栏会显示每个文件的删除结果（成功/失败）。


### 操作完成后说明
- **全部成功**：会弹出提示框，确认所有文件处理完成。
- **部分失败**：若部分文件处理失败，可在状态栏查看详细原因（如文件权限不足、代码不匹配等）。
- **配置持久化**：文件列表和输入的代码会自动保存到`CRCMenu-Manager_file_list.json`，下次启动工具时会自动加载。


## 许可证
本项目采用[Apache License 2.0](https://github.com/add-qwq/CRCMenu-Manager/blob/main/LICENSE)许可证。

## 反馈与贡献
- **问题反馈**：在[Issues页面](https://github.com/add-qwq/CRCMenu-Manager/issues)提交bug或功能请求。
- **代码贡献**：Fork仓库并提交拉取请求，参与工具的改进与优化。

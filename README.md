# 🐱 桌面宠物 (Desktop Pets)

一款可爱的桌面宠物应用，支持多平台运行，让你的桌面更加生动有趣！

## ✨ 功能特性

- 🐾 **多种宠物** - 支持橘猫、小猫咪、小狗狗、小兔子等多种宠物
- 🏃 **动画效果** - 流畅的待机、行走、跳跃动画
- 💬 **智能问候** - 根据时间段显示不同的问候语
- 🎨 **自定义配置** - 支持配置宠物大小、移动速度、问候语等
- 🖱️ **交互功能** - 点击跳跃、右键菜单、自动移动
- 🌐 **跨平台** - 支持 Linux、Windows、macOS

## 🚀 快速开始

### 方式一：Electron 版本（推荐）

**安装依赖**
```bash
npm install
```

**开发模式**
```bash
npm run dev
```

**构建生产版本**
```bash
# Linux
npm run dist:linux

# Windows
npm run dist:win

# macOS
npm run dist:mac
```

### 方式二：Python 版本

**安装依赖**
```bash
pip install PyQt5 Pillow
```

**运行**
```bash
python3 desktop_pet.py
```

**打包（可选）**
```bash
# 使用 PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed desktop_pet.py
```

## 📁 项目结构

```
desktop-pets/
├── src/
│   ├── main.js          # Electron 主进程
│   ├── preload.js       # Electron 预加载脚本
│   └── desktop_pet.py   # Python 版本主文件
├── index.html           # Electron 渲染进程
├── assets/
│   └── pets/            # 宠物素材目录
│       ├── orange_cat/  # 橘猫
│       ├── cat/         # 小猫咪
│       ├── dog/         # 小狗狗
│       └── bunny/       # 小兔子
├── config/
│   └── greetings.json   # 问候语配置
├── build/
│   └── icons/           # 应用图标
├── package.json
└── .github/workflows/
    └── electron-build.yml  # GitHub Actions 配置
```

## 📝 配置说明

### 主配置文件 (`config/greetings.json`)

```json
{
  "current_pet": "orange_cat",
  "interval_seconds": 30,
  "display_duration_seconds": 5,
  "move_speed": 3,
  "idle_timeout_seconds": 5,
  "pet_size": 128,
  "animation_interval_ms": 150,
  "greetings": {
    "morning": ["早上好！", "今天也要加油哦！"],
    "noon": ["该吃午饭啦！", "休息一下吧~"],
    "afternoon": ["下午好！", "继续加油！"],
    "evening": ["晚上好！", "辛苦了一天！"],
    "night": ["夜深了，早点休息吧！", "晚安！"]
  }
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `current_pet` | 当前宠物名称 | orange_cat |
| `interval_seconds` | 问候语间隔（秒） | 30 |
| `display_duration_seconds` | 气泡显示时长（秒） | 5 |
| `move_speed` | 移动速度（像素/帧） | 3 |
| `idle_timeout_seconds` | 空闲自动移动超时（秒） | 5 |
| `pet_size` | 宠物大小（像素） | 128 |
| `animation_interval_ms` | 动画帧间隔（毫秒） | 150 |

### 添加自定义宠物

1. 在 `assets/pets/` 下创建新文件夹（如 `my_pet/`）
2. 创建 `config.json` 配置文件：
```json
{
  "name": "我的宠物",
  "size": 128,
  "frames": {
    "idle": ["idle_0.png", "idle_1.png"],
    "walk": ["walk_0.png", "walk_1.png"],
    "jump": ["jump_0.png", "jump_1.png"]
  }
}
```
3. 将动画帧图片放入该文件夹
4. 在 `config/greetings.json` 中设置 `"current_pet": "my_pet"`

## 🎮 使用方法

| 操作 | 效果 |
|------|------|
| 左键点击 | 宠物跳跃并移动到新位置 |
| 右键点击 | 显示菜单（跳跃、移动、退出） |
| 自动移动 | 空闲一段时间后自动移动 |

## 🛠️ 技术栈

### Electron 版本
- **框架**: Electron 28
- **语言**: JavaScript
- **UI**: HTML5 Canvas
- **构建工具**: electron-builder

### Python 版本
- **框架**: PyQt5
- **语言**: Python 3
- **图像处理**: Pillow
- **打包工具**: PyInstaller

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

🐱 让你的桌面不再孤单！

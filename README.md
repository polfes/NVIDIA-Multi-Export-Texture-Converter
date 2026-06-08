# 🎮 NVIDIA Multi Export Texture Converter

> RU [Русская версия](./README.ru.md)

> EN [English version](./README.md)

**Multi / Portable PNG ↔ DDS texture converter based on NVIDIA Texture Tools. Single EXE file, no installation required.**

[![Version](https://img.shields.io/badge/version-1.3.3.7-red)](https://github.com/polfes/NVIDIA-Multi-Export-Texture-Converter/releases)
[![Windows](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/polfes/NVIDIA-Multi-Export-Texture-Converter/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Features

- 🔄 **Bidirectional conversion** - PNG ↔ DDS
- 📦 **Single EXE file** - Fully portable, no installation
- 🎯 **Drag & Drop support** - Just drag files onto the EXE
- 🚀 **6 compression formats** - BC1, BC2, BC3/DXT5, BC4, BC5, BC7
- 🎨 **Alpha channel support** - Preserves transparency
- ⚡ **NVIDIA Texture Tools engine** - Professional quality compression
- 💻 **No dependencies** - Works on clean Windows 10/11

## 📋 Available Formats

| Format | Description | Best for |
|--------|-------------|----------|
| **BC1 (DXT1)** | No alpha, smallest size | Opaque textures |
| **BC2 (DXT3)** | Sharp 4-bit alpha | UI with hard edges |
| **BC3 (DXT5)** | Smooth interpolated alpha | ★ **RECOMMENDED** for most |
| **BC4 (ATI1)** | Single channel | Height maps, masks |
| **BC5 (ATI2)** | Two channel | Normal maps |
| **BC7** | High quality | DirectX 11+ games |

## 🚀 How to Use

### Method 1: Drag & Drop (Recommended)
1. Drag PNG or DDS files onto `TextureConverter.exe`
2. Select format (for PNG → DDS)
3. Wait for completion
4. Done! Files appear next to originals

### Method 2: Command Line
```bash
TextureConverter.exe "C:\MyTextures"
```

## 💻 How to compile (You need to have the "NVIDIA Texture Tools" folder in the folder where you will compile the exe)
```bash
pyinstaller --onefile --name "TextureConverter" --add-data "NVIDIA Texture Tools;NVIDIA Texture Tools" --console --uac-admin --icon="icon.ico" --version-file="version.txt" texture_converter.py
```

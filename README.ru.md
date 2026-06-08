# 🎮 NVIDIA Multi Export Texture Converter 

> RU [Русская версия](./README.ru.md)

> EN [English version](./README.md)

**Портативный / Массовый конвертер текстур PNG ↔ DDS на основе инструментов NVIDIA Texture Tools.** Один EXE-файл, установка не требуется.**

[![Версия](https://img.shields.io/badge/version-1.3.3.7-red)](https://github.com/polfes/NVIDIA-Multi-Export-Texture-Converter/releases)
[![Windows](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/polfes/NVIDIA-Multi-Export-Texture-Converter/releases)
[![Лицензия](https://img.shields.io/badge/license-MIT-green)](ЛИЦЕНЗИЯ)

## ✨ Особенности

- 🔄 **Двунаправленное преобразование** - PNG ↔ DDS
- 📦 **Один EXE-файл** - Полностью портативный, установка не требуется
- 🎯 **Поддержка перетаскивания** - Просто перетащите файлы на EXE-файл
- 🚀 **6 форматов сжатия** - BC1, BC2, BC3/DXT5, BC4, BC5, BC7
- 🎨 **Поддержка альфа-канала** - Сохраняет прозрачность
- ⚡ **Движок текстурных инструментов NVIDIA** - Сжатие профессионального качества
- 💻 **Без зависимостей** - Работает на чистой Windows 10/11

## 📋 Доступные форматы

| Format | Description | Best for |
|--------|-------------|----------|
| **BC1 (DXT1)** | No alpha, smallest size | Opaque textures |
| **BC2 (DXT3)** | Sharp 4-bit alpha | UI with hard edges |
| **BC3 (DXT5)** | Smooth interpolated alpha | ★ **RECOMMENDED** for most |
| **BC4 (ATI1)** | Single channel | Height maps, masks |
| **BC5 (ATI2)** | Two channel | Normal maps |
| **BC7** | High quality | DirectX 11+ games |

## 🚀 Как использовать

### Способ 1: Перетаскивание (рекомендуется)
1. Перетащите файлы PNG или DDS на `TextureConverter.exe`
2. Выберите формат (для PNG → DDS)
3. Дождитесь завершения
4. Готово! Файлы появятся рядом с оригиналами

### Способ 2: Командная строка
```bash
TextureConverter.exe "C:\MyTextures"
```

## 💻 Инструкция по компиляции (Вам потребуется папка "NVIDIA Texture Tools" в той же папке, куда вы будете компилировать исполняемый файл)
```bash
pyinstaller --onefile --name "TextureConverter" --add-data "NVIDIA Texture Tools;NVIDIA Texture Tools" --console --uac-admin --icon="icon.ico" --version-file="version.txt" texture_converter.py
```

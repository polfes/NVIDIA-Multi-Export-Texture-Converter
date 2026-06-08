#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import signal
import atexit
import tempfile
import shutil
from pathlib import Path

# ANSI color codes
RED_BOLD = '\033[91;1m'
RESET = '\033[0m'

def cleanup():
    """Reset console color and cleanup temp files on exit"""
    if os.name == 'nt':
        os.system('color 07')
    
    global TEMP_DIR
    if TEMP_DIR and TEMP_DIR.exists():
        try:
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        except:
            pass

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    cleanup()
    print(f"\n\n{RED_BOLD}[!] Cancelled by user. Goodbye!{RESET}")
    input(f"{RED_BOLD}Press Enter to exit...{RESET}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup)

def extract_nvtt_folder():
    """Extract entire NVIDIA Texture Tools folder from within the EXE"""
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE
        temp_dir = Path(tempfile.gettempdir()) / "TextureConverterTemp"
        temp_dir.mkdir(exist_ok=True)
        
        nvtt_folder = temp_dir / "NVIDIA Texture Tools"
        nvtt_exe = nvtt_folder / "nvtt_export.exe"
        
        # Only extract if not already extracted
        if not nvtt_exe.exists():
            try:
                # Get the embedded folder from PyInstaller bundle
                base_path = Path(sys._MEIPASS)
                source_folder = base_path / "NVIDIA Texture Tools"
                
                if source_folder.exists():
                    # Copy entire folder
                    shutil.copytree(source_folder, nvtt_folder, dirs_exist_ok=True)
                    print(f"{RED_BOLD}[OK] Extracted NVIDIA Texture Tools folder{RESET}")
                else:
                    print(f"{RED_BOLD}[ERROR] NVIDIA Texture Tools folder not found in bundle!{RESET}")
                    return None
            except Exception as e:
                print(f"{RED_BOLD}[ERROR] Failed to extract: {e}{RESET}")
                return None
        
        return nvtt_exe
    else:
        # Running as script - look for local folder
        local_folder = Path(__file__).parent / "NVIDIA Texture Tools"
        local_exe = local_folder / "nvtt_export.exe"
        if local_exe.exists():
            return local_exe
        
        # Try system installation
        system_paths = [
            r"C:\Program Files\NVIDIA Corporation\NVIDIA Texture Tools\nvtt_export.exe",
            r"C:\Program Files (x86)\NVIDIA Corporation\NVIDIA Texture Tools\nvtt_export.exe",
        ]
        for path in system_paths:
            if Path(path).exists():
                return Path(path)
        
        return None

def set_console_red_bold():
    """Sets console to red bold color mode"""
    if os.name == 'nt':
        os.system('color 0C')
        os.system('')
    print(f"{RED_BOLD}", end='', flush=True)

def reset_console_color():
    """Resets console color"""
    if os.name == 'nt':
        os.system('color 07')
    print(f"{RESET}", end='', flush=True)

def print_logo():
    """Prints ASCII art logo in bold red"""
    logo = f"""
{RED_BOLD}███─███─██─██─███─█─█─████─███────███─████─████─█──────███─██─██─████─████─████─███─███─████
─█──█────███───█──█─█─█──█─█───────█──█──█─█──█─█──────█────███──█──█─█──█─█──█──█──█───█──█
─█──███───█────█──█─█─████─███─────█──█──█─█──█─█──────███───█───████─█──█─████──█──███─████
─█──█────███───█──█─█─█─█──█───────█──█──█─█──█─█──────█────███──█────█──█─█─█───█──█───█─█─
─█──███─██─██──█──███─█─█──███─────█──████─████─███────███─██─██─█────████─█─█───█──███─█─█─

████──██─██────████─████─█───███─███─███─███─███
█──██──███─────█──█─█──█─█───█───█───█───█───█──
████────█──────████─█──█─█───███─███─███─███─███
█──██───█──────█────█──█─█───█───█─────█───█───█
████────█──────█────████─███─█───███─███─███─███{RESET}
"""
    print(logo)

def print_header():
    """Prints header in bold red"""
    print_logo()
    print(f"{RED_BOLD}{'='*70}{RESET}")
    print(f"{RED_BOLD}   PORTABLE TEXTURE CONVERTER (PNG <-> DDS){RESET}")
    print(f"{RED_BOLD}   Powered by NVIDIA Texture Tools{RESET}")
    print(f"{RED_BOLD}{'='*70}{RESET}")

def find_files_from_dropped_items(items, extensions):
    """Finds all files from dropped items"""
    files = []
    nvtt_folder_name = "NVIDIA Texture Tools"
    
    for item in items:
        path = Path(item)
        if not path.exists():
            continue
        if path.name == nvtt_folder_name:
            continue
        if path.is_file():
            if path.suffix.lower() in extensions:
                files.append(path)
        elif path.is_dir():
            if path.name == nvtt_folder_name:
                continue
            for ext in extensions:
                for f in path.rglob(f"*{ext}"):
                    if nvtt_folder_name in str(f.parent):
                        continue
                    files.append(f)
                for f in path.rglob(f"*{ext.upper()}"):
                    if nvtt_folder_name in str(f.parent):
                        continue
                    files.append(f)
    
    return sorted(set(files))

def convert_png_to_dds(input_path, output_path, format_type):
    """Converts PNG to DDS"""
    formats = {"1": "bc1", "2": "bc2", "3": "bc3", "4": "bc4", "5": "bc5", "6": "bc7"}
    format_name = formats.get(format_type, "bc3")
    
    cmd = [str(NVTT_PATH), str(input_path), "--format", format_name, "--output", str(output_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except:
        return False

def convert_dds_to_png(input_path, output_path, keep_alpha=True):
    """Converts DDS to PNG"""
    format_type = "rgba8" if keep_alpha else "rgb8"
    cmd = [str(NVTT_PATH), str(input_path), "--format", format_type, "--output", str(output_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except:
        return False

def wait_for_exit():
    """Wait for Enter key before closing"""
    print(f"\n{RED_BOLD}Press Enter to exit...{RESET}", end='', flush=True)
    try:
        input()
    except:
        pass

# Global variables
NVTT_PATH = None
TEMP_DIR = None

def main():
    global NVTT_PATH, TEMP_DIR
    
    # Enable ANSI support
    if os.name == 'nt':
        os.system('')
    
    set_console_red_bold()
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header()
        
        # Extract or find NVIDIA Texture Tools
        print(f"\n{RED_BOLD}[INFO] Loading NVIDIA Texture Tools...{RESET}")
        NVTT_PATH = extract_nvtt_folder()
        
        if not NVTT_PATH or not NVTT_PATH.exists():
            print(f"\n{RED_BOLD}[ERROR] NVIDIA Texture Tools not found!{RESET}")
            print(f"\n{RED_BOLD}SOLUTION:{RESET}")
            print(f"{RED_BOLD}Make sure the 'NVIDIA Texture Tools' folder is included in the EXE{RESET}")
            print(f"{RED_BOLD}Use: pyinstaller --onefile --add-data 'NVIDIA Texture Tools;NVIDIA Texture Tools' --console script.py{RESET}")
            wait_for_exit()
            return
        
        print(f"{RED_BOLD}[OK] Ready!{RESET}")
        
        # Drag & Drop only
        if len(sys.argv) <= 1:
            print(f"\n{RED_BOLD}[INFO] How to use:{RESET}")
            print(f"\n{RED_BOLD}1. Drag and drop PNG or DDS files onto this EXE{RESET}")
            print(f"{RED_BOLD}2. Or drag and drop a FOLDER containing files{RESET}")
            print(f"{RED_BOLD}3. Select conversion options{RESET}")
            print(f"\n{RED_BOLD}Tip: You can drag multiple files/folders at once!{RESET}")
            wait_for_exit()
            return
        
        # Get dropped items
        items = sys.argv[1:]
        print(f"\n{RED_BOLD}Processing {len(items)} dropped item(s)...{RESET}")
        
        # Find PNG and DDS files
        png_files = find_files_from_dropped_items(items, ['.png'])
        dds_files = find_files_from_dropped_items(items, ['.dds'])
        
        # Choose mode
        if png_files and dds_files:
            print(f"\n{RED_BOLD}Found: {len(png_files)} PNG and {len(dds_files)} DDS files{RESET}")
            print(f"{RED_BOLD}1 - Convert PNG to DDS{RESET}")
            print(f"{RED_BOLD}2 - Convert DDS to PNG{RESET}")
            choice = input(f"\n{RED_BOLD}Choose (1-2): {RESET}").strip()
            if choice == "2":
                files = dds_files
                mode = "dds"
            else:
                files = png_files
                mode = "png"
        elif png_files:
            files = png_files
            mode = "png"
            print(f"\n{RED_BOLD}Found {len(png_files)} PNG file(s){RESET}")
        elif dds_files:
            files = dds_files
            mode = "dds"
            print(f"\n{RED_BOLD}Found {len(dds_files)} DDS file(s){RESET}")
        else:
            print(f"\n{RED_BOLD}[ERROR] No PNG or DDS files found!{RESET}")
            wait_for_exit()
            return
        
        # Show files
        print(f"\n{RED_BOLD}Files to process:{RESET}")
        for f in files[:15]:
            print(f"{RED_BOLD}  - {f.name}{RESET}")
        if len(files) > 15:
            print(f"{RED_BOLD}  ... and {len(files)-15} more{RESET}")
        
        # Process PNG to DDS
        if mode == "png":
            print(f"\n{RED_BOLD}Available formats:{RESET}")
            print(f"{RED_BOLD}1 - BC1 (DXT1) - No alpha (smallest){RESET}")
            print(f"{RED_BOLD}2 - BC2 (DXT3) - Sharp alpha{RESET}")
            print(f"{RED_BOLD}3 - BC3 (DXT5) - Smooth alpha (RECOMMENDED){RESET}")
            print(f"{RED_BOLD}4 - BC4 (ATI1) - Single channel{RESET}")
            print(f"{RED_BOLD}5 - BC5 (ATI2) - Two channel{RESET}")
            print(f"{RED_BOLD}6 - BC7 - High quality (DX11+){RESET}")
            
            fmt = input(f"\n{RED_BOLD}Select format (1-6) [Enter=3]: {RESET}").strip()
            if fmt == "": fmt = "3"
            
            confirm = input(f"\n{RED_BOLD}Start conversion? (y/n) [Enter=y]: {RESET}").lower()
            if confirm and confirm not in ['y', 'yes', '']:
                print(f"\n{RED_BOLD}Cancelled{RESET}")
                wait_for_exit()
                return
            
            print()
            success = 0
            for i, f in enumerate(files, 1):
                out = f.with_suffix('.dds')
                print(f"{RED_BOLD}[{i}/{len(files)}] {f.name}...{RESET}", end=" ", flush=True)
                if convert_png_to_dds(f, out, fmt):
                    if out.exists():
                        orig = f.stat().st_size
                        new = out.stat().st_size
                        ratio = orig / new if new > 0 else 0
                        print(f"{RED_BOLD}OK ({orig/1024:.1f}KB -> {new/1024:.1f}KB, {ratio:.1f}x){RESET}")
                    else:
                        print(f"{RED_BOLD}OK{RESET}")
                    success += 1
                else:
                    print(f"{RED_BOLD}FAILED{RESET}")
            print(f"\n{RED_BOLD}Done! {success}/{len(files)} successful{RESET}")
        
        # Process DDS to PNG
        else:
            keep = input(f"\n{RED_BOLD}Keep alpha channel? (y/n) [Enter=y]: {RESET}").lower()
            keep_alpha = keep not in ['n', 'no']
            
            confirm = input(f"\n{RED_BOLD}Start conversion? (y/n) [Enter=y]: {RESET}").lower()
            if confirm and confirm not in ['y', 'yes', '']:
                print(f"\n{RED_BOLD}Cancelled{RESET}")
                wait_for_exit()
                return
            
            print()
            success = 0
            for i, f in enumerate(files, 1):
                out = f.with_suffix('.png')
                print(f"{RED_BOLD}[{i}/{len(files)}] {f.name}...{RESET}", end=" ", flush=True)
                if convert_dds_to_png(f, out, keep_alpha):
                    if out.exists():
                        dds_size = f.stat().st_size
                        png_size = out.stat().st_size
                        print(f"{RED_BOLD}OK ({dds_size/1024:.1f}KB -> {png_size/1024:.1f}KB){RESET}")
                    else:
                        print(f"{RED_BOLD}OK{RESET}")
                    success += 1
                else:
                    print(f"{RED_BOLD}FAILED{RESET}")
            print(f"\n{RED_BOLD}Done! {success}/{len(files)} successful{RESET}")
        
        wait_for_exit()
        
    except KeyboardInterrupt:
        print(f"\n\n{RED_BOLD}[!] Cancelled by user. Goodbye!{RESET}")
        wait_for_exit()
    except Exception as e:
        print(f"\n{RED_BOLD}[ERROR] {e}{RESET}")
        wait_for_exit()
    finally:
        reset_console_color()
        cleanup()

if __name__ == "__main__":
    main()
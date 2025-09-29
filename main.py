#!/usr/bin/env python3
"""
画像ファイル名変更システム
メインアプリケーション

Mac環境で動作する、画像ファイル名の一括変更システム
フォルダ内の画像を順次表示し、各種情報を入力してファイル名を規則的に変更する

作成者: Python + Tkinter
バージョン: 1.0.0
対応形式: JPG, PNG, HEIC
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# パスの設定（相対インポートのため）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.main_window import MainWindow
except ImportError as e:
    print(f"モジュールのインポートに失敗しました: {e}")
    print("必要なライブラリがインストールされているか確認してください:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """必要なライブラリがインストールされているかチェック"""
    missing_packages = []
    
    try:
        import PIL
    except ImportError:
        missing_packages.append("Pillow")
    
    try:
        import openpyxl
    except ImportError:
        missing_packages.append("openpyxl")
    
    try:
        import pillow_heif
    except ImportError:
        missing_packages.append("pillow-heif")
    
    if missing_packages:
        error_msg = (
            f"以下のパッケージがインストールされていません:\\n"
            f"{', '.join(missing_packages)}\\n\\n"
            f"以下のコマンドでインストールしてください:\\n"
            f"pip install {' '.join(missing_packages)}"
        )
        print(error_msg)
        
        # Tkinterが使用可能な場合はGUIでエラー表示
        try:
            root = tk.Tk()
            root.withdraw()  # メインウィンドウを隠す
            messagebox.showerror("依存関係エラー", error_msg)
            root.destroy()
        except:
            pass
        
        return False
    
    return True


def main():
    """メイン関数"""
    print("画像ファイル名変更システムを起動しています...")
    
    # 依存関係チェック
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # メインアプリケーションを起動
        app = MainWindow()
        app.run()
        
    except Exception as e:
        error_msg = f"アプリケーションの起動に失敗しました:\\n{str(e)}"
        print(error_msg)
        
        # エラーダイアログを表示
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("起動エラー", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
ファイル操作モジュール
フォルダ選択、画像ファイル検出、ファイル名変更処理を行う
"""
import os
import re
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional
import shutil


class FileHandler:
    """ファイル操作処理を行うクラス"""
    
    # 対応する画像拡張子
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.heif'}
    
    # ファイル名禁止文字（Windows + Mac対応）
    FORBIDDEN_CHARS = r'[<>:"/\\|?*\x00-\x1f]'
    
    def _natural_sort_key(self, filepath: str):
        """自然順序ソート用のキー関数（数字を数値として認識）"""
        filename = Path(filepath).name
        # 数字部分を数値として、文字部分をそのまま返すリストを生成
        parts = []
        for part in re.split(r'(\d+)', filename):
            if part.isdigit():
                parts.append(int(part))
            else:
                parts.append(part.lower())  # 大文字小文字を統一
        return parts
    
    def __init__(self):
        self.image_folder: Optional[str] = None
        self.image_files: List[str] = []
        self.current_index: int = 0
    
    def select_folder(self) -> bool:
        """画像フォルダを選択し、画像ファイルを検出する"""
        folder_path = filedialog.askdirectory(
            title="画像フォルダを選択してください",
            initialdir=os.path.expanduser("~")
        )
        
        if not folder_path:
            return False
        
        self.image_folder = folder_path
        return self._scan_image_files()
    
    def _scan_image_files(self) -> bool:
        """フォルダ内の画像ファイルをスキャンする"""
        if not self.image_folder:
            return False
        
        try:
            image_files = []
            folder_path = Path(self.image_folder)
            
            # フォルダ内のすべてのファイルをチェック
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    extension = file_path.suffix.lower()
                    if extension in self.SUPPORTED_EXTENSIONS:
                        image_files.append(str(file_path))
            
            if not image_files:
                messagebox.showwarning("警告", "選択したフォルダに対応する画像ファイルが見つかりません。\\n"
                                               "対応形式: jpg, png, heic")
                return False
            
            # 自然順序ソート（数字を数値として認識）
            image_files.sort(key=self._natural_sort_key)
            print(f"デバッグ: 画像ファイルを自然順序でソート完了 ({len(image_files)}ファイル)")
            for i, file in enumerate(image_files[:5]):  # 最初の5ファイルを表示
                print(f"  {i+1}: {Path(file).name}")
            if len(image_files) > 5:
                print(f"  ... (他{len(image_files)-5}ファイル)")
            self.image_files = image_files
            self.current_index = 0
            
            messagebox.showinfo("完了", f"画像ファイルを{len(image_files)}件検出しました。")
            return True
            
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダの読み込みに失敗しました:\\n{str(e)}")
            return False
    
    def get_current_image_path(self) -> Optional[str]:
        """現在の画像ファイルパスを取得"""
        if not self.image_files or self.current_index >= len(self.image_files):
            return None
        return self.image_files[self.current_index]
    
    def get_current_image_info(self) -> tuple:
        """現在の画像情報を取得 (現在のインデックス, 総数)"""
        return (self.current_index + 1, len(self.image_files))
    
    def has_next_image(self) -> bool:
        """次の画像があるかチェック"""
        return self.current_index + 1 < len(self.image_files)
    
    def has_previous_image(self) -> bool:
        """前の画像があるかチェック"""
        return self.current_index > 0
    
    def next_image(self) -> bool:
        """次の画像に移動"""
        if self.has_next_image():
            self.current_index += 1
            return True
        return False
    
    def previous_image(self) -> bool:
        """前の画像に移動"""
        if self.has_previous_image():
            self.current_index -= 1
            return True
        return False
    
    def sanitize_filename(self, filename: str) -> str:
        """ファイル名から禁止文字を除去"""
        # 禁止文字を除去
        sanitized = re.sub(self.FORBIDDEN_CHARS, '', filename)
        
        # 連続するスペースを単一のスペースに変換
        sanitized = re.sub(r'\\s+', ' ', sanitized)
        
        # 前後の空白を削除
        sanitized = sanitized.strip()
        
        # 空文字列の場合は「untitled」を返す
        if not sanitized:
            sanitized = "untitled"
        
        return sanitized
    
    def generate_new_filename(self, part_name: str, weight: str, unit: str,
                            material_code: str, processing_code: str,
                            photo_type_code: str, has_notes: str, manual_number: str = "") -> str:
        """新しいファイル名を生成"""
        # 各パラメータをサニタイズ
        part_name = self.sanitize_filename(part_name)
        weight = self.sanitize_filename(weight)
        
        # 連番を取得（手動番号がある場合はそれを使用、なければ自動番号）
        if manual_number and manual_number.isdigit():
            number = int(manual_number)
        else:
            number = self.get_next_number()
        
        # ファイル名を組み立て（番号を先頭に追加）
        filename = f"{number}_{part_name}_{weight}_{unit}_{material_code}_{processing_code}_{photo_type_code}_{has_notes}"
        
        return filename
    
    def get_next_number(self) -> int:
        """フォルダ内の既存ファイルから次のペア番号を取得（1, 1, 2, 2, 3, 3...）"""
        if not self.image_folder:
            return 1
        
        folder_path = Path(self.image_folder)
        number_counts = {}  # 番号ごとのファイル数をカウント
        
        # 画像拡張子のリスト
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.tiff', '.bmp', '.gif'}
        
        # フォルダ内のすべての画像ファイルを調べる
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                # ファイル名から番号を抽出（最初のアンダースコアまでの部分）
                filename = file_path.stem
                parts = filename.split('_')
                
                # 最初の部分が数字の場合のみ処理（リネーム済みファイル）
                if parts and parts[0].isdigit():
                    number = int(parts[0])
                    number_counts[number] = number_counts.get(number, 0) + 1
        
        # ペア番号ロジック：1, 1, 2, 2, 3, 3...
        if not number_counts:
            return 1  # 最初のファイル
        
        max_number = max(number_counts.keys())
        
        # 最大番号のファイル数をチェック
        if number_counts[max_number] < 2:
            # 最大番号がまだ2個未満の場合、同じ番号を返す
            print(f"デバッグ: 番号 {max_number} は {number_counts[max_number]} 個存在、同じ番号 {max_number} を返す")
            return max_number
        else:
            # 最大番号が2個ある場合、次の番号を返す
            next_number = max_number + 1
            print(f"デバッグ: 番号 {max_number} は2個存在、次の番号 {next_number} を返す")
            return next_number
    
    def check_file_exists(self, new_filename: str, extension: str) -> bool:
        """指定されたファイル名が既に存在するかチェック"""
        if not self.image_folder:
            return False
        
        new_file_path = Path(self.image_folder) / f"{new_filename}{extension}"
        return new_file_path.exists()
    
    def rename_current_file(self, part_name: str, weight: str, unit: str,
                          material_code: str, processing_code: str,
                          photo_type_code: str, has_notes: str, manual_number: str = "") -> bool:
        """現在のファイルをリネーム"""
        current_path = self.get_current_image_path()
        if not current_path:
            return False
        
        try:
            current_file = Path(current_path)
            extension = current_file.suffix
            
            # 新しいファイル名を生成（手動番号を渡す）
            new_filename = self.generate_new_filename(
                part_name, weight, unit, material_code, processing_code, photo_type_code, has_notes, manual_number
            )
            
            # 重複チェック（連番があるため基本的に重複しないが念のため）
            if self.check_file_exists(new_filename, extension):
                current_filename = current_file.stem + extension
                new_full_filename = new_filename + extension
                
                # 現在のファイルと同じ名前でなければ警告
                if current_filename != new_full_filename:
                    messagebox.showwarning("警告", 
                                         f"同名のファイルが既に存在します。\\n"
                                         f"ファイル名: {new_full_filename}\\n"
                                         f"予期しない重複です。")
                    return False
            
            # リネーム実行
            new_path = current_file.parent / f"{new_filename}{extension}"
            current_file.rename(new_path)
            
            # リストを更新
            self.image_files[self.current_index] = str(new_path)
            
            return True
            
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルのリネームに失敗しました:\\n{str(e)}")
            return False
    
    def is_ready(self) -> bool:
        """画像ファイルが読み込まれているかチェック"""
        return bool(self.image_files)
    
    def get_total_files(self) -> int:
        """総ファイル数を取得"""
        return len(self.image_files)
    
    def is_last_file(self) -> bool:
        """最後のファイルかチェック"""
        return self.current_index == len(self.image_files) - 1
    
    def preview_filename(self, part_name: str, weight: str, unit: str,
                        material_code: str, processing_code: str,
                        photo_type_code: str, has_notes: str) -> str:
        """生成されるファイル名をプレビュー（拡張子付き）"""
        if not self.get_current_image_path():
            return ""
        
        current_path = Path(self.get_current_image_path())
        extension = current_path.suffix
        
        new_filename = self.generate_new_filename(
            part_name, weight, unit, material_code, processing_code, photo_type_code, has_notes
        )
        
        return f"{new_filename}{extension}"
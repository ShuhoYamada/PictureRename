"""
画像処理モジュール
HEIC対応を含む画像表示機能を提供
"""
from PIL import Image, ImageTk
import pillow_heif
from typing import Optional, Tuple
import tkinter as tk


class ImageProcessor:
    """画像処理を行うクラス"""
    
    def __init__(self):
        # HEIF/HEIC形式のサポートを有効化
        pillow_heif.register_heif_opener()
        self.max_width = 800
        self.max_height = 600
    
    def load_and_resize_image(self, image_path: str) -> Optional[ImageTk.PhotoImage]:
        """
        画像を読み込み、指定サイズに縮小してTkinter用の画像オブジェクトを返す
        アスペクト比は維持される
        """
        try:
            # 画像を開く
            with Image.open(image_path) as img:
                # RGBA形式の場合はRGBに変換（透明度を白で埋める）
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # リサイズ処理
                resized_img = self._resize_with_aspect_ratio(img)
                
                # Tkinter用のPhotoImageに変換
                return ImageTk.PhotoImage(resized_img)
                
        except Exception as e:
            print(f"画像の読み込みに失敗しました: {image_path}")
            print(f"エラー: {str(e)}")
            return None
    
    def _resize_with_aspect_ratio(self, image: Image.Image) -> Image.Image:
        """
        アスペクト比を維持しながら画像をリサイズ
        """
        original_width, original_height = image.size
        
        # アスペクト比を計算
        width_ratio = self.max_width / original_width
        height_ratio = self.max_height / original_height
        
        # 小さい方の比率を使用（画像が枠に収まるように）
        ratio = min(width_ratio, height_ratio)
        
        # リサイズが必要かチェック
        if ratio >= 1.0:
            # 元画像の方が小さい場合はそのまま返す
            return image
        
        # 新しいサイズを計算
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # リサイズ実行（高品質なリサンプリング使用）
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        画像の基本情報を取得
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'mode': img.mode,
                    'format': img.format,
                    'size_mb': self._get_file_size_mb(image_path)
                }
        except Exception as e:
            print(f"画像情報の取得に失敗しました: {image_path}")
            print(f"エラー: {str(e)}")
            return None
    
    def _get_file_size_mb(self, file_path: str) -> float:
        """ファイルサイズをMBで取得"""
        import os
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    
    def create_placeholder_image(self, width: int = 400, height: int = 300) -> ImageTk.PhotoImage:
        """
        画像が読み込めない場合のプレースホルダー画像を作成
        """
        try:
            # グレーの背景に「No Image」テキストを描画
            img = Image.new('RGB', (width, height), color='lightgray')
            
            # フォントは使用しないシンプルなバージョン
            # （PIL.ImageDrawは使わずにシンプルな画像のみ作成）
            
            return ImageTk.PhotoImage(img)
            
        except Exception:
            # 最終的なフォールバック：小さな白い画像
            fallback_img = Image.new('RGB', (100, 100), color='white')
            return ImageTk.PhotoImage(fallback_img)
    
    def set_max_size(self, width: int, height: int):
        """最大表示サイズを設定"""
        self.max_width = width
        self.max_height = height
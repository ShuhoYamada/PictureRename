"""
画像表示GUI
画像プレビュー、ナビゲーションボタン、進捗表示を提供
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from utils.image_processor import ImageProcessor


class ImageViewer:
    """画像表示パネルを管理するクラス"""
    
    def __init__(self, parent_frame: tk.Frame):
        self.parent_frame = parent_frame
        self.image_processor = ImageProcessor()
        
        # コールバック関数
        self.prev_callback: Optional[Callable] = None
        self.next_callback: Optional[Callable] = None
        
        # ウィジェットの参照
        self.image_label: Optional[tk.Label] = None
        self.progress_label: Optional[tk.Label] = None
        self.prev_button: Optional[tk.Button] = None
        self.next_button: Optional[tk.Button] = None
        self.filename_label: Optional[tk.Label] = None
        
        # 現在の画像オブジェクト（参照を保持するため）
        self.current_image = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """画像表示関連のウィジェットを作成"""
        # ヘッダー部分
        header_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # タイトル
        title_label = tk.Label(
            header_frame,
            text="🖼️ 画像プレビュー",
            font=("SF Pro Display", 16, "bold"),
            fg="#1f2937",
            bg="#ffffff"
        )
        title_label.pack(side="left")
        
        # 進捗表示
        self.progress_label = tk.Label(
            header_frame,
            text="0 / 0",
            font=("SF Pro Display", 12, "bold"),
            fg="#3b82f6",
            bg="#ffffff"
        )
        self.progress_label.pack(side="right")
        
        # 現在のファイル名表示
        self.filename_label = tk.Label(
            self.parent_frame,
            text="",
            font=("SF Pro Display", 10),
            fg="#6b7280",
            bg="#ffffff",
            wraplength=500
        )
        self.filename_label.pack(pady=(0, 15), padx=20)
        
        # 画像表示エリアのフレーム（カード風）
        image_frame = tk.Frame(
            self.parent_frame,
            bg="#f8fafc",
            relief="flat",
            bd=0
        )
        image_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # インナーフレーム（影付き）
        inner_frame = tk.Frame(
            image_frame,
            bg="#ffffff",
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightcolor="#e5e7eb",
            highlightbackground="#e5e7eb"
        )
        inner_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 画像表示ラベル
        self.image_label = tk.Label(
            inner_frame,
            text="🖼️\n画像を読み込んでください",
            bg="#ffffff",
            font=("SF Pro Display", 14),
            fg="#9ca3af"
        )
        self.image_label.pack(expand=True, fill="both", padx=15, pady=15)
        
        # ナビゲーションボタンのフレーム
        nav_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        nav_frame.pack(pady=20)
        
        # 前へボタン
        self.prev_button = tk.Button(
            nav_frame,
            text="⬅️ 前へ",
            font=("SF Pro Display", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.prev_button.pack(side="left", padx=15)
        
        # 次へボタン
        self.next_button = tk.Button(
            nav_frame,
            text="次へ ➡️",
            font=("SF Pro Display", 11, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.next_button.pack(side="right", padx=15)
    
    def set_navigation_callbacks(self, prev_callback: Callable, next_callback: Callable):
        """ナビゲーションボタンのコールバックを設定"""
        self.prev_callback = prev_callback
        self.next_callback = next_callback
        
        if self.prev_button:
            self.prev_button.configure(command=prev_callback)
        if self.next_button:
            self.next_button.configure(command=next_callback)
    
    def display_image(self, image_path: str):
        """画像を表示"""
        if not image_path:
            self._show_placeholder("画像パスが無効です")
            return
        
        # 画像を読み込み＆リサイズ
        photo_image = self.image_processor.load_and_resize_image(image_path)
        
        if photo_image:
            self.current_image = photo_image  # 参照を保持
            self.image_label.configure(
                image=photo_image,
                text="",
                compound="center"
            )
        else:
            self._show_placeholder("画像の読み込みに失敗しました")
        
        # ファイル名を表示
        import os
        filename = os.path.basename(image_path)
        self.filename_label.configure(text=filename)
    
    def _show_placeholder(self, message: str):
        """プレースホルダー表示"""
        placeholder_image = self.image_processor.create_placeholder_image()
        self.current_image = placeholder_image
        self.image_label.configure(
            image=placeholder_image,
            text=message,
            compound="center",
            font=("Arial", 12),
            fg="#666666"
        )
    
    def update_progress(self, current: int, total: int):
        """進捗表示を更新"""
        if self.progress_label:
            self.progress_label.configure(text=f"{current} / {total}")
    
    def update_navigation_buttons(self, has_prev: bool, has_next: bool):
        """ナビゲーションボタンの状態を更新"""
        if self.prev_button:
            state = "normal" if has_prev else "disabled"
            self.prev_button.configure(state=state)
        
        if self.next_button:
            state = "normal" if has_next else "disabled"
            self.next_button.configure(state=state)
    
    def clear_display(self):
        """表示をクリア"""
        self.current_image = None
        self.image_label.configure(
            image="",
            text="画像を読み込んでください",
            font=("Arial", 14),
            fg="#888888"
        )
        self.filename_label.configure(text="")
        self.progress_label.configure(text="0 / 0")
        self.update_navigation_buttons(False, False)
    
    def set_enabled(self, enabled: bool):
        """ナビゲーションボタンの有効/無効を設定"""
        state = "normal" if enabled else "disabled"
        
        if not enabled:
            # 無効化時は両方とも無効
            if self.prev_button:
                self.prev_button.configure(state="disabled")
            if self.next_button:
                self.next_button.configure(state="disabled")
        # 有効化時は実際の状態に応じて個別に設定されるため、ここでは何もしない
    
    def show_completion_message(self):
        """完了メッセージを表示"""
        self.image_label.configure(
            image="",
            text="すべての画像の処理が完了しました！\\n\\nお疲れさまでした。",
            font=("Arial", 16, "bold"),
            fg="#4CAF50"
        )
        self.filename_label.configure(text="")
        self.update_navigation_buttons(False, False)
"""
メインウィンドウGUI
アプリケーションのレイアウト構成とイベント処理を管理
"""
import tkinter as tk
from tkinter import messagebox, Menu
from gui.input_panel import InputPanel
from gui.image_viewer import ImageViewer
from utils.excel_reader import ExcelReader
from utils.file_handler import FileHandler


class MainWindow:
    """メインウィンドウを管理するクラス"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📸 Image Renamer Pro")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg="#f8fafc")
        
        # モダンなスタイル設定
        self.colors = {
            'primary': '#3b82f6',
            'secondary': '#10b981', 
            'accent': '#f59e0b',
            'danger': '#ef4444',
            'success': '#22c55e',
            'surface': '#ffffff',
            'background': '#f8fafc',
            'text_primary': '#1f2937',
            'text_secondary': '#6b7280',
            'border': '#e5e7eb'
        }
        
        # バックエンドクラスのインスタンス
        self.excel_reader = ExcelReader()
        self.file_handler = FileHandler()
        
        # GUIコンポーネント
        self.input_panel: InputPanel = None
        self.image_viewer: ImageViewer = None
        
        self._create_menu()
        self._create_layout()
        self._setup_callbacks()
        self._setup_keyboard_shortcuts()
    
    def _create_menu(self):
        """メニューバーを作成"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # ファイルメニュー
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="素材マスターを読み込み", command=self._load_materials)
        file_menu.add_command(label="加工方法マスターを読み込み", command=self._load_processing_methods)
        file_menu.add_separator()
        file_menu.add_command(label="画像フォルダを選択", command=self._select_image_folder)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        
        # ヘルプメニュー
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="使い方", command=self._show_help)
        help_menu.add_command(label="バージョン情報", command=self._show_about)
    
    def _create_layout(self):
        """レイアウトを作成"""
        # メインフレーム
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 上部のボタンフレーム（カード風デザイン）
        button_frame = tk.Frame(
            main_frame,
            bg=self.colors['surface'],
            relief="flat",
            bd=0
        )
        button_frame.pack(fill="x", pady=(0, 20), padx=5, ipady=15)
        
        # シャドウ効果のフレーム
        shadow_frame = tk.Frame(
            button_frame,
            bg="#e2e8f0",
            height=2
        )
        shadow_frame.pack(fill="x", side="bottom")
        
        # 素材マスター読み込みボタン
        self.materials_button = tk.Button(
            button_frame,
            text="📊 素材マスター読み込み",
            font=("Arial", 11, "bold"),
            bg="#3b82f6",
            fg="#1f2937",
            activebackground="#2563eb",
            activeforeground="#1f2937",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._load_materials
        )
        self.materials_button.pack(side="left", padx=(15, 10))
        
        # 加工方法マスター読み込みボタン
        self.processing_button = tk.Button(
            button_frame,
            text="⚙️ 加工方法マスター読み込み",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="#1f2937",
            activebackground="#d97706",
            activeforeground="#1f2937",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._load_processing_methods
        )
        self.processing_button.pack(side="left", padx=(0, 10))
        
        # 画像フォルダ選択ボタン
        self.folder_button = tk.Button(
            button_frame,
            text="📁 画像フォルダ選択",
            font=("Arial", 11, "bold"),
            bg="#10b981",
            fg="#1f2937",
            activebackground="#059669",
            activeforeground="#1f2937",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._select_image_folder
        )
        self.folder_button.pack(side="left", padx=(0, 10))
        
        # 状態表示ラベル
        status_container = tk.Frame(button_frame, bg=self.colors['surface'])
        status_container.pack(side="right", padx=(10, 15))
        
        self.status_icon = tk.Label(
            status_container,
            text="⏳",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#6b7280"
        )
        self.status_icon.pack(side="left", padx=(0, 8))
        
        self.status_label = tk.Label(
            status_container,
            text="素材マスターとフォルダを読み込んでください",
            font=("Arial", 11),
            fg="#6b7280",
            bg="#ffffff"
        )
        self.status_label.pack(side="left")
        
        # 左右分割のフレーム（カード風デザイン）
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True)
        
        # 左側：入力パネル（カード風）
        left_frame = tk.Frame(
            content_frame, 
            width=450, 
            bg=self.colors['surface'], 
            relief="flat",
            bd=0
        )
        left_frame.pack(side="left", fill="y", padx=(5, 10), pady=5)
        left_frame.pack_propagate(False)  # サイズ固定
        
        # 左フレームのシャドウ
        left_shadow = tk.Frame(left_frame, bg="#e2e8f0", height=2)
        left_shadow.pack(fill="x", side="bottom")
        
        # 右側：画像表示パネル（カード風）
        right_frame = tk.Frame(
            content_frame, 
            bg=self.colors['surface'], 
            relief="flat",
            bd=0
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=(0, 5), pady=5)
        
        # 右フレームのシャドウ
        right_shadow = tk.Frame(right_frame, bg="#e2e8f0", height=2)
        right_shadow.pack(fill="x", side="bottom")
        
        # 入力パネルの作成
        self.input_panel = InputPanel(left_frame)
        
        # 画像表示パネルの作成
        self.image_viewer = ImageViewer(right_frame)
        
        # 初期状態では入力パネルを無効化
        self.input_panel.set_enabled(False)
        self.image_viewer.set_enabled(False)
    
    def _setup_callbacks(self):
        """コールバック関数を設定"""
        # 入力検証コールバック
        self.input_panel.set_validation_callback(self._validate_inputs)
        
        # 適用ボタンコールバック
        self.input_panel.set_apply_button_callback(self._apply_and_next)
        
        # ナビゲーションコールバック
        self.image_viewer.set_navigation_callbacks(
            self._go_to_previous_image,
            self._go_to_next_image
        )
    
    def _setup_keyboard_shortcuts(self):
        """キーボードショートカットを設定"""
        self.root.bind('<Return>', self._on_enter_pressed)
        self.root.bind('<Left>', lambda e: self._go_to_previous_image())
        self.root.bind('<Right>', lambda e: self._go_to_next_image())
    
    def _load_materials(self):
        """素材マスターを読み込み"""
        if self.excel_reader.select_and_load_materials_file():
            self.input_panel.update_material_list(self.excel_reader.get_materials_list())
            self.materials_button.configure(
                bg="#22c55e", 
                text="✓ 素材マスター読み込み済み",
                activebackground="#16a34a",
                fg="#1f2937"
            )
            self._update_status_display()
            self._check_ready_state()
    
    def _load_processing_methods(self):
        """加工方法マスターを読み込み"""
        if self.excel_reader.select_and_load_processing_methods_file():
            self.input_panel.update_processing_list(self.excel_reader.get_processing_methods_list())
            self.processing_button.configure(
                bg="#22c55e",
                text="✓ 加工方法マスター読み込み済み",
                activebackground="#16a34a",
                fg="#1f2937"
            )
            self._update_status_display()
            self._check_ready_state()
    
    def _select_image_folder(self):
        """画像フォルダを選択"""
        if self.file_handler.select_folder():
            self.folder_button.configure(
                bg="#22c55e",
                text="✓ 画像フォルダ選択済み",
                activebackground="#16a34a",
                fg="#1f2937"
            )
            self._update_status_display()
            self._check_ready_state()
            if self._is_ready():
                self._load_first_image()
    
    def _check_ready_state(self):
        """準備完了状態をチェックし、UIを更新"""
        ready = self._is_ready()
        self.input_panel.set_enabled(ready)
        self.image_viewer.set_enabled(ready)
        
        if ready and not self._is_image_loaded():
            self._load_first_image()
        
        # 準備完了後、入力検証は少し遅延させて実行
        if ready:
            self.root.after(200, self._validate_inputs)
    
    def _is_ready(self) -> bool:
        """アプリケーションが使用可能な状態かチェック"""
        return (self.excel_reader.is_ready() and 
                self.file_handler.is_ready())
    
    def _is_image_loaded(self) -> bool:
        """画像が読み込まれているかチェック"""
        return self.file_handler.get_current_image_path() is not None
    
    def _load_first_image(self):
        """最初の画像を読み込み"""
        self._update_image_display()
        self._update_ui_state()
    
    def _update_image_display(self):
        """現在の画像を表示"""
        image_path = self.file_handler.get_current_image_path()
        if image_path:
            self.image_viewer.display_image(image_path)
            current, total = self.file_handler.get_current_image_info()
            self.image_viewer.update_progress(current, total)
    
    def _update_ui_state(self):
        """UI状態を更新"""
        if not self.file_handler.is_ready():
            return
        
        # ナビゲーションボタンの状態更新
        has_prev = self.file_handler.has_previous_image()
        has_next = self.file_handler.has_next_image()
        self.image_viewer.update_navigation_buttons(has_prev, has_next)
        
        # 入力検証
        self._validate_inputs()
    
    def _validate_inputs(self):
        """入力検証を実行"""
        if not self.input_panel:
            return
        
        is_valid = self.input_panel.is_all_filled()
        self.input_panel.set_apply_button_state(is_valid)
        
        # ハイライト処理は現在のフォーカス状態を考慮して実行
        focused_widget = self.root.focus_get()
        
        if not is_valid:
            # テキスト入力中でない場合のみハイライトを適用
            if (not focused_widget or 
                focused_widget not in [self.input_panel.part_name_entry, self.input_panel.weight_entry]):
                self.input_panel.highlight_empty_fields()
        else:
            self.input_panel.clear_highlight()
    
    def _apply_and_next(self):
        """現在の設定を適用して次の画像に進む"""
        if not self.input_panel.is_all_filled():
            messagebox.showwarning("警告", "すべての項目を入力してください。")
            return
        
        # 入力値を取得
        values = self.input_panel.get_input_values()
        
        # ID値を取得
        material_id = self.excel_reader.get_material_code(values['material'])
        processing_id = self.excel_reader.get_processing_method_code(values['processing'])
        photo_type_code = self.input_panel.get_photo_type_code()
        notes_code = self.input_panel.get_notes_code()
        
        if not material_id or not processing_id:
            messagebox.showerror("エラー", "素材または加工方法のIDが見つかりません。")
            return
        
        # ファイルリネーム実行
        success = self.file_handler.rename_current_file(
            values['part_name'],
            values['weight'],
            values['unit'],
            material_id,
            processing_id,
            photo_type_code,
            notes_code
        )
        
        if not success:
            return  # エラーメッセージは file_handler 内で表示済み
        
        # 次の画像に移動
        if self.file_handler.has_next_image():
            self.file_handler.next_image()
            self.input_panel.clear_text_inputs()  # 部品名と重量のみクリア
            self._update_image_display()
            self._update_ui_state()
        else:
            # 最後の画像の場合、完了メッセージを表示
            self._show_completion()
    
    def _go_to_previous_image(self):
        """前の画像に移動"""
        if self.file_handler.has_previous_image():
            self.file_handler.previous_image()
            self.input_panel.clear_text_inputs()
            self._update_image_display()
            self._update_ui_state()
    
    def _go_to_next_image(self):
        """次の画像に移動（リネームなし）"""
        if self.file_handler.has_next_image():
            self.file_handler.next_image()
            self.input_panel.clear_text_inputs()
            self._update_image_display()
            self._update_ui_state()
    
    def _on_enter_pressed(self, event):
        """Enterキーが押された時の処理"""
        if (self.input_panel and 
            self.input_panel.is_all_filled() and 
            self._is_ready()):
            self._apply_and_next()
    
    def _show_completion(self):
        """完了画面を表示"""
        total_files = self.file_handler.get_total_files()
        messagebox.showinfo("🎉 完了", 
                          f"すべての画像ファイルの処理が完了しました！\\n\\n"
                          f"✨ 処理済みファイル数: {total_files}件\\n\\n"
                          f"🎊 お疲れさまでした！")
        
        self.image_viewer.show_completion_message()
        self.input_panel.set_enabled(False)
    
    def _update_status_display(self):
        """状態表示を更新"""
        materials_loaded = bool(self.excel_reader.materials)
        processing_loaded = bool(self.excel_reader.processing_methods)
        folder_loaded = self.file_handler.is_ready()
        
        if materials_loaded and processing_loaded and folder_loaded:
            self.status_icon.configure(text="✅", fg="#22c55e")
            self.status_label.configure(
                text="準備完了！画像処理を開始できます",
                fg="#22c55e"
            )
        elif materials_loaded and processing_loaded:
            self.status_icon.configure(text="⚠️", fg="#f59e0b")
            self.status_label.configure(
                text="画像フォルダを選択してください",
                fg="#f59e0b"
            )
        elif materials_loaded or processing_loaded:
            self.status_icon.configure(text="📊", fg="#ef4444")
            missing = []
            if not processing_loaded:
                missing.append("加工方法マスター")
            if not materials_loaded:
                missing.append("素材マスター")
            self.status_label.configure(
                text=f"{', '.join(missing)}を読み込んでください",
                fg="#ef4444"
            )
        else:
            self.status_icon.configure(text="⏳", fg="#6b7280")
            self.status_label.configure(
                text="素材マスターと加工方法マスターを読み込んでください",
                fg="#6b7280"
            )
    
    def _show_help(self):
        """ヘルプダイアログを表示"""
        help_text = """🚀 Image Renamer Pro 使い方

✨ 初期設定:
   • 上部のボタンから素材マスター.xlsxを読み込み
   • 加工方法マスター.xlsxを読み込み
   • 画像フォルダを選択

📝 ファイル名変更:
   • 各項目に情報を入力
   • 「適用&次へ」ボタンをクリック
   • 次の画像に自動で移動

⌨️ キーボードショートカット:
   • Enter: 適用&次へ
   • ←→: 前の画像/次の画像へ移動

📋 ファイル名形式:
   部品名_重量_単位_素材ID_加工ID_写真区分_特記事項.拡張子
   
📷 写真区分:
   • 部品写真(P): 部品のみの写真
   • 素材込み(M): 素材情報込みの写真
"""
        messagebox.showinfo("📖 使い方", help_text)
    
    def _show_about(self):
        """バージョン情報を表示"""
        about_text = """📸 Image Renamer Pro

🎯 Version: 2.0.0
🛠️ Built with: Python + Tkinter

📁 対応形式: JPG, PNG, HEIC
💻 対応OS: macOS

✨ Modern UI Design
🚀 Fast & Efficient  
💎 Beautiful Results

© 2024 - Made with ❤️"""
        messagebox.showinfo("ℹ️ バージョン情報", about_text)
    
    def run(self):
        """アプリケーションを実行"""
        # 起動時のメッセージ
        messagebox.showinfo("🎉 ようこそ！", 
                          "Image Renamer Pro へようこそ！\\n\\n"
                          "🚀 以下の手順で始めましょう：\\n\\n"
                          "📊 1. 素材マスター.xlsxを読み込み\\n"
                          "⚙️ 2. 加工方法マスター.xlsxを読み込み\\n"
                          "📁 3. 画像フォルダを選択\\n\\n"
                          "✨ 簡単で美しいファイル名に変更できます！")
        
        self.root.mainloop()
"""
入力パネルGUI
部品名、重量、単位、素材、加工方法、特記事項の入力フォームを提供
"""
import tkinter as tk
from tkinter import ttk
import re
from typing import Dict, List, Optional, Callable


class InputPanel:
    """入力パネルを管理するクラス"""
    
    def __init__(self, parent_frame: tk.Frame):
        self.parent_frame = parent_frame
        self.validation_callback: Optional[Callable] = None
        self.excel_reader = None  # ExcelReaderインスタンスへの参照
        
        # 入力フィールドの変数
        self.part_name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="kg")  # デフォルト値
        self.material_category_var = tk.StringVar()  # 素材区分
        self.material_var = tk.StringVar()  # 素材名
        self.processing_var = tk.StringVar()
        self.photo_type_var = tk.StringVar(value="部品写真(P) - 部品のみの写真")  # デフォルト値
        self.notes_var = tk.StringVar(value="なし(0) - 特記事項なし")  # デフォルト値
        
        # ウィジェットの参照
        self.part_name_entry: Optional[tk.Entry] = None
        self.weight_entry: Optional[tk.Entry] = None
        self.unit_combo: Optional[ttk.Combobox] = None
        self.material_category_combo: Optional[ttk.Combobox] = None  # 素材区分
        self.material_combo: Optional[ttk.Combobox] = None  # 素材名
        self.processing_combo: Optional[ttk.Combobox] = None
        self.photo_type_combo: Optional[ttk.Combobox] = None
        self.notes_combo: Optional[ttk.Combobox] = None
        self.apply_button: Optional[tk.Button] = None
        
        # 半角英数字のみ許可する入力検証用
        self.weight_validation = parent_frame.register(self._validate_weight_input)
        
        self._create_widgets()
        self._setup_validation()
    
    def _create_input_section(self, title, description):
        """入力セクションのラベルを作成"""
        section_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        section_frame.pack(fill="x", padx=20, pady=(5, 0))
        
        tk.Label(
            section_frame,
            text=title,
            font=("SF Pro Display", 12, "bold"),
            fg="#374151",
            bg="#ffffff"
        ).pack(anchor="w")
        
        tk.Label(
            section_frame,
            text=description,
            font=("SF Pro Display", 9),
            fg="#6b7280",
            bg="#ffffff"
        ).pack(anchor="w")
    
    def _create_widgets(self):
        """入力フォームのウィジェットを作成"""
        # タイトル
        title_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            title_frame,
            text="📝 ファイル情報入力",
            font=("SF Pro Display", 16, "bold"),
            fg="#1f2937",
            bg="#ffffff"
        ).pack(anchor="w")
        
        # 部品名
        self._create_input_section(
            "🔧 部品名",
            "部品の名前を入力してください"
        )
        self.part_name_entry = tk.Entry(
            self.parent_frame, 
            textvariable=self.part_name_var,
            font=("SF Pro Display", 11),
            bg="#f9fafb",
            fg="#1f2937",
            relief="flat",
            bd=1,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb"
        )
        self.part_name_entry.pack(padx=20, pady=(5, 15), fill="x", ipady=8)
        
        # 重量
        self._create_input_section(
            "⚖️ 重量",
            "半角英数字で入力してください"
        )
        self.weight_entry = tk.Entry(
            self.parent_frame, 
            textvariable=self.weight_var,
            font=("SF Pro Display", 11),
            bg="#f9fafb",
            fg="#1f2937",
            relief="flat",
            bd=1,
            highlightthickness=2,
            highlightcolor="#3b82f6",
            highlightbackground="#e5e7eb",
            validate="key",
            validatecommand=(self.weight_validation, "%P")
        )
        self.weight_entry.pack(padx=20, pady=(5, 15), fill="x", ipady=8)
        
        # 単位
        self._create_input_section(
            "📎 単位",
            "重量の単位を選択してください"
        )
        # カスタムスタイルのttk.Combobox
        style = ttk.Style()
        style.configure(
            "Modern.TCombobox",
            fieldbackground="#f9fafb",
            background="#ffffff",
            borderwidth=1,
            relief="flat"
        )
        self.unit_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.unit_var,
            values=["kg", "g"],
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.unit_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=5)
        
        # 素材区分
        self._create_input_section(
            "🧩 素材区分 (必須)",
            "Excelマスターから素材区分を選択してください"
        )
        self.material_category_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.material_category_var,
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.material_category_combo.pack(padx=20, pady=(5, 10), fill="x", ipady=6)
        
        # 素材名
        self._create_input_section(
            "📦 素材名 (必須)",
            "素材区分を選択した後、素材名を選択してください"
        )
        self.material_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.material_var,
            font=("SF Pro Display", 11),
            state="disabled",  # 初期状態は非活性
            style="Modern.TCombobox"
        )
        self.material_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=6)
        
        # 加工方法
        self._create_input_section(
            "⚙️ 加工方法 (必須)",
            "Excelマスターから加工方法を選択してください"
        )
        self.processing_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.processing_var,
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.processing_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=6)
        
        # 写真区分
        self._create_input_section(
            "📷 写真区分 (必須)",
            "撮影した写真の種類を選択してください - P: 部品のみ / M: 素材も含む"
        )
        self.photo_type_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.photo_type_var,
            values=["部品写真(P) - 部品のみの写真", "素材込み(M) - 素材も含む写真"],
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox",
            width=40
        )
        self.photo_type_combo.pack(padx=20, pady=(5, 20), fill="x", ipady=8)
        
        # 特記事項の有無
        self._create_input_section(
            "📝 特記事項 (必須)",
            "この部品に特記事項があるかどうかを選択してください"
        )
        self.notes_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.notes_var,
            values=["なし(0) - 特記事項なし", "ある(1) - 特記事項あり"],
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox",
            width=40
        )
        self.notes_combo.pack(padx=20, pady=(5, 20), fill="x", ipady=8)
        
        # 適用&次へボタン
        button_frame = tk.Frame(self.parent_frame, bg="#ffffff")
        button_frame.pack(fill="x", padx=20, pady=30)
        
        self.apply_button = tk.Button(
            button_frame,
            text="✨ 適用 & 次へ",
            font=("SF Pro Display", 13, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            state="disabled"
        )
        self.apply_button.pack(fill="x", ipady=5)
    
    def _validate_weight_input(self, value: str) -> bool:
        """重量入力の検証（半角英数字のみ許可）"""
        if value == "":
            return True
        # 半角英数字、小数点、ハイフンのみ許可
        return bool(re.match(r'^[0-9a-zA-Z.-]*$', value))
    
    def _setup_validation(self):
        """入力検証とボタン状態の設定"""
        def on_input_change(*args):
            if self.validation_callback:
                # 入力変更時の検証は少し遅延させて、連続する変更を安定化
                self.parent_frame.after(100, self.validation_callback)
        
        # 各変数の変更を監視
        self.part_name_var.trace('w', on_input_change)
        self.weight_var.trace('w', on_input_change)
        self.unit_var.trace('w', on_input_change)
        self.material_category_var.trace('w', self._on_material_category_change)
        self.material_var.trace('w', on_input_change)
        self.processing_var.trace('w', on_input_change)
        self.photo_type_var.trace('w', on_input_change)
        self.notes_var.trace('w', on_input_change)
    
    def set_validation_callback(self, callback: Callable):
        """入力検証コールバックを設定"""
        self.validation_callback = callback
    
    def set_apply_button_callback(self, callback: Callable):
        """適用ボタンのコールバックを設定"""
        if self.apply_button:
            self.apply_button.configure(command=callback)
    
    def set_excel_reader(self, excel_reader):
        """ExcelReaderインスタンスを設定"""
        self.excel_reader = excel_reader
    
    def set_scroll_callback(self, callback):
        """スクロールコールバックを設定"""
        self.scroll_callback = callback
        
        # 各入力フィールドにフォーカスイベントを設定
        if hasattr(self, 'part_name_entry') and self.part_name_entry:
            self.part_name_entry.bind('<FocusIn>', lambda e: self._scroll_to_widget(e.widget))
        if hasattr(self, 'weight_entry') and self.weight_entry:
            self.weight_entry.bind('<FocusIn>', lambda e: self._scroll_to_widget(e.widget))
    
    def _scroll_to_widget(self, widget):
        """指定されたウィジェットが見える位置にスクロール"""
        if hasattr(self, 'scroll_callback') and self.scroll_callback:
            self.scroll_callback(widget)
    
    def _on_material_category_change(self, *args):
        """素材区分が変更された時の処理"""
        if not self.excel_reader:
            return
            
        selected_category = self.material_category_var.get()
        
        if selected_category:
            # 選択された区分の素材名リストを取得
            materials = self.excel_reader.get_materials_by_category(selected_category)
            
            # 素材名ドロップダウンを更新して活性化
            if self.material_combo:
                self.material_combo['values'] = materials
                self.material_combo['state'] = 'readonly'
                self.material_var.set("")  # 現在の選択をクリア
                
                # バリデーションコールバックがあれば呼び出し
                if self.validation_callback:
                    self.validation_callback()
        else:
            # 素材区分が未選択の場合、素材名を非活性に
            if self.material_combo:
                self.material_combo['values'] = []
                self.material_combo['state'] = 'disabled'
                self.material_var.set("")
                
                # バリデーションコールバックがあれば呼び出し
                if self.validation_callback:
                    self.validation_callback()
    
    def update_material_categories_list(self, categories: List[str]):
        """素材区分リストを更新"""
        if self.material_category_combo:
            self.material_category_combo['values'] = categories
            if categories and not self.material_category_var.get():
                # デフォルト選択はしない（空のまま）
                pass
    
    def update_material_list(self, materials: List[str]):
        """素材リストを更新（互換性のため保持）"""
        if self.material_combo:
            self.material_combo['values'] = materials
            if materials and not self.material_var.get():
                # デフォルト選択はしない（空のまま）
                pass
    
    def update_processing_list(self, processing_methods: List[str]):
        """加工方法リストを更新"""
        if self.processing_combo:
            self.processing_combo['values'] = processing_methods
            if processing_methods and not self.processing_var.get():
                # デフォルト選択はしない（空のまま）
                pass
    
    def clear_text_inputs(self):
        """テキスト入力項目をクリア（部品名と重量のみ）- 現在は保持するため何もしない"""
        # 部品名と重量は保持するためクリアしない
        # self.part_name_var.set("")
        # self.weight_var.set("")
        pass
    
    def set_focus_to_part_name(self):
        """部品名フィールドにフォーカスを設定"""
        if self.part_name_entry and self.part_name_entry['state'] == 'normal':
            self.parent_frame.after(50, lambda: self.part_name_entry.focus_set())
    
    def force_clear_text_inputs(self):
        """部品名と重量を強制的にクリア（明示的にクリアしたい場合用）"""
        self.part_name_var.set("")
        self.weight_var.set("")
        self.set_focus_to_part_name()
    
    def get_input_values(self) -> Dict[str, str]:
        """現在の入力値を取得"""
        return {
            'part_name': self.part_name_var.get().strip(),
            'weight': self.weight_var.get().strip(),
            'unit': self.unit_var.get(),
            'material_category': self.material_category_var.get(),
            'material': self.material_var.get(),
            'processing': self.processing_var.get(),
            'photo_type': self.photo_type_var.get(),
            'notes': self.notes_var.get()
        }
    
    def get_material_id(self) -> Optional[str]:
        """選択された素材名から素材IDを取得"""
        if self.excel_reader and self.material_var.get():
            return self.excel_reader.get_material_id_by_name(self.material_var.get())
        return None
    
    def get_photo_type_code(self) -> str:
        """写真区分からコードを取得"""
        photo_type_value = self.photo_type_var.get()
        if "部品写真(P)" in photo_type_value:
            return "P"
        elif "素材込み(M)" in photo_type_value:
            return "M"
        else:
            return "P"  # デフォルト
    
    def get_notes_code(self) -> str:
        """特記事項の有無からコードを取得"""
        notes_value = self.notes_var.get()
        if "ある(1)" in notes_value:
            return "1"
        else:
            return "0"
    
    def is_all_filled(self) -> bool:
        """すべての項目が入力されているかチェック"""
        values = self.get_input_values()
        return (
            bool(values['part_name']) and
            bool(values['weight']) and
            bool(values['unit']) and
            bool(values['material_category']) and
            bool(values['material']) and
            bool(values['processing']) and
            bool(values['photo_type']) and
            bool(values['notes'])
        )
    
    def set_apply_button_state(self, enabled: bool):
        """適用ボタンの状態を設定"""
        if self.apply_button:
            state = "normal" if enabled else "disabled"
            self.apply_button.configure(state=state)
    
    def highlight_empty_fields(self):
        """未入力フィールドをハイライト"""
        values = self.get_input_values()
        
        # 部品名
        if not values['part_name']:
            self.part_name_entry.configure(bg="#fef2f2")
        else:
            self.part_name_entry.configure(bg="#f9fafb")
        
        # 重量
        if not values['weight']:
            self.weight_entry.configure(bg="#fef2f2")
        else:
            self.weight_entry.configure(bg="#f9fafb")
        
        # コンボボックスのハイライトは視覚的な変更のみ（フォーカス移動を避ける）
        # フォーカス設定は削除してテキストボックスの入力を妨げないようにする
    
    def clear_highlight(self):
        """ハイライトをクリア"""
        if self.part_name_entry:
            self.part_name_entry.configure(bg="#f9fafb")
        if self.weight_entry:
            self.weight_entry.configure(bg="#f9fafb")
    
    def set_enabled(self, enabled: bool):
        """全フィールドの有効/無効を設定"""
        state = "normal" if enabled else "disabled"
        readonly_state = "readonly" if enabled else "disabled"
        
        if self.part_name_entry:
            self.part_name_entry.configure(state=state)
        if self.weight_entry:
            self.weight_entry.configure(state=state)
        if self.unit_combo:
            self.unit_combo.configure(state=readonly_state)
        if self.material_category_combo:
            self.material_category_combo.configure(state=readonly_state)
        if self.material_combo:
            # 素材名は素材区分が選択されている場合のみ有効
            if enabled and self.material_category_var.get():
                self.material_combo.configure(state="readonly")
            else:
                self.material_combo.configure(state="disabled")
        if self.processing_combo:
            self.processing_combo.configure(state=readonly_state)
        if self.photo_type_combo:
            self.photo_type_combo.configure(state=readonly_state)
        if self.notes_combo:
            self.notes_combo.configure(state=readonly_state)
        
        # 有効化された時は部品名フィールドにフォーカスを設定
        if enabled and self.part_name_entry:
            # 少し遅延させてフォーカスを確実に設定
            self.parent_frame.after(100, lambda: self.part_name_entry.focus_set())
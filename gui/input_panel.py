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
        
        # 入力フィールドの変数
        self.part_name_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="kg")  # デフォルト値
        self.material_var = tk.StringVar()
        self.processing_var = tk.StringVar()
        self.notes_var = tk.StringVar(value="なし(0)")  # デフォルト値
        
        # ウィジェットの参照
        self.part_name_entry: Optional[tk.Entry] = None
        self.weight_entry: Optional[tk.Entry] = None
        self.unit_combo: Optional[ttk.Combobox] = None
        self.material_combo: Optional[ttk.Combobox] = None
        self.processing_combo: Optional[ttk.Combobox] = None
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
        
        # 素材
        self._create_input_section(
            "🧩 素材",
            "Excelマスターから素材を選択してください"
        )
        self.material_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.material_var,
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.material_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=5)
        
        # 加工方法
        self._create_input_section(
            "⚙️ 加工方法",
            "Excelマスターから加工方法を選択してください"
        )
        self.processing_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.processing_var,
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.processing_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=5)
        
        # 特記事項の有無
        self._create_input_section(
            "📝 特記事項",
            "特記事項の有無を選択してください"
        )
        self.notes_combo = ttk.Combobox(
            self.parent_frame,
            textvariable=self.notes_var,
            values=["なし(0)", "ある(1)"],
            font=("SF Pro Display", 11),
            state="readonly",
            style="Modern.TCombobox"
        )
        self.notes_combo.pack(padx=20, pady=(5, 15), fill="x", ipady=5)
        
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
                self.validation_callback()
        
        # 各変数の変更を監視
        self.part_name_var.trace('w', on_input_change)
        self.weight_var.trace('w', on_input_change)
        self.unit_var.trace('w', on_input_change)
        self.material_var.trace('w', on_input_change)
        self.processing_var.trace('w', on_input_change)
        self.notes_var.trace('w', on_input_change)
    
    def set_validation_callback(self, callback: Callable):
        """入力検証コールバックを設定"""
        self.validation_callback = callback
    
    def set_apply_button_callback(self, callback: Callable):
        """適用ボタンのコールバックを設定"""
        if self.apply_button:
            self.apply_button.configure(command=callback)
    
    def update_material_list(self, materials: List[str]):
        """素材リストを更新"""
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
        """テキスト入力項目をクリア（部品名と重量のみ）"""
        self.part_name_var.set("")
        self.weight_var.set("")
    
    def get_input_values(self) -> Dict[str, str]:
        """現在の入力値を取得"""
        return {
            'part_name': self.part_name_var.get().strip(),
            'weight': self.weight_var.get().strip(),
            'unit': self.unit_var.get(),
            'material': self.material_var.get(),
            'processing': self.processing_var.get(),
            'notes': self.notes_var.get()
        }
    
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
            bool(values['material']) and
            bool(values['processing']) and
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
            self.part_name_entry.configure(bg="#ffcccc")
        else:
            self.part_name_entry.configure(bg="white")
        
        # 重量
        if not values['weight']:
            self.weight_entry.configure(bg="#ffcccc")
        else:
            self.weight_entry.configure(bg="white")
        
        # コンボボックスは背景色変更が困難なため、フォーカス設定で対応
        if not values['material']:
            self.material_combo.focus_set()
        elif not values['processing']:
            self.processing_combo.focus_set()
    
    def clear_highlight(self):
        """ハイライトをクリア"""
        if self.part_name_entry:
            self.part_name_entry.configure(bg="white")
        if self.weight_entry:
            self.weight_entry.configure(bg="white")
    
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
        if self.material_combo:
            self.material_combo.configure(state=readonly_state)
        if self.processing_combo:
            self.processing_combo.configure(state=readonly_state)
        if self.notes_combo:
            self.notes_combo.configure(state=readonly_state)
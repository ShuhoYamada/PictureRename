"""
Excel読み込みモジュール
素材マスター.xlsxと加工方法マスター.xlsxからデータを読み込む
"""
import openpyxl
from tkinter import filedialog, messagebox
from typing import Dict, List, Tuple, Optional
import os


class ExcelReader:
    """Excel読み込み処理を行うクラス"""
    
    def __init__(self):
        self.materials: Dict[str, str] = {}  # 表示名 -> 素材ID
        self.processing_methods: Dict[str, str] = {}  # 表示名 -> 加工ID
        self.materials_data: Dict[str, Dict[str, str]] = {}  # 素材IDの詳細データ
        self.processing_methods_data: Dict[str, Dict[str, str]] = {}  # 加工IDの詳細データ
    
    def select_and_load_materials_file(self) -> bool:
        """素材マスターファイルを選択し、読み込む"""
        file_path = filedialog.askopenfilename(
            title="素材マスター.xlsxを選択してください",
            filetypes=[("Excel files", "*.xlsx")],
            initialdir=os.path.expanduser("~")
        )
        
        if not file_path:
            return False
        
        return self._load_materials_file(file_path)
    
    def select_and_load_processing_methods_file(self) -> bool:
        """加工方法マスターファイルを選択し、読み込む"""
        file_path = filedialog.askopenfilename(
            title="加工方法マスター.xlsxを選択してください",
            filetypes=[("Excel files", "*.xlsx")],
            initialdir=os.path.expanduser("~")
        )
        
        if not file_path:
            return False
        
        return self._load_processing_methods_file(file_path)
    
    def _load_materials_file(self, file_path: str) -> bool:
        """素材マスターファイルを読み込む"""
        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet = workbook.active
            
            materials = {}  # display_name -> material_id のマッピング
            self.materials_data = {}  # material_id -> {name, description} の詳細データ
            
            # ヘッダー行をスキップして2行目から読み込み
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] and row[2]:  # A列（素材名）、C列（素材ID）ともに値がある場合
                    material_name = str(row[0]).strip()
                    material_description = str(row[1]).strip() if row[1] else ""
                    material_id = str(row[2]).strip()
                    
                    if material_name and material_id:
                        # ドロップダウン表示用の文字列を作成
                        if material_description:
                            display_name = f"{material_name} - {material_description}"
                        else:
                            display_name = material_name
                        
                        materials[display_name] = material_id
                        self.materials_data[material_id] = {
                            'name': material_name,
                            'description': material_description
                        }
            
            if not materials:
                messagebox.showerror("エラー", "素材マスターファイルにデータが見つかりません。")
                return False
            
            self.materials = materials
            messagebox.showinfo("完了", f"素材マスターを読み込みました。({len(materials)}件)")
            return True
            
        except Exception as e:
            messagebox.showerror("エラー", f"素材マスターファイルの読み込みに失敗しました:\\n{str(e)}")
            return False
    
    def _load_processing_methods_file(self, file_path: str) -> bool:
        """加工方法マスターファイルを読み込む"""
        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet = workbook.active
            
            processing_methods = {}  # display_name -> processing_id のマッピング
            self.processing_methods_data = {}  # processing_id -> {name, description} の詳細データ
            
            # ヘッダー行をスキップして2行目から読み込み
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] and row[2]:  # A列（加工方法）、C列（加工ID）ともに値がある場合
                    method_name = str(row[0]).strip()
                    method_description = str(row[1]).strip() if row[1] else ""
                    method_id = str(row[2]).strip()
                    
                    if method_name and method_id:
                        # ドロップダウン表示用の文字列を作成
                        if method_description:
                            display_name = f"{method_name} - {method_description}"
                        else:
                            display_name = method_name
                        
                        processing_methods[display_name] = method_id
                        self.processing_methods_data[method_id] = {
                            'name': method_name,
                            'description': method_description
                        }
            
            if not processing_methods:
                messagebox.showerror("エラー", "加工方法マスターファイルにデータが見つかりません。")
                return False
            
            self.processing_methods = processing_methods
            messagebox.showinfo("完了", f"加工方法マスターを読み込みました。({len(processing_methods)}件)")
            return True
            
        except Exception as e:
            messagebox.showerror("エラー", f"加工方法マスターファイルの読み込みに失敗しました:\\n{str(e)}")
            return False
    
    def get_materials_list(self) -> List[str]:
        """素材名のリストを取得"""
        return list(self.materials.keys())
    
    def get_processing_methods_list(self) -> List[str]:
        """加工方法名のリストを取得"""
        return list(self.processing_methods.keys())
    
    def get_material_code(self, display_name: str) -> Optional[str]:
        """表示名から素材IDを取得"""
        return self.materials.get(display_name)
    
    def get_processing_method_code(self, display_name: str) -> Optional[str]:
        """表示名から加工IDを取得"""
        return self.processing_methods.get(display_name)
    
    def get_material_details(self, material_id: str) -> Optional[Dict[str, str]]:
        """素材IDから詳細情報を取得"""
        return self.materials_data.get(material_id)
    
    def get_processing_method_details(self, method_id: str) -> Optional[Dict[str, str]]:
        """加工IDから詳細情報を取得"""
        return self.processing_methods_data.get(method_id)
    
    def is_ready(self) -> bool:
        """両方のマスターファイルが読み込まれているかチェック"""
        return bool(self.materials) and bool(self.processing_methods)
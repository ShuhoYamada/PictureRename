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
        self.materials: Dict[str, str] = {}  # 素材名 -> 素材コード
        self.processing_methods: Dict[str, str] = {}  # 加工方法名 -> 加工方法コード
    
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
            
            materials = {}
            
            # ヘッダー行をスキップして2行目から読み込み
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] and row[1]:  # A列、B列ともに値がある場合
                    material_name = str(row[0]).strip()
                    material_code = str(row[1]).strip()
                    if material_name and material_code:
                        materials[material_name] = material_code
            
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
            
            processing_methods = {}
            
            # ヘッダー行をスキップして2行目から読み込み
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] and row[1]:  # A列、B列ともに値がある場合
                    method_name = str(row[0]).strip()
                    method_code = str(row[1]).strip()
                    if method_name and method_code:
                        processing_methods[method_name] = method_code
            
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
    
    def get_material_code(self, material_name: str) -> Optional[str]:
        """素材名から素材コードを取得"""
        return self.materials.get(material_name)
    
    def get_processing_method_code(self, method_name: str) -> Optional[str]:
        """加工方法名から加工方法コードを取得"""
        return self.processing_methods.get(method_name)
    
    def is_ready(self) -> bool:
        """両方のマスターファイルが読み込まれているかチェック"""
        return bool(self.materials) and bool(self.processing_methods)
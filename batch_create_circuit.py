# -*- coding: utf-8 -*-
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
import System.Windows.Forms as WinForms
import System.Drawing as Drawing
from System.Drawing import Size, Point
import os

try:
    import ScriptEnv
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    oDesktop.RestoreWindow()
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.GetActiveEditor()
    oModelManager = oProject.GetDefinitionManager().GetManager("Model")
except:
    pass  # 供非 AEDT 環境下測試介面用


class NetlistBatchRunner(WinForms.Form):
    def __init__(self):
        self.Text = "AEDT 全自動 S參數模擬與報告匯出系統"
        self.Size = Size(500, 450)
        
        self.file_list = []
        
        # 定義全域微軟正黑體字型
        font_default = Drawing.Font("Microsoft JhengHei", 9)
        font_bold = Drawing.Font("Microsoft JhengHei", 10, Drawing.FontStyle.Bold)
        font_btn = Drawing.Font("Microsoft JhengHei", 9, Drawing.FontStyle.Bold)
        
        self.Font = font_default
        
        # ==================================
        # Left Panel (Target Model Setup)
        # ==================================
        lbl_head_1 = WinForms.Label()
        lbl_head_1.Text = "【步驟一】鎖定要替換的 S參數模型"
        lbl_head_1.Location = Point(20, 20)
        lbl_head_1.AutoSize = True
        lbl_head_1.Font = font_bold
        self.Controls.Add(lbl_head_1)

        lbl_desc_1 = WinForms.Label()
        lbl_desc_1.Text = "請輸入您在原電路中所使用的模型名稱\n(請參考您在 AEDT 中的命名，填入此處)："
        lbl_desc_1.Location = Point(20, 50)
        lbl_desc_1.AutoSize = True
        self.Controls.Add(lbl_desc_1)
        
        lbl_model = WinForms.Label()
        lbl_model.Text = "模型名稱:"
        lbl_model.Location = Point(20, 100)
        lbl_model.AutoSize = True
        self.Controls.Add(lbl_model)
        
        self.txt_model = WinForms.TextBox()
        self.txt_model.Text = ""
        self.txt_model.Location = Point(90, 97)
        self.txt_model.Size = Size(100, 25)
        self.Controls.Add(self.txt_model)

        # ==================================
        # Right/Bottom Panel (S-parameter Files)
        # ==================================
        lbl_head_2 = WinForms.Label()
        lbl_head_2.Text = "【步驟二】加入要獨立跑分析的 S參數檔"
        lbl_head_2.Location = Point(20, 150)
        lbl_head_2.AutoSize = True
        lbl_head_2.Font = font_bold
        self.Controls.Add(lbl_head_2)
        
        self.listbox = WinForms.ListBox()
        self.listbox.Location = Point(20, 180)
        self.listbox.Size = Size(440, 130)
        self.Controls.Add(self.listbox)
        
        btn_add = WinForms.Button()
        btn_add.Text = "+ 新增 S參數檔"
        btn_add.Location = Point(20, 330)
        btn_add.Size = Size(120, 35)
        btn_add.Click += self.OnAddClick
        self.Controls.Add(btn_add)
        
        btn_clear = WinForms.Button()
        btn_clear.Text = "清空清單"
        btn_clear.Location = Point(150, 330)
        btn_clear.Size = Size(80, 35)
        btn_clear.Click += self.OnClearClick
        self.Controls.Add(btn_clear)
        
        # ==================================
        # Run Button
        # ==================================
        btn_run = WinForms.Button()
        btn_run.Text = "▶ 開始自動模擬與匯出！"
        btn_run.Location = Point(240, 330)
        btn_run.Size = Size(220, 35)
        btn_run.BackColor = Drawing.Color.LightSkyBlue
        btn_run.Font = font_btn
        btn_run.Click += self.OnRunClick
        self.Controls.Add(btn_run)

    def OnAddClick(self, sender, args):
        dialog = WinForms.OpenFileDialog()
        dialog.Multiselect = True
        dialog.Filter = "Touchstone Files (*.s*p)|*.s*p|All Files (*.*)|*.*"
        if dialog.ShowDialog() == WinForms.DialogResult.OK:
            for filepath in dialog.FileNames:
                if filepath not in self.file_list:
                    self.file_list.append(filepath)
                    self.listbox.Items.Add(os.path.basename(filepath))

    def OnClearClick(self, sender, args):
        self.file_list = []
        self.listbox.Items.Clear()

    def OnRunClick(self, sender, args):
        model_name = self.txt_model.Text.strip()
        if not model_name:
            WinForms.MessageBox.Show("請填寫要替換的模型名稱 (例如 S1)！", "錯誤")
            return
            
        if len(self.file_list) == 0:
            WinForms.MessageBox.Show("請先加入至少一個新 S 參數檔案！", "錯誤")
            return
            
        # 開始執行！
        self.Hide() 
        RunNetlistBatch(model_name, self.file_list)
        self.Close()

def generate_html_report(save_dir, project_name, report_data):
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AEDT Batch Summary Report</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7fa; color: #333; margin: 0; padding: 30px; }
        h1 { text-align: center; color: #0055a4; margin-bottom: 5px; font-size: 2.5rem; }
        .sub-title { text-align: center; color: #666; margin-bottom: 40px; }
        .card { background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 40px; padding: 25px; border-top: 5px solid #0055a4; }
        .header { display: flex; align-items: center; padding-bottom: 15px; margin-bottom: 20px; border-bottom: 1px solid #eee; }
        .header h2 { margin: 0; color: #0f172a; font-size: 1.8rem; }
        .badge { background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 20px; font-weight: bold; margin-right: 15px; }
        .img-container { display: flex; flex-wrap: wrap; gap: 25px; }
        .img-box { flex: 1 1 calc(50% - 25px); min-width: 300px; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .img-box img { width: 100%; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .img-title { font-weight: bold; margin-bottom: 10px; text-align: center; color: #475569; font-size: 1.1rem; }
    </style>
</head>
<body>
    <h1>Automated Simulation Summary</h1>
    <div class="sub-title">Project: <b>""" + project_name + """</b></div>"""

    for item in report_data:
        html += """
    <div class="card">
        <div class="header">
            <span class="badge">S-Parameter</span>
            <h2>""" + item['name'] + """</h2>
        </div>
        <div class="img-container">"""
        
        if item.get('schematic_img'):
            html += """
            <div class="img-box">
                <div class="img-title">Circuit Schematic Snapshot</div>
                <img src=\"""" + item['schematic_img'] + """\" alt="Schematic">
            </div>"""
            
        for chart in item['charts']:
            # Pretty title for the chart
            chart_title = chart.replace(".jpg","").replace(item['name'] + "_", "").replace("_", " ")
            html += """
            <div class="img-box">
                <div class="img-title">""" + chart_title + """</div>
                <img src=\"""" + chart + """\" alt="Result">
            </div>"""
            
        html += """
        </div>
    </div>"""
    
    html += """
</body>
</html>"""
    
    import codecs
    with codecs.open(os.path.join(save_dir, "Summary_Report.html"), "w", "utf-8") as f:
        f.write(html)


def RunNetlistBatch(target_model_name, file_paths):
    global oProject, oDesign, oEditor, oModelManager
    
    project_path = oProject.GetPath()
    project_name = oProject.GetName()
    save_dir = os.path.join(project_path, project_name + "_BatchResults")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    oModule_report = oDesign.GetModule("ReportSetup")
    all_reports = []
    try:
        all_reports = oModule_report.GetAllReportNames()
    except:
        pass
        
    report_data_list = []
    
    for i, filepath in enumerate(file_paths):
        # 取檔名做為這次報告的辨識名 (例如: S2)
        base_filename = os.path.basename(filepath)
        filename_no_ext = os.path.splitext(base_filename)[0]
        
        # 1. 直接修改全域 Model，取代成新的 S-parameter 路徑
        oModelManager.EditWithComps(target_model_name, 
            [
                "NAME:" + target_model_name,
                "Name:="		, target_model_name,
                "ModTime:="		, 0,
                "Library:="		, "",
                "LibLocation:="		, "Project",
                "ModelType:="		, "nport",
                "Description:="		, "",
                "ImageFile:="		, "",
                "SymbolPinConfiguration:=", 0,
                ["NAME:PortInfoBlk"],
                ["NAME:PortOrderBlk"],
                "filename:="		, filepath,
                "numberofports:="	, 2,  # 預設 2-port
                "sssfilename:="		, "", # 強制清空 cached sss，確保重新解析新的 s2p
                "sssmodel:="		, False,
                "PortNames:="		, ["Port1","Port2"],
                "domain:="		, "frequency",
                "datamode:="		, "Link",
                "devicename:="		, "",
                "SolutionName:="	, "",
                "displayformat:="	, "MagnitudePhase",
                "datatype:="		, "SMatrix",
                [
                    "NAME:DesignerCustomization",
                    "DCOption:="		, 0,
                    "InterpOption:="	, 0,
                    "ExtrapOption:="	, 1,
                    "Convolution:="		, 0,
                    "Passivity:="		, 0,
                    "Reciprocal:="		, False,
                    "ModelOption:="		, "",
                    "DataType:="		, 1
                ],
                [
                    "NAME:NexximCustomization",
                    "DCOption:="		, 3,
                    "InterpOption:="	, 1,
                    "ExtrapOption:="	, 3,
                    "Convolution:="		, 0,
                    "Passivity:="		, 0,
                    "Reciprocal:="		, False,
                    "ModelOption:="		, "",
                    "DataType:="		, 2
                ],
                [
                    "NAME:HSpiceCustomization",
                    "DCOption:="		, 1,
                    "InterpOption:="	, 2,
                    "ExtrapOption:="	, 3,
                    "Convolution:="		, 0,
                    "Passivity:="		, 0,
                    "Reciprocal:="		, False,
                    "ModelOption:="		, "",
                    "DataType:="		, 3
                ],
                "NoiseModelOption:="	, "External"
            ], [])
            
        # 2. 直接執行模擬 (NexximTransient，如果有其他 Setup 可以自行調整)
        try:
            oDesign.Analyze("NexximTransient")
        except:
            # 嘗試執行全部
            oDesign.AnalyzeAll()
            
        # 2.5. 截圖最新的電路圖 (Schematic Snapshot)
        schematic_img_filename = filename_no_ext + "_Schematic.jpg"
        schematic_img_path = os.path.join(save_dir, schematic_img_filename)
        try:
            if oEditor:
                oEditor.ExportImageToFile(schematic_img_path, 1920, 1080)
        except:
            pass
            
        # 3. 匯出報告
        chart_imgs = []
        if all_reports and len(all_reports) > 0:
            for report in all_reports:
                report_clean = report.replace(" ", "_")
                csv_path = os.path.join(save_dir, filename_no_ext + "_" + report_clean + ".csv")
                
                img_filename = filename_no_ext + "_" + report_clean + ".jpg"
                img_path = os.path.join(save_dir, img_filename)
                
                try:
                    oModule_report.ExportToFile(report, csv_path, False)
                    oModule_report.ExportImageToFile(report, img_path, 1920, 1080)
                    chart_imgs.append(img_filename)
                except Exception as e:
                    pass
                    
        # 記錄此次成果以供應 HTML 生成器
        sch_img_to_add = schematic_img_filename if os.path.exists(schematic_img_path) else None
        report_data_list.append({
            'name': filename_no_ext,
            'schematic_img': sch_img_to_add,
            'charts': chart_imgs
        })

    # ==========================
    # 產出最終 HTML 總結報告
    # ==========================
    generate_html_report(save_dir, project_name, report_data_list)

    WinForms.MessageBox.Show("批次模擬與匯出成功！\\n產生的報表與 Summary_Report.html 請至專案資料夾下的 BatchResults 尋找。", "完成")


if __name__ == '__main__':
    # 確認是否在 AEDT 環境執行
    try:
        tmp = oDesktop
    except NameError:
        print("請在 AEDT 內部執行此腳本。")
        
    form = NetlistBatchRunner()
    WinForms.Application.Run(form)

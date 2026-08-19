# AEDT Circuit S 參數自動化批次工具

用於在 AEDT Circuit 中批次建立電路、替換 S 參數模型，並執行自動化模擬與報告匯出。

## 主要功能

- 批次載入 S2P／S4P 檔案。
- 自動替換 AEDT Circuit 中的 S 參數模型。
- 建立或更新電路分析設定。
- 執行批次模擬與報告輸出。

## 使用環境

- Ansys Electronics Desktop（含 Circuit）
- AEDT IronPython Script 環境
- Windows

## 使用方式

1. 開啟 AEDT Circuit 專案。
2. 選擇 `Automation > Run Script...`。
3. 載入 `batch_create_circuit.py`。
4. 依操作介面選取 S 參數檔案並設定輸出選項。

## 公開內容

- `batch_create_circuit.py`：AEDT 自動化腳本。
- `Operation_Manual.html`：完整操作手冊。
- `S1.s2p`～`S5.s2p`、`SD1.s4p`～`SD3.s4p`：範例 S 參數資料。
- `Example_video.mp4`：操作示範影片。

---

本 Repository 為 Jeff Hong 個人技術作品集之公開展示內容，非 Taiwan Auto-Design Co.（TADC，虎門科技）官方帳號，亦非 Ansys, Inc. 官方合作項目；Ansys、HFSS、SIwave 為 Ansys, Inc. 之商標。原始碼與內容僅供技術展示，未經授權不得商業使用、散布或製作衍生作品，詳見 [LICENSE](LICENSE)。如需授權或合作，請洽 jeff.hong@cadmen.com。

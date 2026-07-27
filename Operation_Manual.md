# AEDT Circuit 自動化批次引擎操作說明

此工具由虎門科技資深技術工程師 Jeff Hong 洪敬傑提供

## 工具用途

本工具用於在 AEDT Circuit 中批次替換 S 參數模型，並執行自動化模擬與結果匯出。

## 使用環境

- Ansys Electronics Desktop（含 Circuit）
- AEDT IronPython Script 環境
- Windows

## 操作步驟

### 1. 開啟 AEDT Circuit 專案

先開啟 AEDT，載入要執行分析的 Circuit 專案與設計。

### 2. 執行腳本

1. 在 AEDT 選擇 `Automation > Run Script...`。
2. 選取 `batch_create_circuit.py`。
3. 等待工具控制面板開啟。

### 3. 選取 S 參數模型

在工具介面中選取要加入或替換的 S2P／S4P 檔案，例如：

- `S1.s2p`～`S5.s2p`
- `SD1.s4p`～`SD3.s4p`

### 4. 設定與執行

依序確認模型、輸出位置與分析設定，接著執行批次建立、替換與模擬流程。

### 5. 檢查結果

請確認 AEDT Circuit 的模型連結、模擬狀態與報告輸出結果。執行前建議先備份原始專案。

## 範例檔案

Repository 提供 S2P／S4P 範例資料與操作示範影片，可用於測試工具流程。

## 注意事項

- S 參數檔案格式需符合 AEDT Circuit 可讀取的格式。
- 請使用與專案相容的 AEDT 版本。
- 批次模擬前請確認輸出資料夾具有寫入權限。
- 請勿直接以客戶機密資料進行公開展示。

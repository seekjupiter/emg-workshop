# 「肌」不可失｜EMG 肌電訊號工作坊

**肌電訊號、電腦視覺與智慧醫療科技應用**  
北一女中專題講座｜2026 年 11 月 16 日  
講者：許絜翔 博士｜國立虎尾科技大學 機械設計工程系

這個專案提供工作坊使用的 **EMG 互動教材、ESP32-C3 程式、Python 即時波形顯示工具與安裝說明**。本次實作以 **Grove EMG Detector → Seeed XIAO ESP32-C3 → USB → Python** 為主，不需要先學會 Git 或命令列。

## 📚 課程資源

- 🌐 [EMG 互動式教材（免安裝，直接開啟）](https://seekjupiter.github.io/emg-interactive/)
- 📑 [工作坊投影片 PDF](slides/EMG_workshop.pdf)
- 🛠️ [ESP32 / Arduino IDE 安裝與燒錄教學](docs/ESP32_Setup_Guide.md)

> 如果上述 PDF 或安裝教學連結尚未開啟，表示對應檔案還沒上傳至此 Repository。

## 🚀 課前準備（Windows）

1. 安裝 [Arduino IDE 2.x](https://www.arduino.cc/en/software)。
2. 依照 [ESP32 安裝教學](docs/ESP32_Setup_Guide.md) 安裝 **ESP32 by Espressif Systems** 開發板套件，並選擇 **XIAO_ESP32C3**。
3. 安裝 [Python 3.11 或 3.12](https://www.python.org/downloads/)；Windows 安裝時可勾選 **Add Python to PATH**。
4. 在本頁按 **Code → Download ZIP**，解壓縮整個專案。
5. 在解壓縮後的資料夾中，雙擊 **`00_Install.bat`** 安裝 Python 套件，等待出現安裝完成訊息。

本專案提供的**更新版** `00_Install.bat` 會建立 `.venv` 虛擬環境，避免影響電腦上其他 Python 專案。首次安裝需要網路；之後啟動通常不需要重新安裝。

## 🔌 硬體與接線

本次使用 **Seeed XIAO ESP32-C3 + Grove 擴充板 + Grove EMG Detector**。

| Grove EMG | XIAO ESP32-C3 / 擴充板 |
|---|---|
| OUT | A0（GPIO2） |
| VCC | 3V3 |
| GND | GND |
| NC | 不使用 |

請確認擴充板的 A0 接孔與供電標示，避免把訊號線接到其他腳位。

## ▶️ 課堂實作：從電極到即時波形

1. 用 Arduino IDE 開啟 **`esp32_emg_500hz.ino`**，選擇 `XIAO_ESP32C3` 與正確的 COM Port，將程式上傳至開發板。
2. 確認 Arduino 序列監控視窗有數值輸出：`timestamp_us,voltage_mV`（例如 `2000,1532`），**鮑率 230400**。
3. **關閉 Arduino Serial Monitor / Serial Plotter**，避免 COM Port 被占用。
4. 依課程示範貼附三個電極並確認接線。
5. 雙擊 **`01_Start_EMG_Demo.bat`**；選擇正確 COM Port，按 **連線**。
6. 放鬆時按 **重設基準**，再進行維持收縮、反覆收縮，觀察三組波形。
7. 如需儲存資料，可按 **開始記錄 CSV**。

**Python 畫面顯示：** 模組輸出電壓（V）、扣除基準後的相對電壓（mV）、整流與平滑後的活動指標（mV）。

> ESP32 程式的**目標取樣率為 500 Hz**，實際速率可能受到 ADC 與序列傳輸影響。Grove 模組輸出已經過訊號調理，Python 的活動指標不等於未處理原始 sEMG 的研究級包絡線。

## 🧰 常見問題

| 情況 | 先檢查 |
|---|---|
| Arduino IDE 找不到 XIAO ESP32-C3 | 是否已安裝 **ESP32 by Espressif Systems**；參考安裝教學 |
| 找不到 COM Port | USB 線是否支援資料傳輸、Windows 是否辨識開發板、是否需要驅動 |
| Arduino 上傳失敗 | 開發板型號、COM Port、USB 連線；依安裝教學排除 |
| Python 顯示缺少套件 | 重新執行 `00_Install.bat`，確認安裝成功 |
| Python 無法連線 | 關閉 Arduino Serial Monitor / Plotter；確認選擇正確 COM Port |
| 波形沒有明顯變化 | 檢查電極接觸、Grove 供電與 OUT→A0 接線，重新設定基準 |

## 📁 專案檔案

```text
emg-interactive/
├── index.html                 # 線上互動教材（GitHub Pages）
├── README.md                  # 本說明
├── 00_Install.bat             # Windows：建立 venv、安裝 Python 套件
├── 01_Start_EMG_Demo.bat      # Windows：啟動即時繪圖
├── requirements.txt           # Python 套件需求
├── emg_viewer.py              # 即時 EMG 波形顯示與 CSV 記錄
├── esp32_emg_500hz.ino        # ESP32-C3 類比輸入與 USB 序列輸出
├── .gitignore                 # 排除 .venv 與本機資料
├── docs/
│   └── ESP32_Setup_Guide.md  # Arduino IDE / ESP32 安裝教學
└── slides/
    └── EMG_workshop.pdf       # 課程投影片
```

> Arduino IDE 若要求建立與 `.ino` 同名的資料夾，請選擇允許；不影響程式內容。

## 📌 補充說明

本專案用於**教學示範與訊號觀察**，並非醫療診斷系統。請勿將不同人的模組輸出電壓直接視為可比較的肌力數值。

**講者聯絡方式：** mde-chhsu@nfu.edu.tw  
**作者：** CHHsu @ NFU MDE

如需引用或修改教材，請保留適當來源說明；正式授權條款以本專案後續發布的 LICENSE 文件為準。

# ESP32-C3 安裝與燒錄教學（Windows）

本教學搭配 **Seeed XIAO ESP32-C3、Grove EMG Detector** 與工作坊提供的 `esp32_emg_500hz.ino`。請在課前完成步驟 1–4；課堂上再接上 EMG 模組量測。

## 1. 安裝 Arduino IDE

1. 開啟 [Arduino IDE 官方下載頁](https://www.arduino.cc/en/software)。
2. 下載並安裝 **Arduino IDE 2.x（Windows）**。
3. 安裝完成後開啟 Arduino IDE。

## 2. 安裝 ESP32 開發板套件

1. 在 Arduino IDE 開啟 **File → Preferences**（檔案 → 偏好設定）。
2. 找到 **Additional Boards Manager URLs**（其他開發板管理員網址），加入：

   ```text
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```
   for SAMD21
   ```text
   https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
   ```
   若原本已有其他網址，請保留，使用右側編輯按鈕另起一行加入。
3. 開啟左側 **Boards Manager**（開發板管理員），搜尋 `esp32`。
4. 安裝 **esp32 by Espressif Systems**。第一次安裝需要網路，可能花幾分鐘。

官方參考：[Espressif Arduino-ESP32 安裝說明](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)。

## 3. 連接 XIAO ESP32-C3 並選擇板型

1. 使用可傳輸資料的 USB-C 線，將 XIAO ESP32-C3 接上 Windows 電腦。
2. 在 Arduino IDE 選擇 **Tools → Board → esp32 → XIAO_ESP32C3**（名稱可能因套件版本略有差異）。
3. 選擇 **Tools → Port → COMx**，選擇剛接上開發板後出現的埠號。
4. 若看不到 COM Port，先換一條確定能傳資料的 USB 線、換 USB 插孔，並查看 Windows **裝置管理員 → 連接埠 (COM 和 LPT)**。部分開發板／USB 轉序列裝置可能需要對應驅動，應先確認裝置型號再安裝，**不要隨意下載驅動程式**。

Seeed 參考：[XIAO ESP32C3 入門](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)。

## 4. 燒錄課程程式

1. 開啟課程提供的 `esp32_emg_500hz.ino`。若 Arduino IDE 提示建立同名資料夾，選擇確認。
2. 確認板型為 **XIAO_ESP32C3**、COM Port 正確。
3. 按左上角 **Upload（上傳，向右箭頭）**，等待出現上傳完成訊息。
4. 打開 **Tools → Serial Monitor**，將傳輸速率設為 **230400 baud**。
5. 正常情況下會持續看到兩個以逗號分隔的數字，例如：

   ```text
   2000,1532
   4000,1531
   6000,1535
   ```

   第一欄是時間戳記（微秒），第二欄是 A0 的量測電壓（mV）。**即使尚未接 EMG，A0 懸空也可能顯示變動數值；此步只確認程式有輸出，不代表感測器量測成功。**
6. **關閉 Serial Monitor／Serial Plotter**，避免占用 COM Port，讓 Python 程式無法連線。

> 本程式設定目標取樣頻率為 500 Hz（每 2 ms 一筆），實際取樣率可能受 ADC 與傳輸影響。

## 5. 課堂上的 Grove EMG 接線與 Python 啟動

| Grove EMG Detector | XIAO ESP32-C3／Grove Shield |
|---|---|
| OUT | A0（GPIO2） |
| VCC | 3V3 |
| GND | GND |
| NC | 不接 |

請確認實際使用的 Grove Shield 腳位標示與供電配置。完成接線後：

1. 第一次使用先執行 `00_Install.bat` 安裝 Python 套件（需已安裝 Python 並連網）。
2. 接上開發板，雙擊 `01_Start_EMG_Demo.bat`。
3. 在程式中選擇 COM Port，按「連線」。
4. 放鬆時按「重設基準」，再觀察肌肉收縮時的三組波形。

注意：上述 BAT 檔案、`requirements.txt` 和 `emg_viewer.py` 必須放在同一資料夾。下載 GitHub 專案 ZIP 後請先完整解壓縮，不要直接在壓縮檔中執行。

## 常見問題

| 問題 | 建議處理 |
|---|---|
| Boards Manager 搜尋不到 ESP32 | 檢查網址是否完整、網路是否正常，重新啟動 IDE |
| 找不到 XIAO_ESP32C3 | 確認已安裝 `esp32 by Espressif Systems`，並重新開啟板型清單 |
| 沒有 COM Port | 換可傳資料 USB 線／USB 埠，檢查 Windows 裝置管理員 |
| 上傳失敗或無法連線 | 確認板型和 COM Port；關閉占用序列埠的程式；必要時依 Seeed 官方說明進入 bootloader 模式 |
| Serial Monitor 顯示亂碼 | 設定為 230400 baud |
| Python 顯示 COM Port 無法開啟 | 關閉 Arduino Serial Monitor／Plotter，確認沒有其他程式占用 |
| Python 缺少套件 | 先執行 `00_Install.bat`，確認 Python 安裝與網路正常 |

**課前完成標準：** Arduino IDE 能辨識 XIAO ESP32-C3、成功上傳 `.ino`，且 Serial Monitor 能看到 `timestamp_us,voltage_mV` 兩欄數字。EMG 貼片與波形量測留待課堂實作。

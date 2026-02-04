# Marquee TTS EXE

這個小工具會在螢幕上方顯示全寬跑馬燈，並同步使用 TTS 播報內容。提供 GUI 製作器可調整語速、播報次數與間隔。

## 安裝依賴

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## 直接執行

```bash
python app.py "指定內容"
```

GUI 製作器（可產生綁定指定訊息/設定的 EXE）：

```bash
python app.py --gui
```

GUI 內可輸出 `marquee_tts_build.py`，並選擇是否立即執行 PyInstaller 打包。若不立即打包，可在 Windows 手動執行：

```bash
pyinstaller --onefile --noconsole --name MarqueeTTS marquee_tts_build.py
```

常用參數（預設跑馬燈 2 次後自動關閉）：

```bash
python app.py "指定內容" \
  --speed 5 \
  --font-size 40 \
  --bg "#000000" \
  --fg "#ffffff" \
  --tts-rate 190 \
  --tts-repeat 2 \
  --tts-interval-minutes 1 \
  --loops 2
```

## 產生 EXE (Windows)

請在 Windows 上執行（注意是 `pip install pyinstaller`，不是 `pip install -r PyInstaller`）：

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name MarqueeTTS app.py
```

產出檔案位置：`dist/MarqueeTTS.exe`

## 結束程式

按 `Alt+F4` 或在工作列結束程式。
```

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

GUI 內可直接把圖形化設定輸出成應用程式（EXE）。預設會立即執行 PyInstaller 打包；若取消勾選，也會先輸出 `marquee_tts_build.py`：

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

## 把 `python app.py --gui` 變成 EXE

如果你要的是「雙擊就直接開 GUI 製作器」，建議打包 `gui_launcher.py`：

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name MarqueeTTS_GUI gui_launcher.py
```

產生後執行：`dist/MarqueeTTS_GUI.exe`（Windows 會顯示為 `dist\MarqueeTTS_GUI.exe`）。

如果你是打包 `app.py`，也可以在執行 EXE 時加參數：

```bash
MarqueeTTS.exe --gui
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

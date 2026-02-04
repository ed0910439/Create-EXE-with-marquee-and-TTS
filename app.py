import argparse
import threading
import subprocess
import time
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser

import pyttsx3


class MarqueeTTSApp:
    def __init__(
        self,
        message: str,
        speed: int,
        font_size: int,
        bg: str,
        fg: str,
        tts_rate: int,
        tts_repeat: int,
        tts_interval_seconds: float,
        loops: int,
    ):
        self.message = message
        self.speed = speed
        self.font_size = font_size
        self.bg = bg
        self.fg = fg
        self.tts_rate = tts_rate
        self.tts_repeat = tts_repeat
        self.tts_interval_seconds = tts_interval_seconds
        self.loops = loops
        self.completed_loops = 0
        self.root = tk.Tk()
        self.root.configure(bg=self.bg)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.screen_width = self.root.winfo_screenwidth()
        self.height = self.font_size + 20
        self.root.geometry(f"{self.screen_width}x{self.height}+0+0")
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.height, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.text_id = self.canvas.create_text(
            self.screen_width,
            self.height // 2,
            text=self.message,
            fill=self.fg,
            font=("Arial", self.font_size, "bold"),
            anchor="w",
        )
        self.text_width = self.canvas.bbox(self.text_id)[2] - self.canvas.bbox(self.text_id)[0]
        self.x_pos = self.screen_width
        self._start_tts()
        self._animate()

    def _start_tts(self) -> None:
        def run_tts() -> None:
            if self.tts_repeat <= 0:
                return
            engine = pyttsx3.init()
            engine.setProperty("rate", self.tts_rate)
            for index in range(self.tts_repeat):
                engine.say(self.message)
                engine.runAndWait()
                if index < self.tts_repeat - 1 and self.tts_interval_seconds > 0:
                    time.sleep(self.tts_interval_seconds)

        tts_thread = threading.Thread(target=run_tts, daemon=True)
        tts_thread.start()

    def _animate(self) -> None:
        self.x_pos -= self.speed
        if self.x_pos < -self.text_width:
            self.completed_loops += 1
            if self.completed_loops >= self.loops:
                self.root.destroy()
                return
            self.x_pos = self.screen_width
        self.canvas.coords(self.text_id, self.x_pos, self.height // 2)
        self.root.after(20, self._animate)

    def run(self) -> None:
        self.root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Top-screen marquee with TTS announcement.")
    parser.add_argument("message", nargs="?", default="系統公告：請注意補貨。")
    parser.add_argument("--speed", type=int, default=4, help="Marquee speed (pixels per tick).")
    parser.add_argument("--font-size", type=int, default=36, help="Font size in pixels.")
    parser.add_argument("--bg", default="#000000", help="Background color.")
    parser.add_argument("--fg", default="#ffffff", help="Text color.")
    parser.add_argument("--tts-rate", type=int, default=190, help="TTS speech rate.")
    parser.add_argument("--tts-repeat", type=int, default=1, help="Number of TTS repeats.")
    parser.add_argument(
        "--tts-interval-minutes",
        type=float,
        default=0,
        help="Minutes to wait between TTS repeats.",
    )
    parser.add_argument("--loops", type=int, default=2, help="Number of marquee loops before auto-exit.")
    parser.add_argument("--gui", action="store_true", help="Open the GUI builder instead of running immediately.")
    return parser.parse_args()


def build_script_content(
    message: str,
    speed: int,
    font_size: int,
    bg: str,
    fg: str,
    tts_rate: int,
    tts_repeat: int,
    tts_interval_minutes: float,
    loops: int,
) -> str:
    return f"""import threading
import time
import tkinter as tk

import pyttsx3


class MarqueeTTSApp:
    def __init__(
        self,
        message: str,
        speed: int,
        font_size: int,
        bg: str,
        fg: str,
        tts_rate: int,
        tts_repeat: int,
        tts_interval_seconds: float,
        loops: int,
    ):
        self.message = message
        self.speed = speed
        self.font_size = font_size
        self.bg = bg
        self.fg = fg
        self.tts_rate = tts_rate
        self.tts_repeat = tts_repeat
        self.tts_interval_seconds = tts_interval_seconds
        self.loops = loops
        self.completed_loops = 0
        self.root = tk.Tk()
        self.root.configure(bg=self.bg)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.screen_width = self.root.winfo_screenwidth()
        self.height = self.font_size + 20
        self.root.geometry(f"{{self.screen_width}}x{{self.height}}+0+0")
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.height, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.text_id = self.canvas.create_text(
            self.screen_width,
            self.height // 2,
            text=self.message,
            fill=self.fg,
            font=("Arial", self.font_size, "bold"),
            anchor="w",
        )
        self.text_width = self.canvas.bbox(self.text_id)[2] - self.canvas.bbox(self.text_id)[0]
        self.x_pos = self.screen_width
        self._start_tts()
        self._animate()

    def _start_tts(self) -> None:
        def run_tts() -> None:
            if self.tts_repeat <= 0:
                return
            engine = pyttsx3.init()
            engine.setProperty("rate", self.tts_rate)
            for index in range(self.tts_repeat):
                engine.say(self.message)
                engine.runAndWait()
                if index < self.tts_repeat - 1 and self.tts_interval_seconds > 0:
                    time.sleep(self.tts_interval_seconds)

        tts_thread = threading.Thread(target=run_tts, daemon=True)
        tts_thread.start()

    def _animate(self) -> None:
        self.x_pos -= self.speed
        if self.x_pos < -self.text_width:
            self.completed_loops += 1
            if self.completed_loops >= self.loops:
                self.root.destroy()
                return
            self.x_pos = self.screen_width
        self.canvas.coords(self.text_id, self.x_pos, self.height // 2)
        self.root.after(20, self._animate)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = MarqueeTTSApp(
        message={message!r},
        speed={speed},
        font_size={font_size},
        bg={bg!r},
        fg={fg!r},
        tts_rate={tts_rate},
        tts_repeat={tts_repeat},
        tts_interval_seconds={tts_interval_minutes} * 60,
        loops={loops},
    )
    app.run()


if __name__ == "__main__":
    main()
"""


def launch_gui() -> None:
    root = tk.Tk()
    root.title("Marquee TTS EXE 製作器")
    root.geometry("560x620")

    message_var = tk.StringVar(value="前日拾獲的手機放在右邊的抽屜零錢盤的下方！")
    speed_var = tk.StringVar(value="4")
    font_size_var = tk.StringVar(value="36")
    bg_var = tk.StringVar(value="#000000")
    fg_var = tk.StringVar(value="#ffffff")
    tts_rate_var = tk.StringVar(value="190")
    tts_repeat_var = tk.StringVar(value="1")
    tts_interval_var = tk.StringVar(value="0")
    loops_var = tk.StringVar(value="2")
    output_dir_var = tk.StringVar(value=str(Path.cwd()))
    exe_name_var = tk.StringVar(value="MarqueeTTS")
    build_now_var = tk.BooleanVar(value=False)

    fields = [
        ("公告內容", message_var),
        ("跑馬燈速度 (px/tick)", speed_var),
        ("字體大小", font_size_var),
        ("背景色", bg_var),
        ("文字色", fg_var),
        ("TTS 語速", tts_rate_var),
        ("TTS 播報次數", tts_repeat_var),
        ("TTS 間隔分鐘", tts_interval_var),
        ("跑馬燈重複次數", loops_var),
        ("輸出資料夾", output_dir_var),
        ("EXE 檔名", exe_name_var),
    ]

    def pick_color(target: tk.StringVar) -> None:
        chosen, hex_color = colorchooser.askcolor(color=target.get(), parent=root)
        if hex_color:
            target.set(hex_color)

    for row, (label, var) in enumerate(fields):
        tk.Label(root, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=12, pady=6)
        entry = tk.Entry(root, textvariable=var, width=30)
        entry.grid(row=row, column=1, padx=8, pady=6, sticky="w")
        if label in ("背景色", "文字色"):
            tk.Button(root, text="選擇", command=lambda v=var: pick_color(v)).grid(
                row=row,
                column=1,
                padx=8,
                pady=6,
                sticky="e",
            )

    status_var = tk.StringVar(value="請設定參數後按開始或產生 EXE。")
    tk.Label(root, textvariable=status_var, fg="#666666").grid(row=len(fields), column=0, columnspan=2, pady=8)

    tk.Checkbutton(root, text="立即打包 EXE (需安裝 PyInstaller)", variable=build_now_var).grid(
        row=len(fields) + 1,
        column=0,
        columnspan=2,
        pady=4,
    )

    def parse_inputs() -> tuple[int, int, int, int, float, int]:
        try:
            speed = int(speed_var.get())
            font_size = int(font_size_var.get())
            tts_rate = int(tts_rate_var.get())
            tts_repeat = int(tts_repeat_var.get())
            tts_interval_minutes = float(tts_interval_var.get())
            loops = int(loops_var.get())
        except ValueError:
            status_var.set("數值欄位需輸入數字。")
            raise
        return speed, font_size, tts_rate, tts_repeat, tts_interval_minutes, loops

    def start_marquee() -> None:
        try:
            speed, font_size, tts_rate, tts_repeat, tts_interval_minutes, loops = parse_inputs()
        except ValueError:
            return

        root.destroy()
        app = MarqueeTTSApp(
            message=message_var.get(),
            speed=speed,
            font_size=font_size,
            bg=bg_var.get(),
            fg=fg_var.get(),
            tts_rate=tts_rate,
            tts_repeat=tts_repeat,
            tts_interval_seconds=tts_interval_minutes * 60,
            loops=loops,
        )
        app.run()

    def build_exe() -> None:
        try:
            speed, font_size, tts_rate, tts_repeat, tts_interval_minutes, loops = parse_inputs()
        except ValueError:
            return

        output_dir = Path(output_dir_var.get()).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        script_path = output_dir / "marquee_tts_build.py"
        script_path.write_text(
            build_script_content(
                message=message_var.get(),
                speed=speed,
                font_size=font_size,
                bg=bg_var.get(),
                fg=fg_var.get(),
                tts_rate=tts_rate,
                tts_repeat=tts_repeat,
                tts_interval_minutes=tts_interval_minutes,
                loops=loops,
            ),
            encoding="utf-8",
        )

        exe_name = exe_name_var.get().strip() or "MarqueeTTS"
        command = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name",
            exe_name,
            str(script_path),
        ]
        if build_now_var.get():
            try:
                result = subprocess.run(command, check=False, capture_output=True, text=True)
            except FileNotFoundError:
                status_var.set("找不到 PyInstaller，請先 pip install pyinstaller。")
                return
            if result.returncode == 0:
                status_var.set(f"打包完成，EXE 位於 {output_dir / 'dist'}")
            else:
                status_var.set("打包失敗，請檢查 PyInstaller 輸出。")
        else:
            status_var.set("已產生打包腳本。請在 Windows 執行 PyInstaller 指令。")

    tk.Button(root, text="開始跑馬燈", command=start_marquee, width=24).grid(
        row=len(fields) + 2,
        column=0,
        columnspan=2,
        pady=8,
    )
    tk.Button(root, text="產生 EXE", command=build_exe, width=24).grid(
        row=len(fields) + 3,
        column=0,
        columnspan=2,
        pady=6,
    )

    root.mainloop()


def main() -> None:
    args = parse_args()
    if args.gui:
        launch_gui()
        return
    app = MarqueeTTSApp(
        message=args.message,
        speed=args.speed,
        font_size=args.font_size,
        bg=args.bg,
        fg=args.fg,
        tts_rate=args.tts_rate,
        tts_repeat=args.tts_repeat,
        tts_interval_seconds=args.tts_interval_minutes * 60,
        loops=args.loops,
    )
    app.run()


if __name__ == "__main__":
    main()

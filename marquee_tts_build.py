import threading
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


def main() -> None:
    app = MarqueeTTSApp(
        message='📢 提醒：信用卡感應後，請盯緊電子螢幕，顯示免簽名出單據才算完成，🚫 禁止漏簽！ ',
        speed=4,
        font_size=28,
        bg='#ffff00',
        fg='#ff0000',
        tts_rate=190,
        tts_repeat=0,
        tts_interval_seconds=0.0 * 60,
        loops=1,
    )
    app.run()


if __name__ == "__main__":
    main()

import tkinter as tk
from collections.abc import Callable


class StatusUi:
    def __init__(
        self,
        on_read_selection: Callable[[], None],
        on_stop: Callable[[], None],
        on_test_voice: Callable[[], None],
        on_quit: Callable[[], None],
        log_path: str | None = None,
    ) -> None:
        self._on_quit = on_quit

        self.root = tk.Tk()
        self.root.title("Readaloud Tool")
        self.root.geometry("420x220")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._handle_close)

        self._status_var = tk.StringVar(value="Ready")
        self._error_var = tk.StringVar(value="")

        title = tk.Label(self.root, text="Readaloud Tool", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(10, 4))

        status = tk.Label(self.root, textvariable=self._status_var, font=("Segoe UI", 10))
        status.pack()

        error = tk.Label(self.root, textvariable=self._error_var, font=("Segoe UI", 9), fg="firebrick")
        error.pack(pady=(2, 6))

        button_row = tk.Frame(self.root)
        button_row.pack(pady=(4, 8))

        self._read_button = tk.Button(button_row, text="Read Selection", width=16, command=on_read_selection)
        self._read_button.grid(row=0, column=0, padx=4, pady=2)

        self._stop_button = tk.Button(button_row, text="Stop", width=12, command=on_stop)
        self._stop_button.grid(row=0, column=1, padx=4, pady=2)

        self._test_button = tk.Button(button_row, text="Test Voice", width=12, command=on_test_voice)
        self._test_button.grid(row=1, column=0, padx=4, pady=2)

        self._quit_button = tk.Button(button_row, text="Quit", width=12, command=self._handle_close)
        self._quit_button.grid(row=1, column=1, padx=4, pady=2)

        hotkeys = tk.Label(
            self.root,
            text=(
                "Hotkeys: Ctrl+Alt+R read selection | "
                "Ctrl+Alt+S stop | Ctrl+Alt+Q quit"
            ),
            font=("Segoe UI", 8),
        )
        hotkeys.pack(pady=(4, 6))

        if log_path:
            log_label = tk.Label(self.root, text=f"Log: {log_path}", font=("Segoe UI", 7))
            log_label.pack(pady=(0, 6))

    def run(self) -> None:
        self.root.mainloop()

    def close(self) -> None:
        self.root.destroy()

    def call_soon(self, fn: Callable[[], None]) -> None:
        self.root.after(0, fn)

    def set_status(self, message: str) -> None:
        self.root.after(0, lambda: self._status_var.set(message))

    def set_error(self, message: str) -> None:
        self.root.after(0, lambda: self._error_var.set(message))

    def clear_error(self) -> None:
        self.root.after(0, lambda: self._error_var.set(""))

    def set_actions_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in (self._read_button, self._stop_button, self._test_button):
            btn.configure(state=state)

    def _handle_close(self) -> None:
        self._on_quit()

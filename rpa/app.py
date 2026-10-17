"""In-memory desk. Screens, fields and buttons. No desktop and no vendor runtime."""

from __future__ import annotations


class AppError(RuntimeError):
    pass


class Desk:
    def __init__(self) -> None:
        self.screen = "home"
        self.banner = "unread notice"
        self.fields = {"applicant": "", "case_id": ""}
        self.submitted = False
        self.log: list[str] = []

    def observe(self) -> dict:
        buttons = []
        if self.screen == "home":
            buttons = ["dismiss_notice", "open_intake"] if self.banner else ["open_intake"]
        elif self.screen == "intake":
            buttons = ["submit", "back"]
        elif self.screen == "done":
            buttons = ["back"]
        return {
            "screen": self.screen,
            "banner": self.banner,
            "fields": dict(self.fields),
            "buttons": buttons,
            "submitted": self.submitted,
            "blocked": bool(self.banner) and self.screen == "home",
        }

    def click(self, button: str) -> None:
        obs = self.observe()
        if button not in obs["buttons"]:
            raise AppError(f"{button} is not on {self.screen}")
        if button == "dismiss_notice":
            self.banner = ""
        elif button == "open_intake":
            if self.banner:
                raise AppError("notice is still up")
            self.screen = "intake"
        elif button == "submit":
            missing = [name for name, value in self.fields.items() if not value]
            if missing:
                raise AppError("missing " + ",".join(missing))
            self.submitted = True
            self.screen = "done"
        elif button == "back":
            self.screen = "home"
        else:
            raise AppError(f"unknown button {button}")
        self.log.append(f"click {button}")

    def type(self, field: str, value: str) -> None:
        if self.screen != "intake":
            raise AppError(f"cannot type on {self.screen}")
        if field not in self.fields:
            raise AppError(f"unknown field {field}")
        if not value:
            raise AppError("blank value")
        self.fields[field] = value
        self.log.append(f"type {field}")

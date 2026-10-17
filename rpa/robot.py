"""Step runner. Actions are data. Failures stay in the transcript."""

from __future__ import annotations

from rpa.app import AppError, Desk


def apply_action(desk: Desk, action: dict) -> dict:
    kind = action.get("op")
    try:
        if kind == "click":
            desk.click(action["button"])
        elif kind == "type":
            desk.type(action["field"], action["value"])
        elif kind == "read":
            return {"ok": True, "observation": desk.observe(), "read": desk.observe()["fields"].get(action["field"])}
        else:
            raise AppError(f"unknown op {kind}")
        return {"ok": True, "observation": desk.observe(), "error": ""}
    except AppError as exc:
        return {"ok": False, "observation": desk.observe(), "error": str(exc)}

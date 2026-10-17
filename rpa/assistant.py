"""Local policy that picks the next step. A stand-in for an assistant, not a hosted model.

This is not UiPath, not a UiPath certification, and not a vendor robot.
"""

from __future__ import annotations

from rpa.robot import apply_action


def next_action(goal: str, observation: dict, packet: dict) -> dict:
    if goal != "file_intake":
        return {"op": "stop", "reason": f"unsupported goal {goal}"}
    if observation["submitted"]:
        return {"op": "stop", "reason": "filed"}
    if observation["blocked"]:
        return {"op": "click", "button": "dismiss_notice"}
    if observation["screen"] == "home":
        return {"op": "click", "button": "open_intake"}
    if observation["screen"] == "intake":
        for field in ("applicant", "case_id"):
            if not observation["fields"].get(field):
                value = packet.get(field, "")
                if not value:
                    return {"op": "stop", "reason": f"packet missing {field}"}
                return {"op": "type", "field": field, "value": value}
        return {"op": "click", "button": "submit"}
    return {"op": "stop", "reason": f"no step for {observation['screen']}"}


def run(desk, goal: str, packet: dict, max_steps: int = 8) -> dict:
    transcript = []
    for _ in range(max_steps):
        observation = desk.observe()
        action = next_action(goal, observation, packet)
        if action["op"] == "stop":
            transcript.append({"action": action, "ok": action.get("reason") == "filed", "error": action.get("reason", "")})
            break
        result = apply_action(desk, action)
        transcript.append({"action": action, "ok": result["ok"], "error": result.get("error", "")})
        if not result["ok"]:
            break
    return {
        "submitted": desk.submitted,
        "steps": len(transcript),
        "log": list(desk.log),
        "transcript": transcript,
    }

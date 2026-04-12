from typing import Any
from models import CyberState


# =========================
# HELPERS
# =========================
def _has_action(actions, action_type):
    return any(a.get("action_type") == action_type for a in actions)


def _correct_target(actions, expected_target):
    return any(a.get("target") == expected_target for a in actions)


# =========================
# TASK 1 — ORDER STATUS
# =========================
def grade_task1(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "check_order"):
        score += 0.3

    if _has_action(state.actions_taken, "track_package"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 2 — LATE DELIVERY
# =========================
def grade_task2(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "check_order"):
        score += 0.3

    if _has_action(state.actions_taken, "escalate_issue"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 3 — WRONG ITEM
# =========================
def grade_task3(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "check_order"):
        score += 0.3

    if _has_action(state.actions_taken, "replace_item"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 4 — REFUND
# =========================
def grade_task4(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "check_order"):
        score += 0.3

    if _has_action(state.actions_taken, "initiate_refund"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 5 — PAYMENT FAILURE
# =========================
def grade_task5(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "check_order"):
        score += 0.3

    if _has_action(state.actions_taken, "check_payment"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# MAP (FIXED)
# =========================
GRADER_MAP = {
    "task_1_order_status": grade_task1,
    "task_2_late_delivery": grade_task2,
    "task_3_wrong_item": grade_task3,
    "task_4_refund": grade_task4,
    "task_5_payment_failure": grade_task5,
}


# =========================
# MAIN
# =========================
def grade(state: CyberState) -> float:
    if state.task_id not in GRADER_MAP:
        raise ValueError(f"Unknown task: {state.task_id}")

    raw = GRADER_MAP[state.task_id](state)

    # penalty for too few steps
    if len(state.actions_taken) <= 1:
        raw -= 0.1

    return max(0.01, min(raw, 0.99))

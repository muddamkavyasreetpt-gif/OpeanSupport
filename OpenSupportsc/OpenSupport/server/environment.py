from __future__ import annotations
import copy
import uuid
import random
from typing import Any

from openenv.core.env_server import Environment
from models import CyberAction, CyberObservation, CyberState
from server.scenarios import TASK_MAP


class CyberEnvironment(Environment):
    def __init__(self) -> None:
        super().__init__()
        self._state: CyberState = CyberState()
        self._scenario: dict[str, Any] = {}
        self._systems: dict[str, Any] = {}
        self._logs: dict[str, list[str]] = {}

    # =========================
    # RESET
    # =========================
    def reset(self, task_id: str | None = None, **kwargs: Any) -> CyberObservation:
        if not task_id:
            task_id = "task_1_order_status"

        if task_id not in TASK_MAP:
            raise ValueError(f"Unknown task_id: {task_id}")

        scenario = TASK_MAP[task_id]

        self._scenario = scenario
        self._systems = copy.deepcopy(scenario.get("systems", {}))
        self._logs = copy.deepcopy(scenario.get("logs", {}))

        # add small randomness (keeps realism)
        for sys in self._systems.values():
            if isinstance(sys, dict):
                sys["noise"] = random.randint(0, 2)

        self._state = CyberState(
            episode_id=str(uuid.uuid4()),
            task_id=scenario["task_id"],
            step_count=0,
            actions_taken=[],
            attack_identified=False,
            fix_applied=False,
            system_secured=False,
            current_score=0.0,
        )

        return CyberObservation(
            output=f"🛒 {scenario['description']}",
            systems=self._systems,
            done=False,
            success=True,
            steps_remaining=scenario["max_steps"],
            partial_score=0.0,
        )

    # =========================
    # STEP
    # =========================
    def step(self, action: CyberAction, **kwargs: Any) -> CyberObservation:
        self._state.step_count += 1
        max_steps = self._scenario["max_steps"]

        self._state.actions_taken.append({
            "action_type": action.action_type,
            "target": action.target
        })

        obs = self._dispatch(action)

        # done logic
        if self._state.system_secured:
            obs.done = True
            obs.output += "\n✅ Issue resolved!"
        elif self._state.step_count >= max_steps:
            obs.done = True
            obs.output += "\n❌ Max steps reached"

        prev_score = self._state.current_score
        self._state.current_score = self._calculate_score()

        obs.reward = round(self._state.current_score - prev_score, 4)
        obs.steps_remaining = max_steps - self._state.step_count
        obs.partial_score = self._state.current_score
        obs.systems = self._systems

        return obs

    # =========================
    # DISPATCH
    # =========================
    def _dispatch(self, action: CyberAction) -> CyberObservation:
        handlers = {
            "check_order": self._handle_check_order,
            "track_package": self._handle_track_package,
            "replace_item": self._handle_replace_item,
            "initiate_refund": self._handle_refund,
            "check_payment": self._handle_payment,
            "escalate_issue": self._handle_escalate,
        }

        handler = handlers.get(action.action_type)

        if not handler:
            return CyberObservation(
                output="Invalid action",
                systems=self._systems,
                success=False,
                error="Unknown action"
            )

        return handler(action)

    # =========================
    # ACTION HANDLERS
    # =========================

    def _handle_check_order(self, action: CyberAction):
        self._state.attack_identified = True

        logs = self._logs.get(action.target, [])

        return CyberObservation(
            output="\n".join(logs) if logs else "No order details found",
            systems=self._systems
        )

    def _handle_track_package(self, action: CyberAction):
        if not self._state.attack_identified:
            return CyberObservation(
                output="Check order details first",
                success=False,
                systems=self._systems
            )

        self._state.fix_applied = True
        self._state.system_secured = True

        return CyberObservation(
            output="Package tracking shared with customer",
            systems=self._systems
        )

    def _handle_replace_item(self, action: CyberAction):
        if not self._state.attack_identified:
            return CyberObservation(
                output="Check order details first",
                success=False,
                systems=self._systems
            )

        self._state.fix_applied = True
        self._state.system_secured = True

        return CyberObservation(
            output="Replacement initiated successfully",
            systems=self._systems
        )

    def _handle_refund(self, action: CyberAction):
        if not self._state.attack_identified:
            return CyberObservation(
                output="Check order details first",
                success=False,
                systems=self._systems
            )

        self._state.fix_applied = True
        self._state.system_secured = True

        return CyberObservation(
            output="Refund initiated successfully",
            systems=self._systems
        )

    def _handle_payment(self, action: CyberAction):
        if not self._state.attack_identified:
            return CyberObservation(
                output="Check order details first",
                success=False,
                systems=self._systems
            )

        self._state.fix_applied = True
        self._state.system_secured = True

        return CyberObservation(
            output="Payment issue resolved",
            systems=self._systems
        )

    def _handle_escalate(self, action: CyberAction):
        if not self._state.attack_identified:
            return CyberObservation(
                output="Check order details first",
                success=False,
                systems=self._systems
            )

        self._state.fix_applied = True
        self._state.system_secured = True

        return CyberObservation(
            output="Issue escalated to support team",
            systems=self._systems
        )

    # =========================
    # SCORING
    # =========================
    def _calculate_score(self):
        score = 0.0

        if self._state.attack_identified:
            score += 0.3

        if self._state.fix_applied:
            score += 0.3

        if self._state.system_secured:
            score += 0.4

        if self._state.step_count <= 2:
            score -= 0.1

        return max(0.0, min(score, 1.0))

    @property
    def state(self):
        return self._state

from typing import Any

BASE_SYSTEM = {
    "order-system": {"status": "active"},
    "delivery-system": {"status": "active"},
    "payment-system": {"status": "active"},
}

TASK1 = {
    "task_id": "task_1_order_status",
    "difficulty": "easy",
    "description": "Customer asks: Where is my order?",
    "max_steps": 10,
    "systems": BASE_SYSTEM,
    "logs": {
        "order-system": [
            "Order #1234 placed",
            "Order shipped",
            "Tracking available"
        ]
    },
    "solution": {
        "action_type": "track_package",
        "target": "order_1234"
    }
}

TASK2 = {
    "task_id": "task_2_late_delivery",
    "difficulty": "medium",
    "description": "Customer complains about late delivery",
    "max_steps": 10,
    "systems": BASE_SYSTEM,
    "logs": {
        "delivery-system": [
            "Order delayed",
            "Delivery exceeded expected time"
        ]
    },
    "solution": {
        "action_type": "escalate_issue",
        "target": "delivery_team"
    }
}

TASK3 = {
    "task_id": "task_3_wrong_item",
    "difficulty": "medium",
    "description": "Customer received wrong item",
    "max_steps": 10,
    "systems": BASE_SYSTEM,
    "logs": {
        "order-system": [
            "Mismatch in order items",
            "Customer complaint registered"
        ]
    },
    "solution": {
        "action_type": "replace_item",
        "target": "order_5678"
    }
}

TASK4 = {
    "task_id": "task_4_refund",
    "difficulty": "hard",
    "description": "Customer requests refund",
    "max_steps": 12,
    "systems": BASE_SYSTEM,
    "logs": {
        "payment-system": [
            "Refund requested",
            "Payment completed earlier"
        ]
    },
    "solution": {
        "action_type": "initiate_refund",
        "target": "order_9999"
    }
}

TASK5 = {
    "task_id": "task_5_payment_failure",
    "difficulty": "hard",
    "description": "Customer payment failed",
    "max_steps": 12,
    "systems": BASE_SYSTEM,
    "logs": {
        "payment-system": [
            "Transaction failed",
            "Gateway timeout"
        ]
    },
    "solution": {
        "action_type": "check_payment",
        "target": "order_7777"
    }
}

TASK_MAP = {
    "task_1_order_status": TASK1,
    "task_2_late_delivery": TASK2,
    "task_3_wrong_item": TASK3,
    "task_4_refund": TASK4,
    "task_5_payment_failure": TASK5,
}

ALL_TASKS = list(TASK_MAP.values())

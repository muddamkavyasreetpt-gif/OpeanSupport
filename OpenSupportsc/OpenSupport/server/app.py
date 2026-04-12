from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from openenv.core.env_server.http_server import create_app

from models import CyberAction, CyberObservation
from server.environment import CyberEnvironment
from server.graders import grade, GRADER_MAP
from server.scenarios import ALL_TASKS

import uvicorn

# =========================
# SINGLE GLOBAL ENV (IMPORTANT 🔥)
# =========================
_env = CyberEnvironment()

def _env_factory():
    return _env   # ✅ ensures SAME state is used


# =========================
# CREATE APP
# =========================
app = create_app(
    _env_factory,
    CyberAction,
    CyberObservation,
    env_name="EcomRL 🛒"
)

app.title = "EcomRL API"
app.description = "AI-powered e-commerce support simulation"
app.version = "1.0"


# =========================
# UI DASHBOARD
# =========================
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>EcomRL Dashboard</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0f172a;
                color: #e2e8f0;
            }

            .container {
                padding: 30px;
                max-width: 1100px;
                margin: auto;
            }

            h1 {
                color: #22c55e;
            }

            .subtitle {
                color: #94a3b8;
                margin-bottom: 20px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }

            .card {
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
            }

            .card h2 {
                margin: 0;
                color: #22c55e;
            }

            .section {
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
            }

            .badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
                margin-right: 5px;
            }

            .easy { background: #16a34a; }
            .medium { background: #f59e0b; }
            .hard { background: #dc2626; }

            .endpoint {
                display: flex;
                justify-content: space-between;
                padding: 10px;
                border-bottom: 1px solid #334155;
            }

            .method {
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 5px;
                margin-right: 10px;
            }

            .get { background: #3b82f6; }
            .post { background: #22c55e; }

            pre {
                background: #020617;
                padding: 10px;
                border-radius: 8px;
                overflow-x: auto;
            }

            .footer {
                margin-top: 30px;
                text-align: center;
                color: #64748b;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🛒 EcomRL Environment</h1>
            <p class="subtitle">
                OpenEnv • E-Commerce Support • RL Agent Training
            </p>

            <div class="grid">
                <div class="card">
                    <h2>5</h2>
                    <p>Customer Tasks</p>
                </div>
                <div class="card">
                    <h2>6</h2>
                    <p>Agent Actions</p>
                </div>
                <div class="card">
                    <h2>~0.80</h2>
                    <p>Baseline Score</p>
                </div>
            </div>

            <div class="section">
                <h3>📋 Tasks</h3>
                <p><span class="badge easy">EASY</span> Order status → track package</p>
                <p><span class="badge medium">MEDIUM</span> Late delivery → escalate issue</p>
                <p><span class="badge medium">MEDIUM</span> Wrong item → replace item</p>
                <p><span class="badge hard">HARD</span> Refund → initiate refund</p>
                <p><span class="badge hard">HARD</span> Payment failure → check payment</p>
            </div>

            <div class="section">
                <h3>⚡ API Endpoints</h3>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/health</div>
                    <div>Status</div>
                </div>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/tasks</div>
                    <div>List tasks</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/reset</div>
                    <div>Start task</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/step</div>
                    <div>Take action</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/grader</div>
                    <div>Get score</div>
                </div>
            </div>

            <div class="section">
                <h3>🚀 Quick Test</h3>
                <pre>
curl -X POST "http://localhost:7860/reset" -H "Content-Type: application/json" -d '{"task_id":"task_1_order_status"}'

curl -X POST "http://localhost:7860/step" -H "Content-Type: application/json" -d '{"action":{"action_type":"check_order","target":"order-system"}}'
                </pre>
            </div>

            <div class="footer">
                Built for Hackathon 🚀 • E-Commerce AI Agent
            </div>
        </div>
    </body>
    </html>
    """


# =========================
# TASKS
# =========================
@app.get("/tasks")
def get_tasks():
    return {"tasks": ALL_TASKS}


# =========================
# GRADER (FIXED 🔥)
# =========================
@app.post("/grader")
def run_grader():
    try:
        state = _env.state

        if not state or not state.task_id:
            return {
                "error": "No active episode. Call /reset first.",
                "score": 0.01
            }

        score = grade(state)

        return {
            "task_id": state.task_id,
            "score": score
        }

    except Exception as e:
        return {
            "error": str(e),
            "task_id": getattr(_env.state, "task_id", "unknown"),
            "score": 0.01
        }


# =========================
# BASELINE (FIXED 🔥)
# =========================
@app.post("/baseline")
def run_baseline():
    from models import CyberAction

    results = []

    TASKS = [
        "task_1_order_status",
        "task_2_late_delivery",
        "task_3_wrong_item",
        "task_4_refund",
        "task_5_payment_failure",
    ]

    for task_id in TASKS:
        try:
            _env.reset(task_id=task_id)

            _env.step(CyberAction(
                action_type="check_order",
                target="order-system"
            ))

            _env.step(CyberAction(
                action_type="track_package",
                target="order_1234"
            ))

            score = grade(_env.state)

        except:
            score = 0.01

        results.append({
            "task_id": task_id,
            "score": round(score, 4)
        })

    return {"baseline_scores": results}


# =========================
# RUN
# =========================
def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )


if __name__ == "__main__":
    main()

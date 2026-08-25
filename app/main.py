from datetime import datetime, timezone

from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "Cloud-Native Delivery Platform",
                "status": "running",
            }
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.post("/normalise")
    def normalise():
        body = request.get_json(silent=True) or {}
        rule = body.get("rule", "").strip()

        if not rule:
            return jsonify({"error": "A rule is required"}), 400

        return jsonify(
            {
                "original": rule,
                "normalised": " ".join(rule.lower().split()),
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
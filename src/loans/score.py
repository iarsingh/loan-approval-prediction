REQUIRED = ("income", "debt_ratio", "credit_months",)
WEIGHTS = {"income": 0.00002, "debt_ratio": -6.0, "credit_months": 0.01}
INTERCEPT = -1.5
THRESHOLD = 0.0


class InputError(ValueError):
    pass


def score(body):
    missing = [name for name in REQUIRED if name not in body]
    if missing:
        raise InputError("missing " + ", ".join(missing))
    total = INTERCEPT
    parts = []
    for name, weight in WEIGHTS.items():
        value = body[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InputError(f"{name} must be a number")
        contrib = weight * value
        total += contrib
        parts.append({"feature": name, "contribution": round(contrib, 4)})
    label = "approved" if total >= THRESHOLD else "declined"
    return {"score": round(total, 4), "label": label, "threshold": THRESHOLD, "parts": parts}

"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value

def replay_updates(data):
    fields(data, ("value", "version", "events"))
    value, version = integer(data["value"], -10**9, 10**9), integer(data["version"])
    pending, results = None, []
    for event in sequence(data["events"], 500):
        if not isinstance(event, dict):
            raise ValueError("Expected event object")
        action = event.get("action")
        if action == "begin":
            fields(event, ("action", "id", "value"))
            ident, proposed = label(event["id"]), integer(event["value"], -10**9, 10**9)
            if pending is not None:
                raise ValueError("Only one pending edit is supported")
            pending = {"id": ident, "value": proposed, "version": version}
            outcome = "pending"
        elif action == "resolve":
            fields(event, ("action", "id", "success"))
            if type(event["success"]) is not bool or pending is None or label(event["id"]) != pending["id"]:
                raise ValueError("Resolution must match the pending edit")
            if not event["success"]:
                outcome = "rolled_back"
            elif pending["version"] != version:
                outcome = "conflict"
            else:
                value, version = pending["value"], version + 1
                outcome = "committed"
            pending = None
        elif action == "refresh":
            fields(event, ("action", "value", "version"))
            fresh, revision = integer(event["value"], -10**9, 10**9), integer(event["version"])
            outcome = "stale"
            if revision > version:
                value, version, outcome = fresh, revision, "refreshed"
        else:
            raise ValueError("Unknown event action")
        results.append({"outcome": outcome, "value": pending["value"] if pending else value,
                        "version": version, "pending": pending["id"] if pending else None})
    return {"results": results, "value": pending["value"] if pending else value, "version": version,
            "pending": pending["id"] if pending else None}

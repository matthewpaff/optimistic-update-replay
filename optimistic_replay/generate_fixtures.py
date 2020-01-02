"""Original generated examples with independent expected results."""

def make_case(index):
    value, ident = index, "edit_" + str(index)
    begin = {"action": "begin", "id": ident, "value": value + 1}
    resolve = {"action": "resolve", "id": ident, "success": True}
    data = {"value": value, "version": 1, "events": [begin, resolve]}
    pending = {"outcome": "pending", "value": value + 1, "version": 1, "pending": ident}
    kind, description = index % 8, "confirm an optimistic edit against its original version"
    results = [pending, {"outcome": "committed", "value": value + 1, "version": 2, "pending": None}]
    final, version, pending_id = value + 1, 2, None
    if kind == 1:
        resolve["success"] = False
        results[1] = {"outcome": "rolled_back", "value": value, "version": 1, "pending": None}
        final, version, description = value, 1, "roll back a rejected optimistic edit"
    elif kind == 2:
        data["events"] = [begin, {"action": "refresh", "value": value + 5, "version": 3}, resolve]
        results = [pending, {"outcome": "refreshed", "value": value + 1, "version": 3, "pending": ident},
                   {"outcome": "conflict", "value": value + 5, "version": 3, "pending": None}]
        final, version, description = value + 5, 3, "preserve a newer refresh when an old edit resolves"
    elif kind == 3:
        data["events"] = [{"action": "refresh", "value": -1, "version": 1}]
        results = [{"outcome": "stale", "value": value, "version": 1, "pending": None}]
        final, version, description = value, 1, "ignore an equal-version refresh payload"
    elif kind == 4:
        data["events"] = [begin, begin.copy()]
        description = "reject a second edit while another edit is pending"
    elif kind == 5:
        resolve["id"] = "unknown"
        description = "require resolution IDs to match the pending edit"
    elif kind == 6:
        data["version"] = True
        description = "reject boolean cache versions"
    elif kind == 7:
        data["events"] = [begin]
        results, final, version, pending_id = [pending], value + 1, 1, ident
        description = "retain the displayed optimistic value while unresolved"
    case = {"id": "cache-{:04d}".format(index), "description": description, "input": data}
    case.update({"expected_error": True} if kind in (4, 5, 6) else {"expected": {"results": results, "value": final, "version": version, "pending": pending_id}})
    return case

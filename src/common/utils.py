def generate_update_diff(model, update_data: dict):
    diff = {}
    for key, after in update_data.items():
        before = getattr(model, key)
        if before != after:
            diff[key] = {"before": before, "after": after}
    return diff

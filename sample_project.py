def process_records(records):
    result = []
    for record in records:
        if record.get("active"):
            if record.get("score", 0) > 50:
                if record.get("verified"):
                    result.append(record)
    return result

def format_record(record):
    return str(record.get("name", "")).strip().lower()

def rowsToDictionary(cursor, rows):
    if rows is None:
        return None
    # If it's not a table, just return it as 1
    if isinstance(rows, tuple):
        return {col[0]: rows[idx] for idx, col in enumerate(cursor.description)}
    # If it's a table of rows, handle all of them
    return [{col[0]: row[idx] for idx, col in enumerate(cursor.description)} for row in rows]
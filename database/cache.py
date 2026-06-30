from database.db import get_connection


def get_file_id(url: str, quality: str):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT file_id
        FROM downloads
        WHERE url=? AND quality=?
        """,
        (url, quality),
    ).fetchone()

    conn.close()

    if row:
        return row["file_id"]

    return None


def save_file_id(url: str, quality: str, file_id: str):
    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO downloads
        (url, quality, file_id)
        VALUES (?, ?, ?)
        """,
        (url, quality, file_id),
    )

    conn.commit()
    conn.close()

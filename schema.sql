CREATE TABLE IF NOT EXISTS app_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    window_title TEXT,
    date TEXT NOT NULL,
    seconds_used INTEGER DEFAULT 0
);

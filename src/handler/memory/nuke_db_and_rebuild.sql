DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS nodes;

CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id      INTEGER NOT NULL,
    predicate_id    INTEGER NOT NULL,
    object_id       INTEGER NOT NULL,

    confidence      REAL    NOT     NULL    DEFAULT 1.0,
    source          TEXT    NOT     NULL    DEFAULT 'user',
    created_at      TEXT    NOT     NULL    DEFAULT (datetime('now')),

    FOREIGN KEY (subject_id)    REFERENCES nodes(id),
    FOREIGN KEY (predicate_id)  REFERENCES nodes(id),
    FOREIGN KEY (object_id)     REFERENCES nodes(id),

    UNIQUE(subject_id, predicate_id, object_id)
);

CREATE INDEX IF NOT EXISTS idx_subject   ON relationships(subject_id);
CREATE INDEX IF NOT EXISTS idx_object    ON relationships(object_id);
CREATE INDEX IF NOT EXISTS idx_predicate ON relationships(predicate_id);
CREATE INDEX IF NOT EXISTS idx_source    ON relationships(source);
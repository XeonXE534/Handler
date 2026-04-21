DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS nodes;

CREATE TABLE nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE relationships (
    subject_id INTEGER NOT NULL,
    predicate_id INTEGER NOT NULL,
    object_id INTEGER NOT NULL,

    FOREIGN KEY (subject_id) REFERENCES nodes(id),
    FOREIGN KEY (predicate_id) REFERENCES nodes(id),
    FOREIGN KEY (object_id) REFERENCES nodes(id),

    UNIQUE(subject_id, predicate_id, object_id)
);

CREATE INDEX idx_subject ON relationships(subject_id);
CREATE INDEX idx_object ON relationships(object_id);
CREATE INDEX idx_predicate ON relationships(predicate_id);
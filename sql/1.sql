-- Add scores_log table for tracking karma over time

CREATE TABLE scores_log (
    Id INTEGER NOT NULL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Change INTEGER NOT NULL,
    Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema (
    Version,
    Installed,
    Comment
) VALUES (
    1,
    CURRENT_TIMESTAMP,
    'Add scores_log table'
);

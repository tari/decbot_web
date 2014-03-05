-- Database initialization. Creates karma and quotes tables in addition
-- to the schema versioning table.

CREATE TABLE links (
    Name VARCHAR(100) PRIMARY KEY NOT NULL,
    Link VARCHAR(100) NOT NULL
);

CREATE TABLE scores (
    Name VARCHAR(100) PRIMARY KEY NOT NULL,
    Score INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE quotes (
    -- Use engine's equivalent as necessary
    Id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Timestamp DATETIME NOT NULL,
    AddedBy VARCHAR(45) NOT NULL,
    Quote TEXT NOT NULL,
    Active BOOLEAN NOT NULL DEFAULT True,
    ScoreUp INTEGER NOT NULL DEFAULT 0,
    ScoreDown INTEGER NOT NULL DEFAULT 0,
    DeletedBy VARCHAR(45) DEFAULT NULL
);

CREATE TABLE schema (
    Version INTEGER PRIMARY KEY NOT NULL,
    Installed DATETIME NOT NULL,
    Comment TEXT
);
INSERT INTO schema (
    Version,
    Installed,
    Comment
) VALUES (
    0,
    -- Use engine's equivalent as necessary, such as DATETIME() in sqlite.
    NOW(),
    'Initial install'
);

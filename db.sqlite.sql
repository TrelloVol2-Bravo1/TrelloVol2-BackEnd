BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user"
(
    "id"            INTEGER      NOT NULL,
    "name"          VARCHAR(32)  NOT NULL,
    "email"         VARCHAR(64),
    "password_hash" VARCHAR(256) NOT NULL,
    "access_level"  INTEGER      NOT NULL,
    "creation_date" DATETIME,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "auth"
(
    "api_id"   INTEGER NOT NULL,
    "user_id"  INTEGER,
    "api_key"  VARCHAR(256),
    "api_date" DATETIME,
    PRIMARY KEY ("api_id")
);
COMMIT;

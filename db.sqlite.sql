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
    PRIMARY KEY ("api_id")ą zm
);

CREATE TABLE IF NOT EXISTS "table"
(
    "id"   INTEGER NOT NULL,
    "name"  VARCHAR(64) NOT NULL,
    "author_id"  INTEGER NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "user_to_table"
(
    "id"   INTEGER NOT NULL,
    "table_id"  INTEGER NOT NULL,
    "user_id"  INTEGER NOT NULL,
    "is_favourite" BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY ("id")
);

INSERT INTO "user" ("id", "name", "email", "password_hash", "access_level")
VALUES(1,"admin", "admin@admin.pl", "$6$rounds=656000$.TQuK6zBu0dPK4p0$.DEH3JxVHVvXEKv.3uq/WDzM5i2cA5rzQuM5bIQmqc6xu4Oosf99NL4eEj77hv/J4zE./A3GJhiCFxISnWeZV0", 0);

INSERT INTO "table" ("id", "name", "author_id")
VALUES(1, "My TRELLO", 1);
COMMIT;

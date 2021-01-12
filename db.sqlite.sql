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

CREATE TABLE IF NOT EXISTS "table"
(
    "table_id"   INTEGER NOT NULL,
    "table_name"  VARCHAR(64) NOT NULL,
    "table_description" VARCHAR(1024),
    "user_id"  INTEGER NOT NULL,
    PRIMARY KEY ("table_id")
);

CREATE TABLE IF NOT EXISTS "list"
(
    "list_id"   INTEGER NOT NULL,
    "list_name"  VARCHAR(64) NOT NULL,
    "list_order" INTEGER,
    "list_description" VARCHAR(1024),
    "table_id"  INTEGER NOT NULL,
    "is_archived" INTEGER CHECK ( is_archived in (0, 1)) NOT NULL ,
    PRIMARY KEY ("list_id")
);

CREATE TABLE IF NOT EXISTS "card"
(
    "card_id"   INTEGER NOT NULL,
    "card_name"  VARCHAR(64) NOT NULL,
    "card_description" VARCHAR(1028),
    "list_id"  INTEGER NOT NULL,
    "is_archived" INTEGER CHECK ( is_archived in (0, 1)) NOT NULL ,
    "card_deadline" DATETIME,
    PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "card_members"
(
    "card_members_id" INTEGER NOT NULL,
    "card_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    PRIMARY KEY ("card_members_id")
);

CREATE TABLE IF NOT EXISTS "table_members"
(
    "table_members_id" INTEGER NOT NULL,
    "table_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    PRIMARY KEY ("table_members_id")
);

INSERT INTO "user" ("id", "name", "email", "password_hash", "access_level")
VALUES(1,"admin", "admin@admin.pl", "$6$rounds=656000$.TQuK6zBu0dPK4p0$.DEH3JxVHVvXEKv.3uq/WDzM5i2cA5rzQuM5bIQmqc6xu4Oosf99NL4eEj77hv/J4zE./A3GJhiCFxISnWeZV0", 0);

COMMIT;

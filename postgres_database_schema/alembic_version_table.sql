-- Table: public.alembic_version

-- DROP TABLE IF EXISTS public.alembic_version;

CREATE TABLE IF NOT EXISTS public.alembic_version
(
    version_num character varying(32) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.alembic_version
    OWNER to postgres;


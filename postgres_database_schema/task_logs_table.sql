-- Table: public.task_logs

-- DROP TABLE IF EXISTS public.task_logs;

CREATE TABLE IF NOT EXISTS public.task_logs
(
    task_id integer NOT NULL,
    status character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    CONSTRAINT task_logs_task_id_fkey FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.task_logs
    OWNER to postgres;


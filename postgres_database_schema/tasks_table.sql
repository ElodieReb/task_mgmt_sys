-- Table: public.tasks

-- DROP TABLE IF EXISTS public.tasks;

CREATE TABLE IF NOT EXISTS public.tasks
(
    id integer NOT NULL DEFAULT nextval('tasks_id_seq'::regclass),
    title character varying(256) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    deadline date,
    status character varying(50) COLLATE pg_catalog."default",
    created_by_user integer NOT NULL,
    CONSTRAINT tasks_pkey PRIMARY KEY (id),
    CONSTRAINT tasks_title_key UNIQUE (title),
    CONSTRAINT tasks_user_id_fkey FOREIGN KEY (created_by_user)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tasks
    OWNER to postgres;
-- Index: idx_tasks_status_hash

-- DROP INDEX IF EXISTS public.idx_tasks_status_hash;

CREATE INDEX IF NOT EXISTS idx_tasks_status_hash
    ON public.tasks USING hash
    (status COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Trigger: log_task_status_trigger

-- DROP TRIGGER IF EXISTS log_task_status_trigger ON public.tasks;

CREATE TRIGGER log_task_status_trigger
    AFTER INSERT
    ON public.tasks
    FOR EACH ROW
    EXECUTE FUNCTION public.log_task_status();

-- Trigger: status_update_trigger

-- DROP TRIGGER IF EXISTS status_update_trigger ON public.tasks;

CREATE TRIGGER status_update_trigger
    AFTER UPDATE OF status
    ON public.tasks
    FOR EACH ROW
    EXECUTE FUNCTION public.update_task_progress();

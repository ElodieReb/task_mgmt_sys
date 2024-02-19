-- Table: public.task_assignees

-- DROP TABLE IF EXISTS public.task_assignees;

CREATE TABLE IF NOT EXISTS public.task_assignees
(
    user_id integer NOT NULL,
    task_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT task_assignees_pkey PRIMARY KEY (user_id, task_id),
    CONSTRAINT task_assignees_task_id_fkey FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT task_assignees_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.task_assignees
    OWNER to postgres;
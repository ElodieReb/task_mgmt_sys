# Task Management Database

## Description

This database allows for the creation of new users, tasks, and the assignment of tasks to a user. Additional functionality includes the ability to track a task's status as it is updated, creating the potential for productivity analysis. 

## API Reference Table of Endpoint Paths, Methods, Parameters

| Endpoint Path | Methods | Parameters | Description |
| --- | --- | --- | --- |
| `/tasks` | GET | None | Retrieves all tasks. |
| `/tasks/<int:id>` | GET | `id` (Task ID) | Retrieves information for a specific task. |
| `/tasks` | POST | `created_by_user` (User ID), `title`, `description`, `deadline`, `status` | Creates a new task. |
| `/tasks/<int:id>` | PATCH, PUT | `id` (Task ID), `title`, `description`, `deadline`, `status` | Updates information for a specific task. |
| `/tasks/<int:id>` | DELETE | `id` (Task ID) | Deletes a specific task. |
| `/tasks/<int:id>/assign_to/<int:user_id>` | POST | `id` (Task ID), `user_id` (User ID) | Assigns a task to a user. |
| `/tasks/<int:id>/users_assigned_task` | GET | `id` (Task ID) | Retrieves users assigned to a specific task. |
| `/tasks/<int:id>/unassign_user/<int:user_id>` | PATCH, PUT | `id` (Task ID), `user_id` (User ID) | Unassigns a user from a specific task. |
| `/users` | GET | None | Retrieves all users. |
| `/users/<int:id>` | GET | `id` (User ID) | Retrieves information for a specific user. |
| `/users` | POST | `username`, `email`, `password` | Creates a new user. |
| `/users/<int:id>` | DELETE | `id` (User ID) | Deletes a specific user. |
| `/users/<int:id>` | PATCH, PUT | `id` (User ID), `username`, `email`, `password` | Updates information for a specific user. |
| `/users/<int:id>/tasks_assigned` | GET | `id` (User ID) | Retrieves tasks assigned to a specific user. |

## Other Information

<i> How did the project's design evolve over time? </i>

* At the inception of this project, I had thought to create one more table than is included in the final implementation, namely, a "task_categories" table. This table would have made the database slightly more advanced in that it would offer the functionality of grouping tasks by category. I ultimately decided against implementing this table due to the time constraint I had while working on this project. Additionally, as I began working on the migration file I realized that only two classes, Task and User, had to be created when in reality there are four tables in the database and I had initially thought this would translate to four classes. The reason for this is that the "task_assignees" table is merely an association table that links tasks and users in a many-to-many relationship and the "task_logs table" is an auxiliary table, therefore, neither table needed to be declared as its own class. 

<i> Did you choose to use an ORM or raw SQL? Why? </i>

* I chose the ORM approach. The main advantages of doing so as opposed to the raw SQL approach are as follows: (1) The ORM approach abstracts away the low-level details of database interactions. You work with high-level objects and classes, making your code more focused on business logic rather than SQL syntax. (2) The raw SQL approach requires manual creation and management of database schemas, whereas the ORM approach can automatically create database tables based on my model classes, simplifying the database setup process. (3) I ultimately felt that the ORM approach allowed for better management of the relationships between entities in my database as using raw SQL would have required explicit management of relationships using foreign keys and joins, which is not as practical in practice in an enterprise setting.

* The only times I used raw SQL in the project were in the implementation of a trigger, meant to update the task_logs table each time the status of a task is changed (essential data in tracking productivity/for future application in estimating how long it takes for a task to reach completion), and also in the implementation of an index on task status in the "tasks" table. I chose to implement a hash index in this case as I felt it would be more advantageous than a B-tree index for this data set in particular.

<i> What future improvements are in store, if any? </i>

* If I were to revist this project, I would continue to add functionality to my database by creating the "task_categories" table, as described earlier, in addition to other features such as providing an estimate for the amount of time a task will take to reach completion based on calculated trends from data stored in the task_logs table. 

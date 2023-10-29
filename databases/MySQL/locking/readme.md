record locks on a live system:

create a new schema if doesn't exist - performance_watch

create database performance_watch;

remember to run "use performance_watch;" for all subsequent commands.

create tables:
lock_watcher from file - table.lock_watcher.sql
map_locks from file - table.map_locks.sql

create a procedure:
record_lock_info from file - proc.record_lock_info.sql

create an event to run this procedure every 15s:
record_locks from file - event.record_locks.sql

scheduler system may not be enabled. 
to enable it run:
SET GLOBAL event_scheduler = ON;

the event is created disabled. To enable it run:
alter event record_locks enable;

when you want to stop collecting information, disable it again:
alter event record_locks disable;	
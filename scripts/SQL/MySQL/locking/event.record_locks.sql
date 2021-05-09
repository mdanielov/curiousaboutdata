use performance_watch;
CREATE  EVENT `record_locks` 
	ON SCHEDULE EVERY 15 SECOND 
	DISABLE DO call record_lock_info()
	
# alter event record_locks enable;
# alter event record_locks disable;	
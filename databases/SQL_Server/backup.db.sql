DECLARE @DatePrefix NVARCHAR(13),
@baseDir NVARCHAR(255) = 'C:\Users\Admin\archive\databases\',
@databaseName NVARCHAR(255) = 'MyDB',
@mediaName NVARCHAR(255),
@backupName NVARCHAR(255),
@backupPath NVARCHAR(255);

SET @DatePrefix = FORMAT(GETDATE(), 'yyyy.MM.dd.HH');
set @mediaName = @databaseName + ' backup before delete';
set @backupName = @databaseName + '-Full Database Backup';
set @backupPath = @baseDir + @DatePrefix + '-'+ @databaseName   + '.bak';

BACKUP DATABASE @databaseName TO  DISK = @backupPath 
WITH FORMAT, INIT,  MEDIANAME = @mediaName,  
NAME = @backupName, SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10
GO

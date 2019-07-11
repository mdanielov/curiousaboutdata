$ServerName = "NEZIKIN01\SHVUOT"  
$path = "F:\tmp\funk"

 
[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.SqlServer.SMO')
$serverInstance = New-Object ('Microsoft.SqlServer.Management.Smo.Server') $ServerName
$IncludeTypes = @("Tables","StoredProcedures","Views","Triggers","Functions") #object you want do backup. 
$ExcludeSchemas = @("sys","Information_Schema")
$so = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')

 
$dbs=$serverInstance.Databases


#right now this is limited to one DB. 
#if you want all of them just remove the condition
$db = $dbs | ?{$_.Name -eq "msdb"}

        
echo "********************************************"
       

$dbname = "$db".replace("[","").replace("]","")

$dbpath = "$path"+ "\"+"$dbname" + "\"

echo "Working on $dbname"


if ( !(Test-Path $dbpath))
   {$null=new-item -type directory -name "$dbname"-path "$path"}
     foreach ($Type in $IncludeTypes)
       {
              $objpath = "$dbpath" + "$Type" + "\"
              
         if ( !(Test-Path $objpath))
           {$null=new-item -type directory -name "$Type"-path "$dbpath"}
           #special consideration for functions
		   if ($Type -eq "Functions") {$Type = "UserDefinedFunctions"}
              foreach ($objs in $db.$Type)
              {
             
              
                     If ($ExcludeSchemas -notcontains $objs.Schema ) 
                      {
                           $ObjName = "$objs".replace("[","").replace("]","").Replace("?","")                  
                           $OutFile = "$objpath" + "$ObjName" + ".sql"
                           write-host "working on $ObjName -- $OutFile"
                           $objs.Script($so)+"GO" | out-File $OutFile
                      }
              }
       }    	   
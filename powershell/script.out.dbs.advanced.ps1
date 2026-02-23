$ServerName = "database server name"  
$path = "C:\...\scripts"
$database_name="myData"

 
[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.SqlServer.SMO') | Out-Null
$serverInstance = New-Object ('Microsoft.SqlServer.Management.Smo.Server') $ServerName
#$IncludeTypes = @("Tables","StoredProcedures","Views","Triggers","Functions") #object you want do backup. 
$ExcludeSchemas = @("sys","Information_Schema")
$so = new-object ('Microsoft.SqlServer.Management.Smo.ScriptingOptions')

$so.DriDefaults = $false
$so.AnsiPadding = $false
$so.AllowSystemObjects =$false
$so.NoCollation = $true
$so.DriAllKeys = $true
$so.DriAllConstraints = $true

$so.Triggers = $true
$so.DriChecks = $true
$so.Indexes = $true
 
$dbs=$serverInstance.Databases


#right now this is limited to one DB. 
#if you want all of them just remove the condition
$db = $dbs | ?{$_.Name -eq $database_name}

        
echo "********************************************"
       

$dbname = "$db".replace("[","").replace("]","")

$dbpath = "$path"+ "\"+"$dbname" + "\"

echo "Working on $dbname"
$schemas = $db.Schemas |  ?{$_.IsSystemObject -eq $false -or $_.Name -eq "dbo"} | Select Name

# create new db folder if doesn't exist
if ( !(Test-Path $dbpath)) {$null=new-item -type directory -name "$dbname"-path "$path"}

foreach ($schema in $schemas){
$sch=$schema.Name.Replace('\','_').Replace('.','_')

$db_and_schema_path = "$dbpath" + "$sch" + "\"

Write-Host "working on $sch schema $db_and_schema_path"

#create schema folder if doesn't exist
if ( !(Test-Path $db_and_schema_path)){$null=new-item -type directory -name "$sch"-path "$dbpath"}

     foreach ($Type in (
     ($db | Get-Member -MemberType Property | Where-Object { $_.Definition -match 'Collection' } | ForEach-Object {
        $nm = $_.Name
        if ($db.$nm.GetType().BaseType -match "SchemaCollectionBase") { $nm }
    } 2> $null )))
       {
              $cnt =0
              write-host "working on $Type type"
              $objpath = "$db_and_schema_path" + "$Type" + "\"
              $cnt = $db.$Type | ?{$_.schema -eq $sch -and $_.IsSystemObject -eq $false} | measure-object | %{$_.count}
              Write-Host "found $cnt objects"
              if ($cnt -gt 0){
              
         if ( !(Test-Path $objpath))
           {$null=new-item -type directory -name "$Type"-path "$db_and_schema_path"}
           #special consideration for functions
		   if ($Type -eq "Functions") {$Type = "UserDefinedFunctions"}
              foreach ($objs in $db.$Type | ?{$_.schema -eq $sch -and $_.IsSystemObject -eq $false}) 
              {
                     If ($ExcludeSchemas -notcontains $objs.Schema ) 
                      {
                           $ObjName = "$objs".replace("[","").replace("]","").Replace("?","")                  
                           $OutFile = "$objpath" + "$ObjName" + ".sql"
                           write-host "working on $ObjName -- $OutFile"
                           $objs.Script($so)+"GO" | out-File $OutFile
                      }
              } #object

           } # non-empty type
       } #type    	   
  } # schema
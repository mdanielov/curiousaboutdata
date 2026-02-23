param(
    [string] $Server_addr = "127.0.0.1",
    [string] $db_name = "KiMeTzion",
    [string] $User = "",
    [string] $Pwd = "",
    [string] $T = "",
	[string] $M = "dbo",
	[string] $f = "f:\workspace"
    )
    
function ScriptOut-DBObject {
      param ($objecttype, $relpath, $objects)
      
	  $dirpath = $filepath + "\" + $relpath
	  New-Item $dirpath -type directory -force | out-null
      $listfilepath = ("{0}\@{1}_{2}.txt" -f $logpath, $objecttype, $timestamp)
      
      If ($objects.Length -ne $null) {
            $count = $objects.Length[0]
      } else { # for example: $objecttype = default
            $count = $objects.Count
      }

      for ($i=0; $i -lt $count; $i++) {
            $object = $objects[$i]
            Write-Host ($object.Name).Replace('\', '_').Replace('/', '-').Replace("'", '-')
            if ($object.DateLastModified -ne $null) {
                  $objectdate = $object.DateLastModified
            } else { # for example: $objecttype = default
                  $objectdate = $object.CreateDate
            }
            $logentry = "{0}`t{1}`t{2}" -f $objectdate.ToString("yyyy-MM-dd HH:mm:ss"), $objecttype, $object.Name
            Write-Host ("[{0} of {1}]`t{2}" -f ($i+1), $count, $logentry)
            echo $logentry | Out-File -encoding utf8 -force -append -FilePath $listfilepath
	 		$fullfilepath = "{0}\{1}.sql" -f $dirpath, ($object.Name).Replace('\', '_').Replace('/', '-').Replace("'", '-')  #, $objecttype
			$output = $object.script($scrp.Options)
            #Write-Host $output[2..($output.count)]

			if ($objecttype -match "\btable\b") {
				$output[2..($output.count)] | Out-File -encoding utf8 -force -FilePath $fullfilepath
			} elseif ($objecttype -match "\b(view|proc|function)\b") {
				$output[2..($output.count)] | Out-File -encoding utf8 -force -FilePath $fullfilepath
			} else {
				$output[2..($output.count)] | Out-File -encoding utf8 -force -FilePath $fullfilepath
			}
      }
    }



function delete-dir {
param ($fpath)
if (Test-Path $fpath){
Remove-Item $fpath -Recurse -Force | out-null
}
}

# load assemblies
[Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.Smo") | out-null

$filepath = $f + "\" + $Server_addr + "\" + $db_name
New-Item $filepath -type directory -force | out-null
$timestamp = (Get-Date).ToString("yyyyMMddHHmmss")
$logpath = $f + "\" + $Server_addr + "\" + $db_name + "_logs"
New-Item $logpath -type directory -force | out-null

$server = New-Object Microsoft.SqlServer.Management.Smo.Server $Server_addr
$scrp = New-Object Microsoft.SqlServer.Management.Smo.Scripter $server

if ($User -and $Pwd){
    $server.ConnectionContext.LoginSecure = $false
    $server.ConnectionContext.set_Login($User)
    $server.ConnectionContext.set_Password($Pwd)
}
else{
    $server.ConnectionContext.LoginSecure=$true
}

$server.ConnectionContext.Connect()

$dbs = $server.Databases
$scrp.Options.DriDefaults = $false
$scrp.Options.AnsiPadding = $false
$scrp.Options.AllowSystemObjects =$false
$scrp.Options.NoCollation = $true
$scrp.Options.DriAllKeys = $true
$scrp.Options.DriAllConstraints = $true

$scrp.Options.Triggers = $true
$scrp.Options.DriChecks = $true
$scrp.Options.Indexes = $true




function format-scripted-file{
param($object)
$object.script($scrp.Options)
$og_script = $dbs[$db_name].StoredProcedures[0].Script($scrp.Options)
$formatted_script = @() + $og_array -ne 'SET ANSI_NULLS ON' -ne  'SET QUOTED_IDENTIFIER ON'
Write-Host $formatted_script
}

if ($M){
    $schemas = @($M)
}
else{
    $schemas = $dbs[$db_name].Schemas |  ?{$_.IsSystemObject -eq $false -or $_.Name -eq "dbo"} | Select Name
    if (-not $schemas.Contains('dbo')){
        $schemas += 'dbo'
    }
}

foreach ($schema in $schemas){

if ($schema.GetType().Name -eq 'String'){
    $sch = $schema}
else {
    $sch = $schema.Name
    }

$sch = $sch.trim() 

#tables
    if ($T -match "^$|\btbl\b") {
	    $tables = ($dbs[$db_name].Tables | where {$_.IsSystemObject -eq $false -and $_.Schema -eq $sch })
	
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_') +"\Tables"), "table")
        write-host "starting to script schema $sch"
	    ScriptOut-DBObject "table" ($sch.Replace('\', '-').Replace('/', '-').Replace("'", '-') +"\Tables") $tables
    }


    if ($T -match "^$|\bzzz\b") {
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\Defaults"), "default")
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\User Defined Types"), "udtt")
	    ScriptOut-DBObject "default" ($sch.Replace('\', '_')+"\Defaults") ($dbs[$db_name].Defaults | where {$_.Schema -eq $sch})
    
	    if ($dbs[$db_name].UserDefinedTableTypes  -ne $null)
       {
            delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\UserDefinedTypes"), "udt")
            ScriptOut-DBObject "udtt" ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\User Defined Types") ($dbs[$db_name].UserDefinedTableTypes | where {$_.Schema -eq $sch})
           }
       
    }

    if ($T -match "^$|\bufn\b") {
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\Functions"), "function")
	    ScriptOut-DBObject "function" ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\Functions") ($dbs[$db_name].UserDefinedFunctions | where {$_.IsSystemObject -eq $false -and $_.Schema -eq $sch})
    }

    if ($T -match "^$|\busp\b") {
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_')+"\Stored Procedures"), "proc") 
	    ScriptOut-DBObject "proc" ($sch.Replace('\', '_')+"\Stored Procedures") ($dbs[$db_name].StoredProcedures | where {$_.IsSystemObject -eq $false -and $_.Schema -eq $sch})
    }

    if ($T -match "^$|\bviw\b") {
        delete-dir ("{0}\{1}\*.{2}.sql" -f $filepath, ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\Views"), "view")
	    ScriptOut-DBObject "view" ($sch.Replace('\', '_').Replace('/', '-').Replace("'", '-')+"\Views") ($dbs[$db_name].Views | where {$_.IsSystemObject -eq $false -and $_.Schema -eq $sch})
    }

}

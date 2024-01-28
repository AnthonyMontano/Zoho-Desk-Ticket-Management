$offboarddata = Get-Content -Raw -Path "C:\\Users\\anthonym\\Zoho\\env\\Scripts\\Zoho-Desk-Ticket-Management\\Config Files\\OpenOffboardsData.json"
$offboardinfo = $offboarddata | ConvertFrom-Json 

# Create an array to store offboard objects
$offboardObjects = @()
   
    foreach ($offboard in $offboardinfo) {
        # Create a custom object for each offboard entry
        $offboardObject = $offboard | Select-Object @{
            Name = 'Ticket Number'; Expression = { $_.'Ticket Number' }
        }, @{
            Name = 'Ticket ID' ; Expression = { $_.'Ticket ID'  }
        }, @{
            Name = 'Employee Name'; Expression = { $_.'Employee Name' }
        }, @{
            Name = 'Employee Location' ; Expression = { $_.'Employee Location'  }
        }, @{
            Name = 'Title' ; Expression = { $_.'Title'  }
        }, @{
            Name = 'Associate ID' ; Expression = { $_.'Associate ID'  }
        }, @{
            Name = 'Department'; Expression = { $_.'Department'}
        }, @{
            Name = 'Email Forwarding' ; Expression = { $_.'Email Forwarding' }
        }, @{
            Name = 'Term Time' ; Expression = { $_.'Term Time' }
        }, @{
            Name = 'Term Date' ; Expression = { $_.'Term Date' }
        }

    # Add the object to the array
    $offboardObjects += $offboardObject
}

# Now you have an array of custom objects representing each offboard entry
# You can perform actions on each object in the array
foreach ($obj in $offboardObjects) {
    # Example: Print information about each offboard entry
    #Write-Host "Processing offboard for User: $($obj.'Term Date'),$($obj.'Term Time'),$($obj.'Employee Name'), $($obj.'Ticket Number'), $($obj.'Ticket ID'), $($obj."Department"), $($obj.'Employee Location'), $($obj."Title"), Department: $($obj."Department")"
    $TermDate = $obj."Term Date"
    $termTime = $obj."Term Time"
    $termTicket = $obj."Ticket Number"
    $timenoon = "AM 9-12noon"
    $timeevening = "PM 12-6pm" 
    $Month = $TermDate.Substring(0,2)
    $Day = $TermDate.Substring(3,2)
    $Year = "20" + $TermDate.Substring(6,2)
    $tasktimenoon = $Year + "-" + $Month + "-" + $Day + " " + "12:00:00"
    $tasktimeevening = $Year + "-" + $Month + "-" + $Day + " " + "05:00:00"
    #$tasktimenoon = "2024" + "-" + "01" + "-" + "22" + " " + "19:59:00"
    #$tasktimeevening = "2024" + "-" + "01" + "-" + "22" + " " + "19:59:00"
    
    if ($termTime -eq $timenoon){
        $tasktime = $tasktimenoon
    }
    elseif($termTime -eq $timeevening){
        $tasktime = $tasktimeevening
    }
    else{
        Write-Host "This is unprecedented"
    }
    
 
    $actions = (New-ScheduledTaskAction -Execute 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -Argument '-file "C:\users\Anthony\Zoho\Scripts\Cloned-Repo\Zoho-Desk-Ticket-Management\HelloWorld.Ps1"')
    $trigger = New-ScheduledTaskTrigger -Once -At $tasktime
    $principal = New-ScheduledTaskPrincipal -UserId 'NT AUTHORITY\SYSTEM' -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -WakeToRun
    $task = New-ScheduledTask -Action $actions -Principal $principal -Trigger $trigger -Settings $settings
    Register-ScheduledTask -TaskName $termTicket -InputObject $task
    Write-Host "Scheduled"

}
$pythonScriptPath = "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Ps1toZohoReporter.py"

# Run the Python script using Start-Process
Start-Process python -ArgumentList $pythonScriptPath -NoNewWindow -Wait
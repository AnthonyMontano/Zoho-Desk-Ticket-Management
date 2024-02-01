if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
     $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
     Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine
     Exit
    }
    
   }
$jsonFilePath = "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Config Files\OpenOffboardsData.json" 
$offboarddata = Get-Content -Path "C:\\Users\\anthonym\\Zoho\\env\\Scripts\\Zoho-Desk-Ticket-Management\\Config Files\\OpenOffboardsData.json" | Out-String | ConvertFrom-Json
# Create an array to store offboard objects

    foreach ($offboard in $offboarddata) {
        Write-Host $offboard."Prep Status"
        Write-Host $offboard
        if($offboard."Prep Status" -eq ""){
        $offboard."Prep Status" = "Ready"
        
        }

    # Add the object to the array
    #$offboardObjects += $offboardObject
    $updatedJsonData = $offboarddata | ConvertTo-Json -Depth 10
    $updatedJsonData | Set-Content -Path $jsonFilePath
}

$pythonScriptPath = "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Ps1toZohoReporter.py"

# Run the Python script using Start-Process
Start-Process python -ArgumentList $pythonScriptPath -NoNewWindow -Wait
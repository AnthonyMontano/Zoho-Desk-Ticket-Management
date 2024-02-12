


$ConfirmPreference = "None"

$offboarddata = Get-Content -Path "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json" -Raw | ConvertFrom-Json
$jsonFilePath = "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Config Files\OpenOffboardsData.json" 
    
    # Create an array to store offboard objects
$offboardObjects = @($offboarddata)
       
    <#foreach ($offboard in $offboardObjects) {
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
        }, @{
            Name = 'Employee Email' ; Expression = { $_.'Employee Email'  }
        }, @{
            Name = 'Prep Status' ; Expression = { $_.'Prep Status' }
        }, @{
            Name = 'Supervisor Name' ; Expression = { $_.'Supervisor Name' }
        }, @{
            Name = 'Email Forwarding Address' ; Expression = { $_.'Email Forwarding Address'  }
        }
        # Ad
        # Add the object to the array
        $offboardObjects += $offboardObject
}#>



function GraphSignin {
    $ApplicationId = [Environment]::GetEnvironmentVariable('ApplicationID', 'Machine')       
    $SecuredPassword = [Environment]::GetEnvironmentVariable('SecurePassword', 'Machine')   
    $tenantID = [Environment]::GetEnvironmentVariable('TenantID', 'Machine')  
    $SecuredPasswordPassword = ConvertTo-SecureString `
    -String $SecuredPassword -AsPlainText -Force
    $ClientSecretCredential = New-Object `
    -TypeName System.Management.Automation.PSCredential `
    -ArgumentList $ApplicationId, $SecuredPasswordPassword
    Connect-MgGraph -TenantId $tenantID -ClientSecretCredential $ClientSecretCredential
    Write-Host "Graph Signed in"
    }

function EXOSignIn {
# Connect to Exchange Online
$CertThumbPrint = [System.Environment]::GetEnvironmentVariable('CertThumbPrint','Machine')
$AppID = [System.Environment]::GetEnvironmentVariable('ApplicationID', 'Machine') 
$Org = "alliedstoneinc.com"
Connect-ExchangeOnline -CertificateThumbPrint $CertThumbPrint -AppID $AppID -Organization $Org 
#$mycert = New-SelfSignedCertificate -DnsName "alliedstoneinc.com" -CertStoreLocation "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Config Files" -NotAfter (Get-Date).AddYears(1) -KeySpec KeyExchange
 
 # Export certificate to .pfx file
# $mycert | Export-PfxCertificate -FilePath mycert.pfx -Password (Get-Credential).password

 # Export certificate to .cer file
# $mycert | Export-Certificate -FilePath mycert.cer 
}

#1. Block Sign in on users account
function BlockSignIn{
    $params = @{
        AccountEnabled = $false
            }
    update-mguser -Userid $Employeeemail -BodyParameter $params
    Write-Host "$Employeeemail used in Block Sign in"
    }


#2. Sign out of all sessions
function Signoutofallsessions { 
    Write-Host "$Employeeemail used in sign out of all sessions in"
    Revoke-MgUserSignInSession -UserId $Employeeemail
}

#3a. Remove from all Distro Lists
function RemoveUserfromDistroLists{
    Write-Host "Removing $Employeeemail from distro lists"
    $Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id
    foreach ($i in $Groups.Id){

        # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
        Remove-DistributionGroupMember -Identity $i -Member $Employeeemail -Confirm:$false -ErrorAction SilentlyContinue
        Write-Output "Removing $Employeeemail from the $i Distro List"
    
    
    }
    Start-Sleep -Seconds 20
}

#3b. Remove from all Active Directory Groups
function RemoveUsersfromADGroups {
        Write-Host "$Employeeemail for removing users from AD groups"
        try {
            $samaccountname = Get-ADUser -Filter {UserPrincipalName -eq $Employeeemail} -Properties samaccountname -ErrorAction Stop
            $groupMembership = $samaccountname | Get-ADPrincipalGroupMembership | Where-Object -Property Name -ne -Value "Domain Users"
            foreach ($group in $groupMembership){
                Write-Host "Removing $($samaccountname.SamAccountName) from $($group.name)"-ForegroundColor Cyan
                Remove-ADGroupMember -Identity $group -Members $samaccountname
                } 
            
            
        }
        catch {
            Write-Host "User Principal Name does not exist, please wait 5 seconds" -ForegroundColor Red
            Start-Sleep -Seconds 5
        }    
}

#3b. Remove user from Azure AD Groups
function RemoveUserFromAzureADGroups{
    Write-Host "$Employeeemail for removing users from azure AD groups"
    $employeeidpull = Get-mguser -Userid $Employeeemail -property id | Select-Object id
    $employeeid = $employeeidpull.Id
    $Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id
    foreach ($i in $Groups.Id){

        
        Remove-MgGroupMemberByRef -GroupId $i -DirectoryObjectId $employeeid -ea SilentlyContinue
        Write-Output "Removing $Employeeemail from the $i"
    }
}

function DisableUserandmovetoOU  {

    $deletedusersou = "OU=Disabled Users,OU=Users,OU=ORG,OU=AzureDataCenter,DC=alliedstoneinc,DC=com"
    $user = Get-ADUser -SearchBase "OU=Users,OU=ORG,OU=AzureDataCenter,DC=alliedstoneinc,DC=com" -SearchScope Subtree -Filter {UserPrincipalName -eq $Employeeemail}
    
    if ($user) {
        if (($user.Enabled -eq $true) -and ($user.DistinguishedName -notlike "*$deletedusersou*")) {
            $user | Disable-ADAccount
            Move-ADObject -Identity $user.DistinguishedName -TargetPath $deletedusersou
            Write-Host "$Employeeemail has been disabled and moved to the Deleted Users OU" -ForegroundColor Green
        }
        elseif (($user.Enabled -eq $true) -and ($user.DistinguishedName -like "*$deletedusersou*")) {
            $user | Disable-ADAccount
            Write-Host "$Employeeemail has been disabled and is already in the Deleted Users OU" -ForegroundColor Green
        } 
        elseif (($user.enabled -eq $false) -and ($user.DistinguishedName -notlike "*$deletedusersou*")) {
            Move-ADObject -Identity $user.DistinguishedName -TargetPath $deletedusersou
            Write-Host "$Employeeemail is already disabled and has been moved to Deleted Users OU." -ForegroundColor Green
        }
        elseif (($user.enabled -eq $false) -and ($user.DistinguishedName -like "*$deletedusersou*")) {
            Write-Host "$Employeeemail is already disabled and is already in the Disabled Users OU" -ForegroundColor Green
        }} 
        else {
        Write-Host "$Employeeemail does not exist." -ForegroundColor Red
    }
}

#7.Email forwarding 
function SetForwardingEmail{
    if($null -eq $EmailForwardingAddress){
        Write-Host "No Email Forwarding Requested"
    }
    elseif($null -ne $EmailForwardingAddress ){
        Set-Mailbox $Employeeemail –ForwardingSmtpAddress $supervisoremail  –DeliverToMailboxAndForward $false
    }
    else{
        Write-Host "Field was left blank so assuming No email forwarding wanted"
    }
}

#4a. Mark user as "Termed" in Local AD
function MarkUserTermedOnprem {
    $samaccountname = Get-ADUser -Filter {UserPrincipalName -eq $Employeeemail} -Properties samaccountname -ErrorAction Stop
    
    Set-ADuser $samaccountname -Title "Termed" -Office $EmployeeLocation 
    Write-Host "$Employeeemail is this for MarkUserTermedOnprem"
}

#4b. Mark user as "Termed" in Azure AD
function MarkUserTermedinAzure{
    $params = @{
        jobTitle = "Termed"  
    }
    # A UPN can also be used as -UserId.
    Update-MgUser -UserId $Employeeemail -BodyParameter $params
}

#8. Reporting back to Zoho
function RunReportingScript{
    
}




#Start of tree of actions
GraphSignin
EXOSignIn

foreach($obj in $offboardObjects){
    $Employeeemail = $obj."Employee Email"
    $EmailForwarding = $obj."Email Forwarding"
    $EmailForwardingDuration = $obj."Email Forwarding Duration"
    $TicketNumber = $obj."Ticket Number"
    $EmailForwardingAddress = $obj."Email Forwarding Address"
    $PrepState = $obj."Prep Status"
    $TermDate = $obj."Term Date"
    $termTime = $obj."Term Time"
    $supervisorname = $obj."Supervisor Name"
    $supervisoremail = $obj."Email Forwarding Address"
    $EmployeeLocation = $obj."Employee Location"
    $timenoon = "AM 9-12noon"
    $timeevening = "PM 12-6pm"
    $Month = $TermDate.Substring(0,2)
    $Day = $TermDate.Substring(3,2)
    $Year = "20" + $TermDate.Substring(6,2)
    $tasktimenoon = $Year + "-" + $Month + "-" + $Day + " " + "12:00:00"
    $tasktimeevening = $Year + "-" + $Month + "-" + $Day + " " + "17:00:00"
    
    if ($termTime -eq $timenoon){
        $tasktime = $tasktimenoon
    }
    elseif($termTime -eq $timeevening){
        $tasktime = $tasktimeevening
    }
    else{
        Write-Host "This is unprecedented"
    }

    if((Get-date $tasktime) -lt (get-Date)){
        
        $syncstatus = get-mguser -Userid $Employeeemail -Property OnPremisesSyncEnabled | Select-Object OnPremisesSyncEnabled
        if ($PrepState -eq "Ready"){
            if ($syncstatus.OnPremisesSyncEnabled -eq "True"){
                $obj.'Prep Status' = "Executed"        
                Write-Host "Synced to On Prem"    
                BlockSignIn
                Signoutofallsessions
                MarkUserTermedOnprem
                SetForwardingEmail
                RemoveUserfromDistroLists
                RemoveUsersfromADGroups
                DisableUserandmovetoOU
                RemoveUserFromAzureADGroups
                
                    
                }
            elseif($null -eq $syncstatus.OnPremisesSyncEnabled){
                $obj.'Prep Status' = "Executed"      
                Write-Host "Not Synced to On Prem"
                BlockSignIn
                Signoutofallsessions
                MarkUserTermedinAzure
                #SetForwardingEmail
                RemoveUserfromDistroLists
                RemoveUserFromAzureADGroups
                     

                }
            else {
                Write-Host "Something unprecedented has occured"
                exit
        }

    }
    }
$updatedJsonData = ConvertTo-Json @($offboardObjects) -Depth 10 | Set-Content -Path $jsonFilePath

$updatedJsonData
}

$pythonScriptPath = "C:\Users\anthonym\Zoho\env\Scripts\Zoho-Desk-Ticket-Management\Ps1toZohoReporter.py"

# Run the Python script using Start-Process
Start-Process python -ArgumentList $pythonScriptPath -NoNewWindow -Wait


function GetData{
    $offboarddata = Get-Content -Raw -Path "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json"
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
            }, @{
                Name = 'Employee Email' ; Expression = { $_.'Employee Email'  }
            }
        # Add the object to the array
        $offboardObjects += $offboardObject
}
}

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
    }


#2. Sign out of all sessions
function Signoutofallsessions { 
    Revoke-MgUserSignInSession -UserId $Employeeemail
}

#3a. Remove from all Distro Lists
function RemoveUserfromDistroLists{
    $Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id
    foreach ($i in $Groups.Id){

        # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
        Remove-DistributionGroupMember -Identity $i -Member $Employeeemail
        Write-Output "Removing $Employeeemail from the $i"
    
    
    }
}

#3b. Remove from all Active Directory Groups
function RemoveUsersfromADGroups {

        try {
            $samaccountname = Get-ADUser -Filter {UserPrincipalName -eq $Employeeemail} -Properties samaccountname -ErrorAction Stop
            $groupMembership = $samaccountname | Get-ADPrincipalGroupMembership | Where-Object -Property Name -ne -Value "Domain Users"
            foreach ($group in $groupMembership){
                Write-Host "Removing $($samaccountname.SamAccountName) from $($group.name)"-ForegroundColor Cyan
                } 
            $groupMembership | Where-Object -Property name -ne -value "Domain Users" | Remove-ADGroupMember -members $samaccountname -Confirm:$false -ErrorAction Stop
            
        }
        catch {
            Write-Host "User Principal Name does not exist, please wait 5 seconds" -ForegroundColor Red
            Start-Sleep -Seconds 5
        }    
}

#3b. Remove user from Azure AD Groups
function RemoveUserFromAzureADGroups{
    $employeeidpull = Get-mguser -Userid noahg@alliedstoneinc.com -property id | Select-Object id
    $employeeid = $employeeidpull.Id
    $Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id
    foreach ($i in $Groups.Id){

        
        Remove-MgGroupMemberByRef -GroupId $i -Member $employeeid
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

#
function RemoveUserfromDistroLists{
    $Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id
    foreach ($i in $Groups.Id){

        # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
        Remove-DistributionGroupMember -Identity $i -Member $Employeeemail
        Write-Output "Removing $Employeeemail from the $i"
    
    
    }
}


#7.Email forwarding 
function SetForwardingEmail{
    if($EmailForwarding -eq "No"){
        Write-Host "No Email Forwarding Requested"
    }
    elseif($EmailForwarding -eq "Yes"){
        Set-Mailbox $Employeeemail –ForwardingSmtpAddress $supervisoremail  –DeliverToMailboxAndForward $false
    }
    else{
        Write-Host "Field was left blank so assuming No email forwarding wanted"
    }
}

#4a. Mark user as "Termed" in Local AD
function MarkUserTermedOnprem {
    $samaccountname = Get-ADUser -Filter {UserPrincipalName -eq $Employeeemail} -Properties samaccountname -ErrorAction Stop
    Set-ADuser $samaccountname -Title "Termed" 
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
function ExcecuteFlow{
    GetData
    foreach($obj in $offboardObjects){
        $Employeeemail = $obj."Employee Email"
        $EmailForwarding = $obj."Email Forwarding"
        $EmailForwardingDuration = $obj."Email Forwarding Duration"
        $TicketNumber = $obj."Ticket Number"
        $EmailForwardingAddress = $obj."Email Forwarding Address"
        Write-Host $Employeeemail
        Write-Host $EmailForwarding
        Write-Host $EmailForwardingDuration
        Write-Host $TicketNumber
        Write-Host $EmailForwardingAddress
        
        $syncstatus = get-mguser -Userid $Employeeemail -Property OnPremisesSyncEnabled

        if ($syncstatus.OnPremisesSyncEnabled -eq "true"){
            
            GraphSignin
            EXOSignIn
            BlockSignIn
            Signoutofallsessions
            MarkUserTermedOnprem
            SetForwardingEmail
            RemoveUsersfromADGroups
            RemoveUserfromDistroLists
            RemoveUserFromAzureADGroups
            RunReportingScript
            
                    
            
                    
        }
        elseif($syncstatus.OnPremisesSyncEnabled -eq "false"){
            
            GraphSignin
            EXOSignIn
            BlockSignIn
            Signoutofallsessions
            MarkUserTermedinAzure
            SetForwardingEmail
            RemoveUserfromDistroLists
            RemoveUserFromAzureADGroups
            RunReportingScript
            
        }
        else {
            Write-Host "Something unprecedented has occured"
        }
    }
}
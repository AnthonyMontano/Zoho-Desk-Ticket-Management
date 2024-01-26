function GraphSignin {
    $ApplicationId = [Environment]::GetEnvironmentVariable('APPLICATIONID', 'Machine')       
    $SecuredPassword = [Environment]::GetEnvironmentVariable('SECUREPASSWORD', 'Machine')   
    $tenantID = [Environment]::GetEnvironmentVariable('TENANTID', 'Machine')  
    $SecuredPasswordPassword = ConvertTo-SecureString `
    -String $SecuredPassword -AsPlainText -Force
    $ClientSecretCredential = New-Object `
    -TypeName System.Management.Automation.PSCredential `
    -ArgumentList $ApplicationId, $SecuredPasswordPassword
    Connect-MgGraph -TenantId $tenantID -ClientSecretCredential $ClientSecretCredential
    }

function EXOSignIn {
# Connect to Exchange Online
$CertThumbPrint = ""
$AppID = ""
$Org = ""

Connect-ExchangeOnline -CertificateThumbPrint $CertThumbPrint -AppID $AppID -Organization $Org    
}    




# Just checking to see what is possible with all this code
$Employeeemail = "ENTEREMAILHERE"
$userobject = get-mguser -Userid $Employeeemail -Property Id
$userobjectstr = $userobject.Id

$syncstatus = get-mguser -Userid $Employeeemail -Property OnPremisesSyncEnabled 
$params = @{
    AccountEnabled = $false
        }

#Check if user in on prem synced or not to follow a flow        
if ($syncstatus.OnPremisesSyncEnabled -eq "true"){
    
    #Block sign-in
    update-mguser -Userid $Employeeemail -BodyParameter $params
    
}

#Sign out of all sessions
Revoke-MgUserSignInSession -UserId $Employeeemail

#Remove from all Active Directory Groups



#Remove from all Azure Active Directory Groups(Im thinking all groups in azure should be dynamic ones the user will be removed from anyway on Termed marking or loss of license)

$UserToRemove = "ENTEREMAILHERE"
 
Try {
    #Connect to Exchange Online
    Connect-ExchangeOnline
 
    #Get All Distribution Lists - Excluding Mail enabled security groups
    $DistributionGroups = Get-Distributiongroup -resultsize unlimited |  Where-Object {!$_.GroupType.contains("SecurityEnabled")}
 
    #Loop through each Distribution Lists
    ForEach ($Group in $DistributionGroups)
    {
        #Check if the Distribution List contains the particular user
        If ((Get-DistributionGroupMember $Group.Guid | Select-Object -Expand PrimarySmtpAddress) -contains $UserToRemove)
        {
            Remove-DistributionGroupMember -Identity $Group.Guid -Member $UserToRemove -Confirm:$false
            Write-host "Removed user from group '$Group'" -f Green
        }
    }
}
Catch {
    write-host -f Red "Error:" $_.Exception.Message
}






#7.Email forwarding Prolly use exchange for this also
#Set-Mailbox ringo.starr@mycompany.com –ForwardingSmtpAddress ringo@abbeyroad.com –DeliverToMailboxAndForward $false
#Set-Mailbox ringo.starr@mycompany.com –ForwardingSmtpAddress ringo@abbeyroad.com –DeliverToMailboxAndForward $true


#8. Reporting back to Zoho

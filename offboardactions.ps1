$Employeeemail = "user@contoso.com"
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

#Remove from all Azure Active Directory Groups
$Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id

foreach ($i in $Groups.Id){

    Write-Output "Removing $employeeemail from the group"
    # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
    $ref='$ref'

    
    Invoke-MgGraphRequest -Method Delete -Uri "https://graph.microsoft.com/v1.0/groups/$($i)/members/$($userobjectstr)/$ref"


}

#Remove-MgGroupMemberByRef


$RemoveMembers = get-mguserbyid -BodyParameter $params


foreach ($Member in $RemoveMembers) {
    Write-Output "Removing $Member from the group"
    # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
    $ref='$ref'

    $UserObj = Get-MgUser -UserId "$Member"
    Invoke-MgGraphRequest -Method Delete -Uri "https://graph.microsoft.com/v1.0/groups/$($GroupObj.Id)/members/$($UserObj.Id)/$ref"
}


$Groups = Get-MguserMemberOf -Userid $Employeeemail -property Id 
 foreach ($i in $Groups.Id){

     Write-Output "Removing $($UserObj.Id) from the $i"
     # need this for the graph query below; it needs a $ref tacked on at the end. By setting the variable to '$ref' it does not get interpreted as a variable.
     $ref='$ref'
 
     $UserObj = Get-MgUser -UserId "$Member"
     Invoke-MgGraphRequest -Method Delete -Uri "https://graph.microsoft.com/v1.0/groups/$($i)/members/$($UserObj.Id)/$ref"
 }





 $encryptedsecretpassword = ConvertTo-SecureString -String $clientsecretpassword -AsPlainText -Force

$token2 = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $encryptedsecretpassword, $clientsecret

$ApplicationId = 'APPLICATION_ID'
$SecuredPassword = "SECURE_PASSWORD"
$tenantID = "TENANT_ID"
$SecuredPasswordPassword = ConvertTo-SecureString `
-String $SecuredPassword -AsPlainText -Force
$ClientSecretCredential = New-Object `
-TypeName System.Management.Automation.PSCredential `
-ArgumentList $ApplicationId, $SecuredPasswordPassword
Connect-MgGraph -TenantId $tenantID -ClientSecretCredential $ClientSecretCredential
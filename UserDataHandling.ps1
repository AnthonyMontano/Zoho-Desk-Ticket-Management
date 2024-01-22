$offboarddata = Get-Content -Raw -Path "C:\Users\Anthony\Zoho\Scripts\Cloned-Repo\Zoho-Desk-Ticket-Management\Config Files\OpenOffboardsData.json"
$offboardinfo = $offboarddata | ConvertFrom-Json 

# Create an array to store offboard objects
$offboardObjects = @()

<#foreach ($offboard in $offboardinfo.GetEnumerator()) {
    # Create a custom object for each offboard entry
    $offboardObject = [PSCustomObject]@{
        'Ticket Number'      = $offboard.Value.'Ticket Number' 
        'Ticket ID'      = $offboard.Value.'Ticket ID'
        'Employee Name'      = $offboard.Value.'Employee Name' 
        'Employee Location'      = $offboard.Value.'Employee Location'
        'Title'      = $offboard.Value.'Title' 
        'AssociateID'      = $offboard.Value.'Associate ID'
        'Department'       = $offboard.Value.'Department'
        'Email Forwarding'      = $offboard.Value.'Email Forwarding' 
        # Add more properties as needed
    }#>
    
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
        }

    # Add the object to the array
    $offboardObjects += $offboardObject
}

# Now you have an array of custom objects representing each offboard entry
# You can perform actions on each object in the array
foreach ($obj in $offboardObjects) {
    # Example: Print information about each offboard entry
    Write-Host "Processing offboard for User: $($obj.'Employee Name'), $($obj.'Ticket Number'), $($obj.'Ticket ID'), $($obj."Department"), $($obj.'Employee Location'), $($obj."Title"), Department: $($obj."Department")"
    # Add your custom logic here
}

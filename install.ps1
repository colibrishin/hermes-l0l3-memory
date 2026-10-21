$HermesDir = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { [IO.Path]::Combine($env:USERPROFILE, ".hermes") }
New-Item -ItemType Directory -Force -Path ([IO.Path]::Combine($HermesDir, "plugins")) | Out-Null
New-Item -ItemType Directory -Force -Path ([IO.Path]::Combine($HermesDir, "skills")) | Out-Null
Copy-Item -Recurse -Force ([IO.Path]::Combine($PSScriptRoot, "plugins", "l0-l3-memory")) ([IO.Path]::Combine($HermesDir, "plugins", "l0-l3-memory"))
Copy-Item -Recurse -Force ([IO.Path]::Combine($PSScriptRoot, "skills", "l0-l3-memory")) ([IO.Path]::Combine($HermesDir, "skills", "l0-l3-memory"))
Write-Host "Installed l0-l3-memory plugin and skill to $HermesDir" -ForegroundColor Green

# --------------------------------------------------------------
# USER SETTINGS – DO NOT CHANGE ANYTHING BELOW UNLESS NEEDED
# --------------------------------------------------------------

# 1️⃣ Folder that will become the repo (must be writable)
$projectRoot = "C:\Users\vanda\Downloads\Handwritten"

# 2️⃣ Notebook file name (including .ipynb)
$notebookFile = "Vandana_Handwritten_Digit_Recognition_ANN_CNN (1).ipynb"

# 3️⃣ HTTPS URL of the GitHub repository you just created
$repoUrl = "https://github.com/Vandana251/handwritten-notebooks.git"

# 4️⃣ Do you want to include the most‑recent uploaded image?
#    Set $includeImage = $true to copy it, or $false to skip it.
$includeImage = $true   # <-- change to $false if you do NOT want the image added

# 5️⃣ Target branch (most repos use 'main')
$targetBranch = "main"

# --------------------------------------------------------------
# DO NOT MODIFY BELOW THIS LINE (unless you really need to)
# --------------------------------------------------------------

# ----------------------------------------------------------------
# 1️⃣ Initialise / verify Git repository
# ----------------------------------------------------------------
if (-not (Test-Path $projectRoot)) {
    Write-Error "❌ Folder does not exist: $projectRoot"
    exit 1
}
Set-Location $projectRoot
if (-not (Test-Path ".git")) {
    Write-Host "🔧 Initialising a new Git repository..."
    git init | Out-Null
}

# ----------------------------------------------------------------
# 2️⃣ Set (or update) remote 'origin'
# ----------------------------------------------------------------
if (git remote | Where-Object { $_ -eq "origin" }) {
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}
Write-Host "🔗 Remote set to $repoUrl"

# ----------------------------------------------------------------
# 3️⃣ OPTIONAL: copy the extra uploaded image into the repo folder
# ----------------------------------------------------------------
if ($includeImage) {
    $srcImg = "C:\Users\vanda\.gemini\antigravity\brain\1fdad054-a5ea-492d-a43d-4866d5f53845\.user_uploaded\media_1794236170241_35b96189.jpg"
    $dstImg = Join-Path $projectRoot "extra-image.jpg"
    Write-Host "📁 Copying extra image to the repo folder..."
    Copy-Item -Path $srcImg -Destination $dstImg -Force
    Write-Host "✅ Image copied."
}

# ----------------------------------------------------------------
# 4️⃣ Create (or overwrite) README.md
# ----------------------------------------------------------------
$readme = @"
# Handwritten Notebooks

This repository contains handwritten Jupyter notebooks.

## Contents
- `$notebookFile` – your notebook
$(if ($includeImage) { "- `extra-image.jpg` – the additional image you chose to include." })
- GitHub Actions workflow that validates the notebook on every push.

## How to use
1. Clone the repository: `git clone $repoUrl`  
2. Add or edit notebooks in the root folder.  
3. Commit & push – the CI workflow runs automatically.

---  
*Created with Antigravity AI.*
"@
Set-Content -Path "README.md" -Value $readme -Encoding UTF8
Write-Host "✅ README.md written."

# ----------------------------------------------------------------
# 5️⃣ Create GitHub Actions workflow (ci.yml)
# ----------------------------------------------------------------
$workflowPath = ".github\workflows\ci.yml"
$workflow = @"
name: CI – Notebook validation

on:
  push:
    branches: [ $targetBranch ]
  pull_request:
    branches: [ $targetBranch ]

jobs:
  run-notebook:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        if: exists('requirements.txt')
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install Jupyter
        run: |
          python -m pip install --upgrade pip
          pip install jupyter nbconvert

      - name: Execute notebook
        run: |
          jupyter nbconvert --to notebook --execute "$notebookFile" --output "${notebookFile}_executed.ipynb"

      - name: Upload executed notebook
        uses: actions/upload-artifact@v4
        with:
          name: executed-notebook
          path: "${notebookFile}_executed.ipynb"
"@
$wfFolder = Split-Path $workflowPath -Parent
if (-not (Test-Path $wfFolder)) { New-Item -ItemType Directory -Path $wfFolder -Force | Out-Null }
Set-Content -Path $workflowPath -Value $workflow -Encoding UTF8
Write-Host "✅ GitHub Actions workflow created at $workflowPath"

# ----------------------------------------------------------------
# 6️⃣ Stage, commit, and push everything
# ----------------------------------------------------------------
git add .
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Initial commit – $ts"
Write-Host "🚀 Pushing to $repoUrl (branch: $targetBranch)…"
git push -u origin $targetBranch

Write-Host "`n✅ Done! Open the repository in a browser to verify:"
Write-Host "   $repoUrl"
Write-Host "   → Check the **Actions** tab for the CI run."


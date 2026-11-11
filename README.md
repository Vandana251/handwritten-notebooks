# Handwritten Notebooks

This repository contains handwritten Jupyter notebooks.

## Contents

- One or more `.ipynb` notebook files (e.g., `MyNotebook.ipynb`).
- Any accompanying images (e.g., the uploaded handwritten image).
- A GitHub Actions workflow that validates the notebooks on each push.

## How to use

1. Clone the repository.
2. Add or edit notebooks in the root folder.
3. Push your changes – the CI workflow will automatically run and verify the notebooks.

## CI Workflow

The workflow (`.github/workflows/ci.yml`) runs on Windows, sets up Python 3.11, installs any dependencies from `requirements.txt`, executes the notebooks with `jupyter nbconvert`, and uploads the executed notebooks as artifacts.

---
*Created with the help of Antigravity AI.*

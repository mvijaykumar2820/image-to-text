# GitHub Pages Setup Guide

## Problem: Jekyll Build Errors
GitHub Pages uses Jekyll by default, which can cause build errors when it encounters files with Liquid-like syntax (like `{{ }}` or `{% %}`) in your `node_modules` folder.

## Solution: Configure Jekyll to Ignore Problematic Files

### Files Created:

1. **`.jekyllignore`** - Tells Jekyll which files and folders to ignore
2. **`_config.yml`** - Jekyll configuration file with exclusions
3. **`index.html`** - Static GitHub Pages landing page

### How It Works:

- Jekyll will ignore `node_modules/` and other problematic directories
- Your Flask app can still run locally on `localhost:5003`
- GitHub Pages will serve the static `index.html` as the main page
- Users can clone the repo and run the full React/Flask app locally

### GitHub Pages URL:
Your site will be available at: `https://mvijaykumar2820.github.io/image-to-text/`

### Local Development:
For full functionality, users should:
```bash
git clone https://github.com/mvijaykumar2820/image-to-text.git
cd image-to-text
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5003` for the full React/Flask application.

## Alternative: Disable Jekyll Completely

If you want to disable Jekyll entirely, you can:
1. Create a `.nojekyll` file in your repository root
2. Use GitHub Actions to build and deploy your site
3. Use a different branch (like `gh-pages`) for deployment

## Tips for GitHub Copilot:

When working with GitHub Pages and Jekyll issues, you can prompt Copilot with:

```markdown
# TODO: Fix GitHub Pages Jekyll build errors
# - Add .jekyllignore to exclude node_modules
# - Configure _config.yml to exclude problematic files
# - Create static index.html for GitHub Pages
```

This helps Copilot understand the context and provide better suggestions.

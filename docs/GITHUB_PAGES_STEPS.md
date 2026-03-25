
# GitHub Pages setup

## 1. Create a new repo
Suggested name:
`seasat-demo`

## 2. Upload this whole folder
You can do it in the GitHub web interface:
- open the repo
- click `Add file`
- choose `Upload files`
- drag in everything from this folder
- commit to `main`

## 3. Turn on GitHub Pages
- go to the repo
- click `Settings`
- click `Pages`
- under `Build and deployment`, set:
  - Source: `Deploy from a branch`
  - Branch: `main`
  - Folder: `/ (root)`
- click `Save`

## 4. Wait for the page URL
GitHub will give you a URL like:
`https://solamadeus.github.io/seasat-demo/`

## 5. Test it
Open that URL and check:
- map loads
- layers toggle on and off
- popups show values

## 6. Later update
Any time you upload new `data/*.geojson` or change `config.js`, the site updates automatically after a new commit.

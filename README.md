# sindream.github.io

Personal research portfolio for Woojae Shin, published with GitHub Pages.

## Structure

- `index.html`, `assets/`, and supporting root files - files published by GitHub Pages
- `assets/cv/` - downloadable CV PDF
- `cv/` - editable CV data and PDF builder

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Rebuild the CV

```bash
python3 cv/build_cv.py
```

The script writes `assets/cv/woojae-shin-cv.pdf`.

## Publish

In the repository's GitHub Pages settings, choose:

- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/(root)**

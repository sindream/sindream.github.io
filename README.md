# sindream.github.io

Academic research portfolio for Woojae Shin, published with GitHub Pages.

## Structure

- `index.html` - research homepage with the complete publication list
- `profile.html` - background, identity, education, and research interests
- `projects/` - expandable research project pages linked from publications
- `assets/css/` and `assets/js/` - visual system and lightweight interactions
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

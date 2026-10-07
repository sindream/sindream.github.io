# CV source

The current PDF is a public academic CV generated from:

- profile and education details supplied by Woojae Shin
- ORCID `0000-0002-6155-3712`
- official DOI and proceedings metadata
- KAIST FAIR publication, conference, and thesis records
- KCI, DBpia, and official conference programs where applicable
- official AI Grand Prix and ICUAS competition result announcements
- the owner's public LinkedIn profile URL

Install the PDF dependency, edit `cv_data.json`, then run:

```bash
python3 -m pip install -r cv/requirements.txt
python3 cv/build_cv.py
```

The builder writes the website-ready PDF to `assets/cv/woojae-shin-cv.pdf`.

The date of birth is intentionally public in this edition because the owner requested it. Age is not displayed.

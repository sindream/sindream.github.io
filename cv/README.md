# CV source

The current PDF is a paper-led public research CV generated from:

- profile and education details supplied by Woojae Shin
- ORCID `0000-0002-6155-3712`
- DOI metadata for the listed IEEE Robotics and Automation Letters papers

Edit `cv_data.json`, then run:

```bash
python3 cv/build_cv.py
```

The builder writes the website-ready PDF to `assets/cv/woojae-shin-cv.pdf`.

The date of birth and age are intentionally public in this edition because the owner requested them. Update `age` and `age_as_of` whenever the static PDF is revised; the website calculates age automatically.

# BibleViz

Search the New Testament and see your results visualized.

**Web version: https://bpmdata.github.io/BibleViz/**

Type names, words or phrases; every match in `nt_bible_clean.txt` (King James New Testament, from Project
Gutenberg) is plotted by where it falls, with Plotly.

## Files

| File | What it is |
|---|---|
| `index.html` | The web version. Runs entirely in the browser (served by GitHub Pages); no server needed. |
| `streamlit_bibleviz.py` | The older Streamlit app. |
| `main.py` | The original script that made the first, fixed chart. |

## Run the Streamlit version

```bash
pip install -r requirements.txt
streamlit run streamlit_bibleviz.py
```

The Streamlit app downloads the text from a fixed commit of this repo, so changes here don't affect it.

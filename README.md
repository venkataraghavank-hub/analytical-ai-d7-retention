# D7 Retention Explorer

An interactive classroom simulator based on the multiple linear regression model in `1_Predicting_Retention.ipynb`.

## Included documentation

- `docs/MODEL_CARD.md` — purpose, equation, intended use, and limitations.
- `docs/DATA_DICTIONARY.md` — definitions of the model inputs and target.
- `.streamlit/config.toml` — the application theme and Streamlit server settings.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository, for example `analytical-ai-d7-retention`.
2. Upload the complete project while retaining the folder structure.
3. In Streamlit Community Cloud, select **Create app**, choose the repository and branch, and set the main file path to `streamlit_app.py`.
4. Click **Deploy**. Streamlit will provide the public application URL.

The model shows statistical associations from the classroom dataset, not causal effects.

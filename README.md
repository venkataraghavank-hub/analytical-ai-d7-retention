# D7 Retention Explorer

An interactive classroom simulator based on a multiple linear regression model for seven-day user retention.

## What it does

Enter values for onboarding completion, push-notification opt-in, and average first-week sessions. The application estimates D7 retention and shows the contribution associated with each driver.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Set the repository's main file path to `streamlit_app.py`, then deploy. No secrets or external data connection are required.

### Class-code access

The app requires a class code. In Streamlit Community Cloud, open **App settings → Secrets** and add:

```toml
STUDENT_ACCESS_CODE = "your-class-code"
```

The application compares codes without regard to capitalisation. Do not commit the real code to GitHub.

## Documentation

- `docs/MODEL_CARD.md` — model purpose, equation, use, and limitations.
- `docs/DATA_DICTIONARY.md` — definitions of the inputs and target.

# Weekly CISO Targeting Engine

A Streamlit dashboard prototype for weekly prioritisation of the top 3 CISO targets across Mumbai, Pune and Ahmedabad.

## What is included
- Top-3 weekly target view
- 100-account scoring architecture
- Revenue + market-cap company-size model
- Cyber opportunity scoring
- CISO/contact/evidence panels
- Filters by city and Cyble opportunity
- CSV export
- Starter account universe

## Live intelligence
The UI is ready for a web/AI search connector. For production, connect an approved search provider and an LLM with web grounding to populate:
- revenue
- market cap
- CISO
- public professional contact
- recent cyber/security investment
- breach/threat indicators
- brand impersonation/phishing
- dark-web signals
- evidence URLs and dates

Use only public professional contact details. Do not collect or store private/personal phone numbers.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Production
Deploy the repository to Streamlit Community Cloud, Azure, AWS, or another Python hosting platform. Add the chosen search/AI API credentials as environment/secrets and connect the `refresh_intelligence()` workflow.

## Data methodology
Eligible universe: HQ in Mumbai, Pune or Ahmedabad.
Company-size score: 50% normalised revenue + 50% normalised market capitalisation.
Weekly opportunity score:
- Cybersecurity activity 20%
- Threat exposure 20%
- Brand/impersonation exposure 15%
- Security technology investment 15%
- CISO activity 10%
- Digital expansion 10%
- Recent security incident 10%

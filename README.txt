SMART REWARDS — AUTHENTICATION STARTER

What this package does
- Creates a basic registration page.
- Stores member records in a local SQLite database.
- Hashes passwords before storage (passwords are not stored as plain text).
- Provides login, a protected member dashboard, and logout.

What it does NOT do
- It is not hosted on the internet and has no public login URL.
- It does not process membership fees, bank transfers, withdrawals or rewards.
- It has no password reset, phone verification, email verification, admin dashboard,
  referral tracking, video library, advertiser integration or fraud controls.
- It is not production-ready. A security review and additional protections are required.

Run locally (requires Python 3.10+)
1. Extract this ZIP on a computer.
2. Open a terminal in the extracted smart_rewards_starter folder.
3. Create a virtual environment:
   python -m venv .venv
4. Activate it:
   Windows: .venv\Scripts\activate
   macOS/Linux: source .venv/bin/activate
5. Install dependencies:
   pip install -r requirements.txt
6. Set a strong secret key before running:
   Windows PowerShell: $env:SMART_REWARDS_SECRET="replace-with-a-long-random-secret"
   macOS/Linux: export SMART_REWARDS_SECRET="replace-with-a-long-random-secret"
7. Start:
   python app.py
8. On that same computer, open http://127.0.0.1:5000

IMPORTANT BEFORE PUBLIC LAUNCH
- Use HTTPS and a production WSGI server; never use Flask's development server publicly.
- Set a strong secret key and secure cookie settings.
- Add CSRF protection, rate limiting, phone/email verification, secure password reset,
  audit logs, backups, privacy notices and data-protection controls.
- Obtain Nigerian and Cameroonian legal/compliance advice before accepting payments.
- Confirm advertiser contracts and sustainable reward funding. Never fund member
  rewards from later members' deposits or promise guaranteed daily earnings.
- Choose a licensed payment provider only after due diligence. No provider is selected.
- Do not put real bank account numbers or private credentials in this starter package.

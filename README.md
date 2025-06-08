RentMate – Roommate Chore & Expense Scheduler
Project Overview
RentMate is a collaborative web application built with Streamlit and SQLite that helps roommates or household members manage chores, track shared expenses, and coordinate schedules. It provides user authentication, household management with invite codes, chore and expense tracking, and a simple dashboard to visualize activities.

Features
User Authentication: Secure signup and login with password hashing using bcrypt.

Household Management: Create or join households via unique 6-digit invite codes.

Role-based Membership: Owners and members with specific permissions.

Chore Scheduler: Assign chores with customizable frequency and due dates.

Expense Tracker: Log shared expenses, including participants and payer.

Dashboard: Overview of household chores and expenses.

Session Management: Persistent login state with Streamlit session_state.

Invite Code Sharing: Easy invite code generation to onboard new household members.

Tech Stack
Frontend & Backend: Streamlit (Python)

Database: SQLite (local file-based)

Password Security: bcrypt for hashing passwords

Other Libraries: Python standard libraries (random, string, sqlite3)

Project Structure
graphql
Copy
Edit
rentmate/
│
├── app.py                     # Main app entry point
├── requirements.txt           # Required Python packages
├── utils/
│   ├── auth.py                # Authentication & authorization functions
│   └── db.py                  # Database connection and queries
│
├── pages/
│   ├── 0_🏠_Dashboard.py       # Household dashboard UI
│   ├── 1_👥_Household.py       # Household creation and join page
│   ├── 2_🧹_Chores.py          # Chore management page
│   ├── 3_💸_Expenses.py        # Expense tracking page
│   └── 4_📅_Calendar.py        # Household calendar view (optional)
│
└── rentmate.db                # SQLite database file (auto-generated)
How to Run Locally
Clone the repo:

bash
Copy
Edit
git clone https://github.com/yourusername/rentmate.git
cd rentmate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
streamlit run app.py
Open your browser and go to http://localhost:8501

Deployment
You can deploy RentMate on platforms like:

Streamlit Cloud: https://streamlit.io/cloud

Heroku: Use a suitable buildpack and SQLite file handling

Other Cloud Providers: AWS, GCP, or Azure with Docker or VM setup

Make sure to configure persistent storage for the SQLite database.

Usage
Sign Up / Log In: Register a new user or log in with your credentials.

Create Household: Generate a new household with an auto-generated invite code.

Join Household: Use an existing household’s invite code to join.

Manage Chores & Expenses: Add chores with deadlines and assign them; track household expenses with participants.

Dashboard: View summary and recent activity for your household.

Assumptions & Notes
The app assumes single database file usage (rentmate.db) and does not support multi-tenant or cloud DB by default.

Invite codes are 6-character alphanumeric, unique per household.

No email verification is implemented.

Household members can only belong to one household at a time.

Chores and expenses data persist as long as the rentmate.db file is not deleted.

Session state is managed in-memory by Streamlit, so sessions end when the server restarts.

Future Enhancements
Email-based invites and notifications.

Real-time calendar syncing and reminders.

Role-based access control with more granular permissions.

Export chores and expenses to CSV or Google Sheets.

Mobile responsive UI improvements.

Cloud database integration for multi-user access.

Contact
For questions or contributions, please reach out:

Author: Your Name

Email: your.email@example.com

GitHub: https://github.com/yourusername


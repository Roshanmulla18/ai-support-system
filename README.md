\# AI Support Ticket System

\## Final Year Major Project



---



\## 📋 PROJECT OVERVIEW

An AI-powered helpdesk system that automatically classifies, prioritizes, and responds to support tickets using Natural Language Processing (NLP).



\*\*🔴 Live Demo:\*\* \[https://roshanmulla-ai-support-system-final.hf.space](https://roshanmulla-ai-support-system-final.hf.space)



---



\## 🚀 QUICK START GUIDE



\### \*\*Method 1: Double-click (EASIEST)\*\*

1\. Open File Explorer and go to project folder

2\. \*\*Double-click\*\* `start.bat`

3\. Terminal opens with virtual environment activated

4\. Type: `python main.py`

5\. Open browser to `http://localhost:8000`



\### \*\*Method 2: PowerShell (Colorful)\*\*



```powershell



cd C:\\Users\\mulla\\OneDrive\\Desktop\\ai-support-system

.\\start.ps1



Method 3: Manual (If scripts don't work)



powershell



cd C:\\Users\\mulla\\OneDrive\\Desktop\\ai-support-system

.\\.venv\\Scripts\\Activate.ps1

cd backend

python main.py



📁 PROJECT STRUCTURE



text



ai-support-system/

│

├── 📁 backend/                 # Python backend code

│   ├── 📄 main.py              # Main FastAPI server

│   └── 📄 requirements.txt     # Python dependencies

│

├── 📁 .venv/                   # Virtual environment

│   └── 📁 Scripts/             # Activation scripts

│

├── 📁 data/                     # Database files (future)

├── 📁 frontend/                 # React frontend (future)

├── 📁 notebooks/                # AI experiments (future)

├── 📁 scripts/                  # Helper scripts (future)

├── 📁 tests/                    # Test files (future)

│

├── 📄 start.bat                  # Easy launcher (double-click)

├── 📄 start.ps1                  # PowerShell launcher (colorful)

├── 📄 Dockerfile                  # For cloud deployment

├── 📄 .gitignore                  # Git ignored files

└── 📄 README.md                   # This documentation



🔧 COMMANDS CHEAT SHEET



Command	What it does



python main.py	Start the server

git status	Check git status

git add .	Stage all changes

git commit -m "message"	Commit changes

git push	Push to GitHub

pip list	See installed packages

deactivate	Exit virtual environment

Ctrl + C	Stop the running server



🌐 API ENDPOINTS



URL	Description

http://localhost:8000	Homepage (returns JSON)

http://localhost:8000/test	Test endpoint

http://localhost:8000/docs	Interactive API documentation

http://localhost:8000/redoc	Alternative documentation

Live URLs (same as above):



text

https://roshanmulla-ai-support-system-final.hf.space

https://roshanmulla-ai-support-system-final.hf.space/test

https://roshanmulla-ai-support-system-final.hf.space/docs





📦 INSTALLED PACKAGES



text

Package           Version

----------------- -------

fastapi           0.104.1

uvicorn           0.24.0

sqlalchemy        2.0.23

pydantic          2.5.0

python-dotenv     1.0.0

To install all packages:



powershell



pip install -r backend/requirements.txt





🎯 PROJECT PHASES



Phase	Description	Status

Phase 1	Project Setup \& Environment	✅ Complete

Phase 2	Basic FastAPI Server \& Deployment	✅ Complete

Phase 3	Database \& Authentication	🔜 Next

Phase 4	Ticket CRUD Operations	⏳ Planned

Phase 5	AI Classification \& Sentiment	⏳ Planned

Phase 6	RAG Auto-Resolution	⏳ Planned

Phase 7	Agent Dashboard (Frontend)	⏳ Planned

Phase 8	Admin Analytics \& Final Polish	⏳ Planned







🤖 AI FEATURES (COMING SOON)



Feature	Description	Phase

Auto-categorization	AI detects ticket type (billing, technical, etc.)	Phase 5

Sentiment Analysis	Detects customer mood (angry, happy, urgent)	Phase 5

Priority Assignment	Auto-assigns priority based on sentiment	Phase 5

Auto-Responses	AI suggests answers from knowledge base	Phase 6

RAG Implementation	Retrieval-Augmented Generation for accurate replies	Phase 6





👥 USER ROLES



Role	Permissions

Customer	Create tickets, view own tickets, receive responses

Agent	View all tickets, respond, use AI suggestions

Admin	All agent rights + view analytics, manage users



🔍 TROUBLESHOOTING



Error: "Port 8000 already in use"



powershell



\# Close other server windows or use different port

\# Edit main.py and change port=8000 to port=8001

Error: "No module named fastapi"



powershell



\# Make sure virtual environment is activated

\# Then run: pip install -r backend/requirements.txt

Error: "Cannot find .venv"



powershell



\# Create new virtual environment

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r backend/requirements.txt

Error: "File not found" when running python main.py



powershell



\# Make sure you're in the backend folder

cd C:\\Users\\mulla\\OneDrive\\Desktop\\ai-support-system\\backend

python main.py

Error: "Git push rejected"



powershell



\# Pull latest changes first

git pull origin main

git push





📝 GIT WORKFLOW



powershell



\# Check status

git status



\# Add changes

git add .



\# Commit with message

git commit -m "Description of changes"



\# Push to GitHub

git push



\# Pull latest changes

git pull origin main





🌍 DEPLOYMENT (HUGGING FACE)



Live URL: https://roshanmulla-ai-support-system-final.hf.space



How to update deployment:

Make changes locally



Test with python main.py





Commit and push to GitHub:



powershell



git add .

git commit -m "Description of changes"

git push

Hugging Face auto-updates in 3-5 minutes







📊 FUTURE ENHANCEMENTS





Email notifications for ticket updates



File attachments in tickets



Multi-language support



Mobile app (React Native)



Dashboard with charts and analytics



SLA tracking for urgent tickets



Integration with Slack/Teams





👨‍💻 DEVELOPER INFORMATION



Name: Mulla

Project: Final Year Major Project

Institution: TONTADARYA COLLEGE OF ENGINEERING 

Department: Computer Science \& Engineering

Year: 2026



📚 REFERENCES



FastAPI Documentation: https://fastapi.tiangolo.com



Hugging Face Spaces: https://huggingface.co/docs/hub/spaces



SQLAlchemy: https://www.sqlalchemy.org



React: https://reactjs.org







✅ COMPLETION CHECKLIST



Phase 1: Project Setup \& Environment



Phase 2: Basic FastAPI Server \& Deployment



Startup scripts (start.bat, start.ps1)



GitHub repository



Live deployment on Hugging Face



Complete documentation (README.md)



Phase 3: Database \& Authentication



Phase 4: Ticket CRUD



Phase 5: AI Classification



Phase 6: Auto-Responses



Phase 7: Agent Dashboard



Phase 8: Admin Analytics









📝 LICENSE



This project is created for educational purposes as a Final Year Major Project.

MIT License - Feel free to learn from this code.







📞 CONTACT



For any questions or suggestions, please contact:



Name: Mohammedroshan M Mulla



Email: mullaroshan6@gmail.com



GitHub: https://github.com/Roshanmulla18







⭐ If you find this project useful, please star it on GitHub!



text



---




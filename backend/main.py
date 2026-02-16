"""
FILE: main.py
PURPOSE: Main server for AI Support Ticket System
"""

from fastapi import FastAPI
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="AI Support Ticket System",
    description="Final Year Major Project - AI Powered Helpdesk",
    version="1.0.0"
)

# Root endpoint - Health check
@app.get("/")
def root():
    """
    Homepage endpoint
    Returns: Welcome message
    """
    return {
        "project": "AI Support Ticket System",
        "status": "running",
        "phase": "Phase 2 - Basic Server",
        "message": "Server is working!",
        "developer": "Mulla",
        "year": 2026
    }

# Test endpoint
@app.get("/test")
def test():
    """
    Test endpoint to verify API is working
    """
    return {
        "success": True,
        "message": "API is functioning correctly",
        "endpoints": [
            "/",
            "/test",
            "/docs",
            "/redoc"
        ]
    }

# Run the server - this part is correct now
if __name__ == "__main__":
    print("=" * 50)
    print("AI SUPPORT TICKET SYSTEM")
    print("=" * 50)
    print("Server starting...")
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Press CTRL+C to stop")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException
import requests
import json
import os

app = FastAPI(title="AI Processor Service")

# Points to host.docker.internal when running in Docker
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

@app.post("/process")
async def process_lead(raw_lead: dict):
    prompt = f"""
    Task: Extract data for a Private Medical Clinic in Egypt.
    Text: "{raw_lead['raw_data']}"
    Output ONLY JSON:
    {{
        "is_private_clinic": boolean,
        "dr_name": "string",
        "cleaned_phone": "string",
        "rating": "string",
        "has_dr_title": boolean
    }}
    """
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "format": "json",
            "stream": False
        })
        ai_data = json.loads(res.json()['response'])
        
        if not ai_data.get("is_private_clinic"):
            return {"status": "rejected"}

        # Confidence Scoring logic
        rating = float(ai_data.get("rating", 0)) if str(ai_data.get("rating")).replace('.','',1).isdigit() else 0
        has_phone = ai_data.get("cleaned_phone") != "N/A"
        
        confidence = "LOW"
        if ai_data.get("has_dr_title") and rating >= 4.0 and has_phone:
            confidence = "HIGH"
        elif rating > 0 or has_phone:
            confidence = "MEDIUM"

        return {
            "status": "verified",
            "clinic_name": raw_lead['name'],
            "doctor_name": ai_data.get("dr_name"),
            "phone": ai_data.get("cleaned_phone"),
            "rating": rating,
            "confidence": confidence,
            "link": raw_lead['link']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
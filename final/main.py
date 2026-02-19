import httpx
import asyncio
import pandas as pd
from fastapi import FastAPI, BackgroundTasks
import os

app = FastAPI(title="Orchestrator")

SCRAPER_URL = os.getenv("SCRAPER_URL", "http://localhost:8001/scrape")
AI_URL = os.getenv("AI_URL", "http://localhost:8002/process")

async def process_single_lead(client, lead):
    """Helper function to send one lead to the AI service."""
    try:
        response = await client.post(AI_URL, json=lead, timeout=60.0)
        data = response.json()
        if data.get("status") == "verified":
            return data
    except Exception as e:
        print(f"Error processing lead {lead.get('name')}: {e}")
    return None

async def run_pipeline(query: str, filename: str):
    # 1. Get raw data from Scraper Service
    async with httpx.AsyncClient() as client:
        try:
            # The scraper is still mostly sequential due to Selenium, 
            # but we call it asynchronously here.
            scraper_res = await client.get(SCRAPER_URL, params={"query": query, "limit": 10}, timeout=120.0)
            raw_leads = scraper_res.json()
            
            # 2. Process ALL leads in parallel
            # We create a list of tasks and run them concurrently
            tasks = [process_single_lead(client, lead) for lead in raw_leads]
            results = await asyncio.gather(*tasks)
            
            # Filter out None values (rejected leads or errors)
            processed_results = [r for r in results if r is not None]
            
            # 3. Save to CSV
            if processed_results:
                pd.DataFrame(processed_results).to_csv(filename, index=False)
                print(f"Pipeline complete. Saved to {filename}")
                
        except Exception as e:
            print(f"Pipeline failed: {e}")

@app.post("/start-scrape")
async def start(query: str, output: str = "results.csv", bt: BackgroundTasks = BackgroundTasks()):
    # BackgroundTasks is still used so the API responds immediately
    bt.add_task(run_pipeline, query, output)
    return {"message": "Parallel job submitted to microservices"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
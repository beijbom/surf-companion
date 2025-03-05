from typing import List

from fastapi.responses import HTMLResponse
from sqlmodel import Session, create_engine, select

from config import sqlite_url
from datamodel import Rating, Spot, Surfer


def get_surfers() -> List[Surfer]:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        return session.exec(select(Surfer)).all()


def get_spots() -> List[Spot]:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        return session.exec(select(Spot)).all()


def homepage() -> HTMLResponse:
    surfers = get_surfers()
    spots = get_spots()
    ratings = [{"value": rating.value, "name": rating.name} for rating in Rating]

    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                form {{
                    background: white;
                    padding: 25px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                
                div {{
                    margin-bottom: 20px;
                }}
                
                label {{
                    display: block;
                    margin-bottom: 8px;
                    color: #34495e;
                    font-weight: 500;
                }}
                
                select {{
                    width: 100%;
                    padding: 8px 12px;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                    color: #2c3e50;
                    background-color: white;
                    transition: border-color 0.3s ease;
                }}
                
                select:focus {{
                    border-color: #3498db;
                    outline: none;
                }}
                
                button {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                    font-weight: 500;
                    transition: background-color 0.3s ease;
                }}
                
                button:hover {{
                    background-color: #2980b9;
                }}
                
                option {{
                    padding: 8px;
                }}
            </style>
        </head>
        <body>
            <h1>🏄‍♂️ Log Surf Session</h1>
            <form action="/log_session" method="post">
                <div>
                    <label for="surfer">Surfer</label>
                    <select name="surfer_id" id="surfer" required>
                        <option value="">Select a surfer</option>
                        {"".join(f'<option value="{s.id}">{s.name}</option>' for s in surfers)}
                    </select>
                </div>
                <div>
                    <label for="spot">Spot</label>
                    <select name="spot_id" id="spot" required>
                        <option value="">Select a spot</option>
                        {"".join(f'<option value="{s.id}">{s.name}</option>' for s in spots)}
                    </select>
                </div>
                <div>
                    <label for="crowd">Crowd</label>
                    <select name="crowd" id="crowd">
                        <option value="">How was the crowd?</option>
                        {"".join(f'<option value="{r["value"]}">{r["name"]}</option>' for r in ratings)}
                    </select>
                </div>
                <div>
                    <label for="wind">Wind</label>
                    <select name="wind" id="wind">
                        <option value="">How was the wind?</option>
                        {"".join(f'<option value="{r["value"]}">{r["name"]}</option>' for r in ratings)}
                    </select>
                </div>
                <div>
                    <label for="waves">Waves</label>
                    <select name="waves" id="waves">
                        <option value="">How were the waves?</option>
                        {"".join(f'<option value="{r["value"]}">{r["name"]}</option>' for r in ratings)}
                    </select>
                </div>
                <button type="submit">Log Session</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

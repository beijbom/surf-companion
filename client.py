from typing import List

from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, create_engine, select

from config import sqlite_url
from datamodel import Rating, Spot, Surfer, SurfSession


def get_surfers() -> List[Surfer]:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        return session.exec(select(Surfer)).all()


def get_spots() -> List[Spot]:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        return session.exec(select(Spot)).all()


def get_surfsessions(surfer_id: str = None, spot_id: str = None) -> List[SurfSession]:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        query = select(SurfSession)
        if surfer_id:
            query = query.where(SurfSession.surfer_id == int(surfer_id))
        if spot_id:
            query = query.where(SurfSession.spot_id == int(spot_id))
        query = query.order_by(SurfSession.timestamp.desc())
        return session.exec(query).all()


def get_surfer_name(session: Session, surfer_id: int) -> str:
    surfer = session.exec(select(Surfer).where(Surfer.id == surfer_id)).first()
    return surfer.name if surfer else "Unknown"


def get_spot_name(session: Session, spot_id: int) -> str:
    spot = session.exec(select(Spot).where(Spot.id == spot_id)).first()
    return spot.name if spot else "Unknown"


def format_rating(rating: Rating | None) -> str:
    return rating.name if rating else "-"


def homepage(request: Request) -> HTMLResponse:
    surfers = get_surfers()
    spots = get_spots()

    # Get filter values and success message from query parameters
    params = request.query_params
    surfer_filter = params.get("surfer_id", "")
    spot_filter = params.get("spot_id", "")
    success_message = params.get("success", "")

    sessions = get_surfsessions(surfer_filter, spot_filter)

    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                .filters {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    display: flex;
                    gap: 20px;
                    align-items: flex-end;
                }}
                
                .filter-group {{
                    flex: 1;
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
                }}
                
                button {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 500;
                    transition: background-color 0.3s ease;
                }}
                
                button:hover {{
                    background-color: #2980b9;
                }}
                
                table {{
                    width: 100%;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                
                th {{
                    background-color: #f8f9fa;
                    font-weight: 600;
                    color: #2c3e50;
                }}
                
                tr:last-child td {{
                    border-bottom: none;
                }}
                
                .nav-links {{
                    text-align: center;
                    margin-top: 20px;
                }}
                
                .nav-links a {{
                    color: #3498db;
                    text-decoration: none;
                    margin: 0 10px;
                }}
                
                .nav-links a:hover {{
                    text-decoration: underline;
                }}
                
                .success-banner {{
                    background-color: #2ecc71;
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    text-align: center;
                    font-weight: 500;
                    display: none;
                }}
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const surferSelect = document.getElementById('surfer_id');
                    const spotSelect = document.getElementById('spot_id');
                    const form = document.querySelector('.filters');
                    
                    // Function to automatically submit form on change
                    function autoSubmit() {{
                        form.submit();
                    }}
                    
                    // Add change listeners to both selects
                    surferSelect.addEventListener('change', autoSubmit);
                    spotSelect.addEventListener('change', autoSubmit);
                    
                    // Remove the submit button since we don't need it anymore
                    form.querySelector('button').style.display = 'none';
                }});
            </script>
            <link rel="icon" type="image/x-icon" href="/favicon.ico">
        </head>
        <body>
            <h1><a href="/" style="text-decoration: none; color: inherit;">🏄‍♂️ Surf Companion</a></h1>
            
            {f'<div class="success-banner">{success_message}</div>' if success_message else ''}
            
            <form class="filters" method="get">
                <div class="filter-group">
                    <label for="surfer_id">Surfer</label>
                    <select name="surfer_id" id="surfer_id">
                        <option value="">All Surfers</option>
                        {"".join(f'<option value="{s.id}" {"selected" if str(s.id) == surfer_filter else ""}>{s.name}</option>' for s in surfers)}
                    </select>
                </div>
                <div class="filter-group">
                    <label for="spot_id">Spot</label>
                    <select name="spot_id" id="spot_id">
                        <option value="">All Spots</option>
                        {"".join(f'<option value="{s.id}" {"selected" if str(s.id) == spot_filter else ""}>{s.name}</option>' for s in spots)}
                    </select>
                </div>
            </form>
            
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Surfer</th>
                        <th>Spot</th>
                        <th>Crowd</th>
                        <th>Wind</th>
                        <th>Waves</th>
                    </tr>
                </thead>
                <tbody>
    """

    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        for surf_session in sessions:
            surfer_name = get_surfer_name(session, surf_session.surfer_id)
            spot_name = get_spot_name(session, surf_session.spot_id)
            html_content += f"""
                    <tr>
                        <td>{surf_session.timestamp.strftime('%Y-%m-%d %H:%M')}</td>
                        <td>{surfer_name}</td>
                        <td>{spot_name}</td>
                        <td>{format_rating(surf_session.crowd)}</td>
                        <td>{format_rating(surf_session.wind)}</td>
                        <td>{format_rating(surf_session.waves)}</td>
                    </tr>
            """

    html_content += """
                </tbody>
            </table>
            
            <div class="nav-links">
                <a href="/log">Log New Session</a>
            </div>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)


def log_form() -> HTMLResponse:
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
            <link rel="icon" type="image/x-icon" href="/favicon.ico">
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

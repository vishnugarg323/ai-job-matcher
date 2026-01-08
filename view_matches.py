"""
Simple script to view job matches from the database.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta


def view_matches():
    """Display recent job matches in a readable format."""
    db_path = Path(__file__).parent / 'data' / 'jobs.db'
    
    if not db_path.exists():
        print("❌ Database not found. Run the application first!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get recent matches
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    cursor.execute('''
        SELECT title, company, location, match_score, url, created_at
        FROM jobs
        WHERE created_at >= ? AND match_score >= 0.90
        ORDER BY match_score DESC, created_at DESC
    ''', (seven_days_ago,))
    
    jobs = cursor.fetchall()
    
    if not jobs:
        print("📭 No job matches found in the last 7 days.")
        print("💡 Tip: Run the application first with: python main.py")
        return
    
    print("=" * 80)
    print(f"🎯 JOB MATCHES - Last 7 Days ({len(jobs)} matches)")
    print("=" * 80)
    print()
    
    for i, (title, company, location, score, url, created_at) in enumerate(jobs, 1):
        print(f"{i}. {title}")
        print(f"   🏢 Company: {company}")
        print(f"   📍 Location: {location}")
        print(f"   ⭐ Match: {score*100:.1f}%")
        print(f"   📅 Found: {created_at[:10]}")
        print(f"   🔗 URL: {url}")
        print()
    
    conn.close()
    
    # Statistics
    print("=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM jobs')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(match_score) FROM jobs WHERE match_score >= 0.90')
    avg_score = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT company) FROM jobs')
    unique_companies = cursor.fetchone()[0]
    
    print(f"Total Jobs Tracked: {total}")
    print(f"Average Match Score: {avg_score*100:.1f}%")
    print(f"Unique Companies: {unique_companies}")
    print()
    
    conn.close()


if __name__ == "__main__":
    view_matches()

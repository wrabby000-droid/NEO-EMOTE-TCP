import requests
import re
from pathlib import Path

# Read index.html and extract all emote IDs
def extract_emote_ids(html_file):
    """Extract all unique emote IDs from index.html"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all data-emote-id attributes
    pattern = r'data-emote-id="(\d+)"'
    emote_ids = re.findall(pattern, content)
    
    # Return unique IDs sorted
    return sorted(set(emote_ids))

# Create emote_files directory if it doesn't exist
emote_dir = Path("emote_files")
emote_dir.mkdir(exist_ok=True)

# Extract all emote IDs from index.html
print("Extracting emote IDs from index.html...")
emote_ids = extract_emote_ids("index.html")
print(f"Found {len(emote_ids)} unique emote IDs")

# Download each emote
base_url = "https://emotex1lite.vercel.app/emote_files/"
downloaded = 0
failed = 0

for emote_id in emote_ids:
    url = f"{base_url}{emote_id}.png"
    file_path = emote_dir / f"{emote_id}.png"
    
    # Skip if file already exists
    if file_path.exists():
        print(f"Already exists: {emote_id}.png")
        downloaded += 1
        continue
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"✓ Downloaded {emote_id}.png")
            downloaded += 1
        else:
            print(f"✗ Failed {emote_id}.png (Status: {r.status_code})")
            failed += 1
    except Exception as e:
        print(f"✗ Error downloading {emote_id}.png: {e}")
        failed += 1

print(f"\nDownload complete!")
print(f"Downloaded: {downloaded}")
print(f"Failed: {failed}")
print(f"Total: {len(emote_ids)}")

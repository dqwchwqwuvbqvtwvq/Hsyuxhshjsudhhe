import asyncio
import time
from aiohttp import ClientSession
import re
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'close',
    'Referer': 'https://linkvertise.com'
}

key_regex = r'let content = \("([^"]+)"\);'

async def get_content(url, session):
    async with session.get(url, headers=headers, allow_redirects=True) as response:
        return await response.text()

@app.route('/fluxus', methods=['GET'])
async def fluxus():
    url = request.args.get('url')
    if url is None or not url.startswith("https://flux.li/android/external/start.php?HWID="):
        return jsonify({"error": "No URL provided or invalid URL"}), 400

    urls = [
        url,
        'https://flux.li/android/external/check1.php?hash={hash}',
        'https://flux.li/android/external/main.php?hash={hash}'
    ]

    start_time = time.time()  # Start timer

    async with ClientSession() as session:
        tasks = [get_content(u, session) for u in urls]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            soup = BeautifulSoup(response, 'html.parser')
            script_tag = soup.find('script', type="text/javascript")
            if script_tag:
                key_match = re.search(key_regex, script_tag.string if script_tag.string else "")
                if key_match:
                    key = key_match.group(1)
                    
                    time_taken = time.time() - start_time  # Calculate time taken

                    # Define the response dictionary
                    response_data = {
                        "key": key,
                        "time_taken": f"{time_taken:.2f} seconds",
                        "discord": "https://discord.com/invite/6thZAj3u5k",
                        "credit": "not.xoxo & Jova"
                    }
                    
                    return jsonify(response_data)

        return jsonify({"error": "Key not found"}), 404

if __name__ == '__main__':
    app.run(host="192.168.100.22", port=6969, debug=True)

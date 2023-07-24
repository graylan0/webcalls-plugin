from quart import Quart, request, jsonify
import aiohttp
from github import Github
import os

app = Quart(__name__)

@app.route('/v1', methods=['POST'])
async def handle_instruction():
    instruction = await request.json
    action = instruction['action']

    if action == 'scrape_url':
        url = instruction['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        return jsonify({'content': content})

    elif action == 'rest_api_call':
        url = instruction['url']
        method = instruction['http_method']
        headers = instruction.get('payload_headers', {})
        body = instruction.get('payload_body', {})
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=body) as response:
                content = await response.text()
        return jsonify({'content': content})

    elif action == 'grab_github_repo':
        repo_url = instruction['repo_url']
        g = Github(os.getenv("GITHUB_TOKEN"))
        repo = g.get_repo(repo_url)
        files = []
        for file in repo.get_contents(""):
            files.append(file.path)
        return jsonify({'content': files})

    else:
        return jsonify({'error': 'Invalid action'}), 400

if __name__ == "__main__":
    app.run(port=5000)

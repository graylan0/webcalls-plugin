from flask import Flask, request, jsonify
import requests
from github import Github
import os

app = Flask(__name__)

@app.route('/v1', methods=['POST'])
def handle_instruction():
    instruction = request.json
    action = instruction['action']

    if action == 'scrape_url':
        url = instruction['url']
        response = requests.get(url)
        content = response.text
        return jsonify({'content': content})

    elif action == 'rest_api_call':
        url = instruction['url']
        method = instruction['http_method']
        headers = instruction.get('payload_headers', {})
        body = instruction.get('payload_body', {})
        response = requests.request(method, url, headers=headers, data=body)
        content = response.text
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


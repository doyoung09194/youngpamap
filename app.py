from flask import Flask, render_template, request, jsonify
from graph import SchoolGraph

app = Flask(__name__)
g = SchoolGraph()

@app.route('/')
def index():
    rooms = g.get_all_rooms()
    return render_template('index.html', rooms=rooms)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    all_rooms = g.get_all_rooms()
    results = [r for r in all_rooms if query in r['id'] or query in r['name']]
    return jsonify(results)

@app.route('/route')
def route():
    start = request.args.get('start', '').strip()
    end = request.args.get('end', '').strip()
    if not start or not end:
        return jsonify({'error': '출발지와 목적지를 입력하세요.'})
    if start not in g.node_info:
        return jsonify({'error': f'출발지 "{start}"를 찾을 수 없습니다.'})
    if end not in g.node_info:
        return jsonify({'error': f'목적지 "{end}"를 찾을 수 없습니다.'})
    cost, path = g.dijkstra(start, end)
    if not path:
        return jsonify({'error': '경로를 찾을 수 없습니다.'})
    description = g.describe_path(path)
    return jsonify({'cost': cost, 'path': path, 'description': description})

if __name__ == '__main__':
    app.run(debug=True)
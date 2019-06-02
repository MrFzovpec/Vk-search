from flask import Flask, render_template, redirect, session, request
import vk_api
import requests, json

domains = ['kinopoisk', 'countryballs_re', 'itpedia_youtube']
count = 20

token = '1b5b12671b5b12671b5b12676a1b31d64311b5b1b5b126747b25945950b5e9e27619952'

app = Flask(__name__)
how = 0
app.secret_key = 'jrfasefasefgj'

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/find/<id>/', methods=['GET'])
def find(id, how=how):
    query = request.args['query']
    session['query'] = query
    offset = int(id) * 5
    posts = []
    if int(id) == 0:
        for domain in domains:
            url = "https://api.vk.com/method/wall.search?domain={}&access_token={}&v=5.74&query={}".format(
                domain,
                token,
                query
            )
            response = requests.get(url)
            answer = json.loads(response.text)
            how += answer['response']['count']
        session['how'] = how
    else:
        how = session['how']
    for domain in domains:
        url = "https://api.vk.com/method/wall.search?domain={}&access_token={}&v=5.74&query={}&offset={}".format(domain,
                                                                                                                 token,
                                                                                                                 query,
                                                                                                                 offset)
        response = requests.get(url)
        answer = json.loads(response.text)
        for item in answer['response']['items']:
            if item['post_type'] != 'reply':
                post = {
                    'author': domain,
                    'post': item['text'],
                    'link': 'https://vk.com/{}?w=wall{}_{}'.format(domain, item['owner_id'], item['id'])
                }
                posts.append(post)
    if how > 10:
        how = 10
    return render_template('index.html', posts=posts, how=how)

if __name__ == '__main__':
    app.run()

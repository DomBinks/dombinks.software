from flask import Flask, render_template, request
import requests
from datetime import datetime
from os import getenv

app = Flask(__name__)
google_key = getenv('GOOGLE_API_KEY') 

@app.route('/')
def handle_index():
    return render_template('index.html')

@app.route('/british-food-test')
def british_food_test():
    return render_template('british-food-test.html') 

@app.route('/score', methods=['POST'])
def calc_score():
    score = 0
    for i in range(50):
        if request.form.get(str(i+1)):
            score += 1

    if score == 50:
        comment = "You have indulged in all the finest British cuisine"
    elif score > 35:
        comment = "You have experienced the majority of British cuisine" 
    elif score > 25:
        comment = "You have tasted a respectable amount of British cuisine"
    elif score > 10:
        comment = "You have had a minimal amount of British cuisine"
    else:
       comment = "You have barely scraped the surface of British cuisine" 

    return render_template('score.html', score=score, comment=comment)

@app.route('/latest-michael-reeves-upload')
def latest_michael_reeves_upload():
    url = "https://www.googleapis.com/youtube/v3/search?key=" + google_key + "&channelId=UCtHaxi4GTYDpJgMSGy7AeSw&part=snippet,id&order=date&maxResults=1" 
    try:
        response = requests.get(url).json()
    except:
        return False

    title = response['items'][0]['snippet']['title']
    date = response['items'][0]['snippet']['publishedAt'][:-1].replace('T',' ')
    id = response['items'][0]['id']['videoId']
    days = (datetime.today() - datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).days

    return render_template('latest-michael-reeves-upload.html', title=title, date=date, id=id, days=days) 

if __name__ == '__main__':
    app.run()

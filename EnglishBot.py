import json
import os
import random
import requests

def post_message(token, channel, text, ts=None):
	if ts:
		data={"channel": channel,"text": text, "mrkdwn": True, "thread_ts": ts}
	else:
		data={"channel": channel,"text": text, "mrkdwn": True}

	response = requests.post("https://slack.com/api/chat.postMessage",
		headers={"Authorization": "Bearer "+token},
		data = data,
	)

	return response.json()["ts"]


def get_movie_title_and_date(token):
	page_no = str((random.randint(0, 100)))
	
	addr = "https://api.themoviedb.org/3/movie/popular?api_key=%s&language=en-us&page=%s" % (token, page_no)
	response = requests.get(addr)
	json_result = response.json()

	random_no = random.randint(0, len(json_result['results'])-1)

	return json_result['results'][random_no]['original_title'], json_result['results'][random_no]['release_date']


def get_storyline(token, movie_title):
	url = 'https://www.omdbapi.com/?plot=full&apikey=%s&t=%s' % (token, movie_title)
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	response = requests.get(url, headers=headers)
	json_result = response.json()

	if json_result["Response"] == "True":
		return json_result['Plot']
	else:
		return None
	
def punch_text(text):
	padded_articles = [' %s ' % article for article in ["a", "an", "A", "An", "the", "The"]]
	for article in padded_articles:
		text = text.replace(article, " ______ ")

	return text


tmdb_token = os.environ.get('TMDB_TOKEN', None)
omdb_token = os.environ.get('OMDB_TOKEN', None)
slack_token = os.environ.get('SLACK_AUTH_TOKEN', None)

while True:
	movie_title, release_date = get_movie_title_and_date(tmdb_token)
	story_plot = get_storyline(omdb_token, movie_title)

	if story_plot:
		message_original = "*[%s/%s]* %s" % (movie_title, release_date, story_plot)
		message_test = punch_text(message_original)

		if message_test == message_original:
			continue
		else:
			break

ts = post_message(slack_token, "#english-study", message_test)
post_message(slack_token, "#english-study", message_original, ts)






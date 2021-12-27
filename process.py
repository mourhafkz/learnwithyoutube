from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        vlist = request.form['vlist']
        processed = cloud_process(vlist)
        if processed != "error":
            # the file works so there's no need to recheck
            return jsonify(
                {'data': processed})
        else:
            return jsonify({'error': 'Something is wrong with the list. We could not process it.'})
    else:
        return 'GET request successfully'


def cloud_process(vlist):
    try:
        # songs = ['https://www.youtube.com/watch?v=Qpk4bJOls0g',  # careless whisper
        #          # 'https://www.youtube.com/watch?v=FWT9FJ7aQq4',  # grun grun
        #          # 'https://www.youtube.com/watch?v=E-Fj5HkK6AU',  # nina
        #          'https://www.youtube.com/watch?v=VMc3UHP7TM4',  # my way
        #          # 'https://www.youtube.com/watch?v=wliJGLli3jU',  # hex
        #          'https://www.youtube.com/watch?v=f-Wypwi9UBc',  # baby shark
        #          'https://www.youtube.com/watch?v=TBuIGBCF9jc'  # baby shark
        #          ]
        songs = [x for x in vlist.split('\n')]
        texts = {}
        for song in songs:
            if song:
                video_id, video_title = find_info(song)
                timed_captions, text = find_captions(video_id)
                # sents = split_sentence(text)
                texts[video_id] = {'id': video_id, 'title': video_title, 'sents': text, 'timed_captions': timed_captions}
        # print(texts)
        sorted_list = sort_by_density(texts)
        print_report(sorted_list)
        return sorted_list
    except:
        return "error"


def print_report(sorted_list):
    print("################################### REPORT ######################################")
    n = 1
    for s_id, s_info in sorted_list.items():
        print(str(n) + "- song:" + s_info['title'])
        print(" #### Lexical Diversity Score = " +
              "tokens:" + str(s_info['tokens']) + "/" +
              "types:" + str(s_info['types']) + "=" +
              str(s_info["ld_score"]))
        n += 1
    print("#################################################################################")


def lexical_diversity(text):
    tokens = len(text)
    types = len(set(text.strip().split(' ')))
    ld = tokens / types
    return ld, tokens, types


def percentage(count, total):
    return 100 * count / total


def find_info(link):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            link,
            download=False  # We just want to extract the info
        )
    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result
    # print information from the video
    # print(video)
    return video['id'], video['title']


def find_captions(video_id):
    # find the srt of the video
    timed_caption = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])  # 'de',
    extract_list = [d['text'] for d in timed_caption]
    extract_text = ' '.join(extract_list)

    return timed_caption, extract_text


def sort_by_density(texts):
    for key in texts:
        ld, tokens, types = lexical_diversity(texts[key]['sents'])
        texts[key]['ld_score'] = ld
        texts[key]['tokens'] = tokens
        texts[key]['types'] = types
        if ld >= 18:
            texts[key]['level'] = "easy"
        elif 10 <= ld < 18:
            texts[key]['level'] = "intermediate"
        else:
            texts[key]['level'] = "difficult"

    sorted_texts = {k: v for k, v in sorted(texts.items(), key=lambda k_v: k_v[1]['ld_score'], reverse=True)}
    # texts
    # print(sorted_texts)
    return sorted_texts


if __name__ == '__main__':
    app.run(debug=True)

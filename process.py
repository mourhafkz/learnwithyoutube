from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
from flask import Flask, render_template, request, jsonify
from mtld_method import mtld_score, remove_punc, convert_to_list

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        vlist = request.form['vlist']
        lang = [request.form['lang']]
        method = request.form['method']
        # print(method)
        processed = cloud_process(vlist, lang, method)
        # print(processed)
        if processed != "error":
            # the file works so there's no need to recheck
            return jsonify(
                {'data': processed})
        else:
            return jsonify({'error': 'Something is wrong with the list. We could not process it.'})
    else:
        return 'GET request successfully'


def cloud_process(vlist, lang, method):
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
                timed_captions, text = find_captions(video_id, lang)
                # sents = split_sentence(text)
                texts[video_id] = {'id': video_id, 'title': video_title, 'sents': text,
                                   'timed_captions': timed_captions}
        # print(texts)
        sorted_list = sort_by_density(texts, method)
        # print(sorted_list)
        return sorted_list
    except:
        return "error"


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


def find_captions(video_id, lang):
    # find the srt of the video
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    if transcript_list.find_transcript(lang):
        # print(transcript_list.find_transcript(lang))
        # print("found")
        timed_caption = YouTubeTranscriptApi.get_transcript(video_id, languages=lang)  # ['en'] 'de',
    else:
        # print(transcript_list.find_transcript(lang))
        # print("not found")
        timed_caption = [{'text': 'no available lyrics in the language specified', 'start': 0, 'duration': 0}]

    extract_list = [d['text'] for d in timed_caption]
    extract_text = ' '.join(extract_list)
    # print(timed_caption)
    return timed_caption, extract_text


def sort_by_density(texts, method):
    if method == "TTR":
        for key in texts:
            ld, tokens, types = lexical_diversity(texts[key]['sents'])
            texts[key]['ld_score'] = ld
            texts[key]['tokens'] = tokens
            texts[key]['types'] = types
            if ld >= 5:
                texts[key]['level'] = "easy"
            elif 3 <= ld < 5:
                texts[key]['level'] = "intermediate"
            else:
                texts[key]['level'] = "difficult"

    else:
        for key in texts:
            mtld = mtld_score(texts[key]['sents'])
            texts[key]['ld_score'] = mtld

            # based on Duran et al scale (Duran, Malvern, Richards, Chipere 2004:238)
            if mtld >= 80:
                texts[key]['level'] = "difficult"
            elif 30 <= mtld < 80:
                texts[key]['level'] = "intermediate"
            else:
                texts[key]['level'] = "easy"


    sorted_texts = {k: v for k, v in sorted(texts.items(), key=lambda k_v: k_v[1]['ld_score'], reverse=True)}

    print_ttr_report(sorted_texts) if method == "TTR" else print_mtld_report(sorted_texts)

    return sorted_texts


def lexical_diversity(text):
    new_text = convert_to_list(remove_punc(text))
    tokens = len(new_text)
    types = len(set(new_text))
    # types = len(set(text.strip().split(' ')))
    ld = tokens / types
    return ld, tokens, types


def print_ttr_report(sorted_list):
    print("################################### REPORT ######################################")
    n = 1
    for s_id, s_info in sorted_list.items():
        print(str(n) + "- song: " + s_info['title'])
        print("\x1b[1;32;40m" + "Lexical Diversity Score =" + "\x1b[0m" + " tokens:" +
              "\x1b[1;31;40m" + str(s_info['tokens']) + "\x1b[0m" + "/" + "types:" +
              "\x1b[1;31;40m" + str(s_info['types']) + "\x1b[0m" + " =   " +
              "\x1b[1;32;40m" + str(s_info["ld_score"]) + "\x1b[0m"
              )
        n += 1
    print("#################################################################################")

def print_mtld_report(sorted_list):
    print("################################### REPORT ######################################")
    n = 1
    for s_id, s_info in sorted_list.items():
        print(str(n) + "- song: " + s_info['title'])
        print("\x1b[1;32;40m" + "MTLD score =" +
              "\x1b[1;32;40m" + str(s_info["ld_score"]) + "\x1b[0m"
              )
        n += 1
    print("#################################################################################")



if __name__ == '__main__':
    app.run(debug=True)

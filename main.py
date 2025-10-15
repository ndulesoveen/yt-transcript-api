from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "No video_id"}), 400
    try:
        transcript = YouTubeTranscriptApi.list_transcripts(video_id)
        # Ищем нужный язык
        try:
            ru_transcript = transcript.find_transcript(['ru', 'en']).fetch()
        except Exception:
            # Если нет RU/EN — пробуем авто
            ru_transcript = transcript.find_manually_created_transcript(['en','ru']).fetch()
        aggregated = " ".join([item["text"] for item in ru_transcript])
        return jsonify({"transcript": aggregated})
    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return jsonify({"error": "Transcript not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000)

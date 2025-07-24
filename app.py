from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/get_transcript')
def get_transcript():
    """API endpoint to fetch the transcript for a given video ID."""
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({"error": "Video ID is missing."}), 400

    try:
        # Fetch the transcript using the library
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript into a single string
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        return jsonify({"transcript": full_transcript})

    except NoTranscriptFound:
        return jsonify({"error": "No transcript could be found for this video. It may be private, deleted, or not have captions."}), 404
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 403
    except Exception as e:
        # Catch any other potential errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the app on a local development server
    app.run(debug=True)
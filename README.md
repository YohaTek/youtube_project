# YouTube Transcript Extractor

A small Flask web app: paste a YouTube video URL and read its transcript in the
browser. The URL is parsed client-side into a video ID, and the server fetches
the captions with
[`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api)
and returns them as plain text.

## How it works

- `templates/index.html` — single-page UI (inline CSS/JS). Extracts the 11-character
  video ID from `youtube.com/watch?v=...`, `youtu.be/...`, or embed URLs and calls
  the backend.
- `app.py` — Flask app with two routes:
  - `GET /` serves the page.
  - `GET /get_transcript?videoId=<id>` fetches the transcript from YouTube and
    returns `{"transcript": "..."}` as JSON.

## Project layout

```
app.py               Flask application and transcript endpoint
templates/
  index.html         Browser UI and client-side video ID parsing
requirements.txt     Python runtime dependencies
```

## Prerequisites

- Python 3.9 or newer
- Network access to YouTube (transcripts are fetched on the server, not the
  browser)

## Setup and run

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000> and paste a video URL.

`requirements.txt` pins `youtube-transcript-api` below 1.0 because the app uses
the class-level `YouTubeTranscriptApi.get_transcript()` helper, which was replaced
by the instance-based `fetch()` / `list()` API in 1.0.

## API

`GET /get_transcript?videoId=<video-id>`

| Status | Body | Meaning |
| --- | --- | --- |
| `200` | `{"transcript": "..."}` | Captions found and flattened to one string |
| `400` | `{"error": "Video ID is missing."}` | No `videoId` query parameter |
| `403` | `{"error": "Transcripts are disabled for this video."}` | Uploader disabled captions |
| `404` | `{"error": "No transcript could be found ..."}` | No captions, private, or deleted video |
| `500` | `{"error": "An unexpected error occurred: ..."}` | Anything else, including upstream request failures |

Example:

```sh
curl "http://127.0.0.1:5000/get_transcript?videoId=dQw4w9WgXcQ"
```

## Notes and limitations

- `app.run(debug=True)` is a local development server only; do not expose it as-is.
- Only captions that YouTube already provides are used — no speech-to-text
  fallback, and auto-generated captions depend on the video.
- The page heading reads "Transcript for Video ID: ..." because the app does not
  fetch video titles.
- There is no automated test suite yet; changes are verified by running the app
  and exercising the endpoint above.

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def get_transcript(video_id: str = 'Gfr50f6ZBvo'):
  try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    transcript = " ".join(chunk['text'] for chunk in transcript_list)
    return transcript
  except TranscriptsDisabled:
    print("Transcript not available")
  except Exception as e:
    print(e)

  return None

if __name__ == '__main__':
  video_id = "Gfr50f6ZBvo"
  get_transcript(video_id)
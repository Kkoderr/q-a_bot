from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def get_transcript(video_id: str = 'Gfr50f6ZBvo'):
  try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','en-IN','en-US','en-GB'])
    transcript = " ".join(chunk['text'] for chunk in transcript_list)
    return transcript
  except TranscriptsDisabled:
    print("Transcript not available")
  except Exception as e:
    print(e)

  return None

if __name__ == '__main__':
  video_id = "iaeBnYLNXgQ"
  print(get_transcript(video_id))
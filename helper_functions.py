import re
import unicodedata

def resize_video(width, height, max_width = 600):

  if width > max_width:
    proportion = width / height
    video_width = max_width
    video_height = int(video_width / proportion)
  else:
    video_width = width
    video_height = height

  return video_width, video_height

def remover_caracteres_especiais(texto):
    texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))
    texto = re.sub(r'[^a-zA-Z0-9]+', '', texto)
    texto = texto.lower()
    return texto
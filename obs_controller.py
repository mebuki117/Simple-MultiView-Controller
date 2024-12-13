import obspython as S
import os
import re

version = '0.10.0'

# --- Options ---
browser_format = 'Player '  # brower source format
normal_scene_name = 'Normal'
focus_scene_name = 'Focus'
autosetName = False  # auto set a name to the text source
name_text_format = 'Name '  # text source format

# defs
def updateURL(): 
  path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\names.txt'
  with open(path, encoding='utf-8') as f:
    id = f.read().splitlines()
  
  for l in range(len(id)-1):
    browser_source = S.obs_get_source_by_name(f'{browser_format}{l+1}')
    settings = S.obs_source_get_settings(browser_source)
    url = generate_embed_url(id[l])
    if id[l] == '':
      url = ''
    S.obs_data_set_string(settings, 'url', url)
    S.obs_source_update(browser_source, settings)
    S.obs_source_release(browser_source)
    S.obs_data_release(settings)

    if int(id[len(id)-1]) == len(id)-1:
      normal_scene = S.obs_get_scene_by_name(normal_scene_name)
      normal_scene_source = S.obs_scene_get_source(normal_scene)
      S.obs_frontend_set_current_scene(normal_scene_source)
      S.obs_source_release(normal_scene_source)
    elif int(id[len(id)-1]) != -1:
      focus_scene = S.obs_get_scene_by_name(focus_scene_name)
      focus_scene_source = S.obs_scene_get_source(focus_scene)
      S.obs_frontend_set_current_scene(focus_scene_source)
      S.obs_source_release(focus_scene_source)

    if autosetName:
      path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\id_to_name.txt'
      try:
        with open(path, 'x', encoding='utf-8') as f:
          f.write('')
      except FileExistsError:
        pass
      with open(path, encoding='utf-8') as f:
        idname = f.read().splitlines()
      name_text = S.obs_get_source_by_name(f'{name_text_format}{l+1}')
      settings = S.obs_source_get_settings(name_text)
      name = ''
      for n in range(len(idname)):
        if f'{id[l]}' and f'{id[l]}' in idname[n]:
          split = idname[n].replace(' : ', ';')
          idname_list = split.split(';')
          name = idname_list[0]
      S.obs_data_set_string(settings, 'text', name)
      S.obs_source_update(name_text, settings)
      S.obs_source_release(name_text)
      S.obs_data_release(settings)

def generate_embed_url(url: str) -> str:
  youtube_pattern = r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
  twitch_pattern = r'https?://(?:www\.)?twitch\.tv/([a-zA-Z0-9_-]+)'

  youtube_match = re.match(youtube_pattern, url)
  twitch_match = re.match(twitch_pattern, url)

  if youtube_match:
    video_id = youtube_match.group(1)
    print(video_id)
    return f'https://www.youtube.com/embed/{video_id}?autoplay=1&controls=0&rel=0&modestbranding=1&mute=1'
  elif twitch_match:
    channel_id = twitch_match.group(1)
    return f'https://player.twitch.tv/?channel={channel_id}&enableExtensions=true&muted=true&parent=twitch.tv&player=popout&quality=chunked&volume=0.01'
  else:
    print('Invalid URL. Please provide a valid YouTube or Twitch link.')
    return ''

def execute():
  try:
    updateURL()
  except Exception as e:
    print(e)
  
def script_description():
  return f'Simple MultiView OBS Controller v{version}'

def script_update(settings):
  S.timer_remove(execute)
  S.timer_add(execute, 1000)

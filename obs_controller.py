import obspython as S
import os

version = '0.2.0'

# --- Option ---
browser_format = 'Player '  # brower source format

# defs
def updateURL(): 
  path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\names.txt'
  with open(path) as f:
    name = f.read().splitlines()

  for l in range(len(name)):
    source = S.obs_get_source_by_name(f'{browser_format}{l+1}')
    settings = S.obs_source_get_settings(source)
    url = f'https://player.twitch.tv/?channel={name[l]}&enableExtensions=true&muted=true&parent=twitch.tv&player=popout&quality=chunked&volume=0.01'
    if name[l] == '':
      url = ''
    S.obs_data_set_string(settings, 'url', url)
    S.obs_source_update(source, settings)
    S.obs_source_release(source)
    S.obs_data_release(settings)

def execute():
  try:
    updateURL()
  except Exception as e:
    print(e)
  
def script_description():
  return f'Simple MultiView OBS Controller v{version}'

def script_update(settings):
  S.timer_remove(execute)
  S.timer_add(execute, 100)

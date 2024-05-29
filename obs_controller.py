import obspython as S
import os

version = '0.4.0'

# --- Option ---
browser_format = 'Player '  # brower source format
focus_scene_name = 'Focus'
normal_scene_name = 'Normal'

# defs
def updateURL(): 
  path = f'{os.path.dirname(os.path.realpath(__file__))}\\data\\names.txt'
  with open(path) as f:
    name = f.read().splitlines()
  
  for l in range(len(name)-1):
    browser_source = S.obs_get_source_by_name(f'{browser_format}{l+1}')
    settings = S.obs_source_get_settings(browser_source)
    url = f'https://player.twitch.tv/?channel={name[l]}&enableExtensions=true&muted=true&parent=twitch.tv&player=popout&quality=chunked&volume=0.01'
    if name[l] == '':
      url = ''
    S.obs_data_set_string(settings, 'url', url)
    S.obs_source_update(browser_source, settings)
    S.obs_source_release(browser_source)
    S.obs_data_release(settings)

    if int(name[len(name)-1]) == len(name)-1:
      normal_scene = S.obs_get_scene_by_name(normal_scene_name)
      normal_scene_source = S.obs_scene_get_source(normal_scene)
      S.obs_frontend_set_current_scene(normal_scene_source)
      S.obs_source_release(normal_scene_source)
    elif int(name[len(name)-1]) != -1:
      focus_scene = S.obs_get_scene_by_name(focus_scene_name)
      focus_scene_source = S.obs_scene_get_source(focus_scene)
      S.obs_frontend_set_current_scene(focus_scene_source)
      S.obs_source_release(focus_scene_source)

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

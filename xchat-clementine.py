"""Sadly I have no idea if this[1] really is the scripts origin, but it
   looks like it is.
   If you know who to credit for this version 1.0, please let me know.

   [1] http://pastebin.com/dhnRyXAT
"""

__module_name__ = "xchat-clementine"
__module_version__ = "2.0"
__module_description__ = "Control Clementine from Xchat"
from dbus import Bus, DBusException
import xchat
bus = Bus(Bus.TYPE_SESSION)

def get_clem():
  try:
    return bus.get_object('org.mpris.clementine', '/Player')
  except DBusException:
    print "\x02Either Clementine is not running or you have something wrong with your D-Bus setup."
    return None

def command_np(word, word_eol, userdata):
  clem = get_clem()
  
  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemmd = clemp.GetMetadata()
    
    try:
      artist = clemmd['artist']
      album  = clemmd['album']
      title  = clemmd['title']
    except DBusException:
      print "\x02Can't extract information. File might be insufficently tagged."
      return None

    output = unicode(artist).encode('utf-8') \
           + " - " \
           + unicode(album).encode('utf-8') \
           + " - " \
           + unicode(title).encode('utf-8')

    xchat.command("me np: " + output)
  return xchat.EAT_ALL

def command_next(word, eord_eol, userdata):
  clem = get_clem()

  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemp.Next()

  return xchat.EAT_ALL

def command_prev(word, eord_eol, userdata):
  clem = get_clem()
  
  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemp.Prev()

  return xchat.EAT_ALL

def command_play(word, eord_eol, userdata):
  clem = get_clem()
  
  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemp.Play()

  return xchat.EAT_ALL

def command_stop(word, eord_eol, userdata):
  clem = get_clem()

  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemp.Stop()

  return xchat.EAT_ALL

def command_pause(word, eord_eol, userdata):
  clem = get_clem()

  if clem:
    clemp = bus.get_object('org.mpris.clementine', '/Player')
    clemp.Pause()

  return xchat.EAT_ALL

xchat.hook_command("NP",    command_np,    help="Displays current playing song.")
xchat.hook_command("NEXT",  command_next,  help="Skips the current playing song.")
xchat.hook_command("Prev",  command_prev,  help="Plays the last played song again.")
xchat.hook_command("Play",  command_play,  help="Starts playing.")
xchat.hook_command("Stop",  command_stop,  help="Stops current playing song.")
xchat.hook_command("Pause", command_pause, help="Pauses the current playing song.")
print "xchat-clementine plugin loaded"

import os
import vlc
import time
from datetime import datetime, timedelta
import subprocess

media_list_player = vlc.MediaListPlayer()
media_list = vlc.MediaList()

video_dir = "/home/test/Desktop/videos"

password = input("Bilgisayar şifrenizi girin: ")

# Dizin içindeki mp4 dosyalarını medya listesine ekle
for file_name in os.listdir(video_dir):
    if file_name.endswith(".mp4"):
        file_path = os.path.join(video_dir, file_name)
        media_list.add_media(vlc.Media(file_path))

media_list_player.set_media_list(media_list)

media_player = media_list_player.get_media_player()

# Oynatma saatleri (8:30 - 17:30 arası)
start_time = "11:50:00"
end_time = "17:30:00"

start_datetime = datetime.strptime(start_time, "%H:%M:%S")
end_datetime = datetime.strptime(end_time, "%H:%M:%S")


def is_working_hours():
    current_time = datetime.now().time()
    current_day = datetime.now().strftime("%A")
    if current_day != "Saturday" and current_day != "Sunday" and start_datetime.time() <= current_time <= end_datetime.time():
        return True
    else:
        return False


# Medya oynatma döngüsü
while True:
    if is_working_hours():
        media_list_player.play()
        time.sleep(1)
        if media_list_player.is_playing():
            continue
        else:
            media_list_player.stop()
            time.sleep(1)
    else:
        command = ["sudo", "-S", "systemctl", "suspend"]
        subprocess.run(command, input=f"{password}\n", text=True)
        wake_time = datetime.combine(datetime.today(), start_datetime.time())
        if wake_time < datetime.now():
            wake_time += timedelta(days=1)
        time_to_wake = (wake_time - datetime.now()).seconds
        time.sleep(time_to_wake)

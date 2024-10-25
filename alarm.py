import datetime
import os
import time
import winsound
import pygame
import threading

def play_continuous_sound(sound_file):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_file)
    sound.play(-1)

def stop_continuous_sound():
    pygame.mixer.stop()

def set_alarm_time(alarm_date, alarm_time, am_pm):
    alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
    if am_pm == "PM" and alarm_hour != 12:
        alarm_hour += 12
    elif am_pm == "AM" and alarm_hour == 12:
        alarm_hour = 0
    return datetime.datetime.combine(alarm_date, datetime.time(alarm_hour, alarm_minute, 0))

def play_tone(tone, custom_sound_file=None):
    pygame.init()
    if tone == "beep":
        pygame.mixer.music.load("beep.wav")
        pygame.mixer.music.play()
        sound_file = "beep.wav"
    elif tone == "ding":
        pygame.mixer.music.load("ding.wav")
        pygame.mixer.music.play()
        sound_file = "ding.wav"
    elif tone == "custom":
        if custom_sound_file is None:
            custom_sound_file = input("Enter the path to your custom sound file: ")
        pygame.mixer.music.load(custom_sound_file)
        pygame.mixer.music.play()
        sound_file = custom_sound_file
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        print("Invalid tone. Using default beep.")
        pygame.mixer.music.load("beep.wav")
        pygame.mixer.music.play()
    pygame.quit()

def handle_snooze(snooze_time):
    time.sleep(snooze_time * 60)

def set_alarm(alarm_date, alarm_time, am_pm, tone, snooze_time, custom_sound_file=None):
    alarm_time = set_alarm_time(alarm_date, alarm_time, am_pm)
    while True:
        now = datetime.datetime.now()
        if now >= alarm_time:
            print("Wake up!")
            if tone == "custom":
                threading.Thread(target=play_continuous_sound, args=(custom_sound_file,)).start()
            else:
                threading.Thread(target=play_continuous_sound, args=(tone+".wav",)).start()
            while True:
                response = input("Snooze for {} minutes? (y/n) ".format(snooze_time))
                if response.lower() == "y":
                    stop_continuous_sound()
                    handle_snooze(snooze_time)
                    if tone == "custom":
                        threading.Thread(target=play_continuous_sound, args=(custom_sound_file,)).start()
                    else:
                        threading.Thread(target=play_continuous_sound, args=(tone+".wav",)).start()
                else:
                    stop_continuous_sound()
                    exit()

def main():
    print("Alarm Clock")
    alarm_date = input("Enter alarm date (YYYY-MM-DD): ")
    alarm_date = datetime.datetime.strptime(alarm_date, "%Y-%m-%d").date()
    (alarm_time, am_pm) = input("Enter alarm time (HH:MM am/pm): ").split(" ")
    tone = input("Enter tone (beep, ding, custom): ")
    if tone == "custom":
        custom_sound_file = input("Enter the path to your custom sound file: ")
    else:
        custom_sound_file = None
    snooze_time = int(input("Enter snooze time (minutes): "))
    set_alarm(alarm_date, alarm_time, am_pm, tone, snooze_time, custom_sound_file)

if __name__ == "__main__":
    main()
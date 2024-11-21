from moviepy import *
from PIL import Image
import os
import ffmpeg


def file_thumbnail(source_path):
    # Загрузка видеофайла
    name = os.path.splitext(os.path.basename(source_path))[0]

    # Создание папки для thumbnail
    thumbnails_dir = "static/thumbnails"
    os.makedirs(thumbnails_dir, exist_ok=True)
    new_image_filepath = os.path.join(thumbnails_dir, f"{name}_thumbnail.jpg")
    if os.path.isfile(new_image_filepath ):
        return new_image_filepath
    else:
        # Создание объекта VideoFileClip
        clip = VideoFileClip(source_path)

        # Получение количества кадров в секунду
        fps = clip.reader.fps

        # Получение количества кадров в видео
        nframes = clip.reader.n_frames

        # Получение длительности видео в секундах
        duration = clip.duration

        # Создание thumbnail на определенном кадре
        frame_at_second = float(duration * 10 / 100)
        frame = clip.get_frame(frame_at_second)

        # Сохранение thumbnail в файл
        new_image = Image.fromarray(frame)
        new_image.save(new_image_filepath)
        return new_image_filepath


def get_audio_tracks(video_file):
    probe = ffmpeg.probe(video_file)
    audio_tracks = []

    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            audio_tracks.append({
                'index': stream['index'],
                'codec': stream['codec_name'],
                'language': stream.get('tags', {}).get('language', 'und')
            })

    return audio_tracks

def display_audio_menu(audio_tracks):
    print("Выберите аудиодорожку:")
    for i, track in enumerate(audio_tracks):
        print(f"{i + 1}. {track['language']} ({track['codec']})")

    choice = int(input("Введите номер аудиодорожки: ")) - 1
    return audio_tracks[choice]['index'] if 0 <= choice < len(audio_tracks) else None

def create_menu(video_file):
    audio_tracks = get_audio_tracks(video_file)

    if audio_tracks:
        selected_track_index = display_audio_menu(audio_tracks)
        print(f"Выбрана аудиодорожка с индексом: {selected_track_index}")
    else:
        print("Аудиодорожки не найдены.")
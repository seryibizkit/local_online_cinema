// Получаем список видеофайлов и их кадров
fetch('/video_list')
    .then(response => response.json())
    .then(data => {
        // Создаем список видеофайлов
        const videoList = document.getElementById('video-list');
        data.forEach(video => {
            const li = document.createElement('li');
            li.innerHTML = `<img src="${video.frames[0]}"> ${video.file}`;
            videoList.appendChild(li);
        });
    });

// Обработчик клика по видеофайлу
document.addEventListener('click', e => {
    if (e.target.tagName === 'LI') {
        const videoFile = e.target.innerHTML.split(' ')[2];
        const videoPlayer = document.getElementById('video-player');
        videoPlayer.src = `static/video/${videoFile}`;
        videoPlayer.load();
        videoPlayer.play();
    }
});

// Обработчик события воспроизведения видео
const videoPlayer = document.getElementById('video-player')
videoPlayer.addEventListener('play', () => {
    // Сохраняем текущее время воспроизведения
    const video = videoPlayer.currentTime;
    localStorage.setItem('videoTime', video);
    localStorage.setItem('video', videoPlayer.src)
});

// Обработчик события загрузки страницы
window.addEventListener('load', () => {
    // Восстанавливаем время воспроизведения при загрузке страницы
    const videoTime = localStorage.getItem('videoTime');
    const video = localStorage.getItem('video');
    if (videoTime) {
        const videoPlayer = document.getElementById('video-player');
        videoPlayer.src = `${video}`;
        videoPlayer.currentTime = videoTime;
    }

});

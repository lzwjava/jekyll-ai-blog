document.addEventListener("DOMContentLoaded", function () {
    var playAudioButton = document.getElementById('playAudioButton');
    if (playAudioButton) {
        playAudioButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default anchor behavior

            // Extract the base filename without the extension
            var filePath = playAudioButton.getAttribute('data-file-path'); // e.g., "pages/donate-en.md"
            var fileName = filePath.split('/').pop().replace('.md', ''); // e.g., "donate-en"

            // Set the audio source to the corresponding MP3 file
            var audioFile = '/assets/audios/' + fileName + '.mp3'; // e.g., "/assets/audios/donate-en.mp3"

            var audioPlayer = document.getElementById('audioPlayer');
            var audioSource = document.getElementById('audioSource');

            audioSource.src = audioFile;
            audioPlayer.style.display = 'block'; // Show the audio player
            audioPlayer.load();
            audioPlayer.play();
        });
    }

});

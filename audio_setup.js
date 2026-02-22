// Add this note at the top of app.js explaining the audio setup
/*
 * AUDIO PLAYER SETUP:
 * The audio player now uses real HTML5 audio with sample music files.
 * To use your own Tamil recitation audio files:
 * 1. Place your .mp3 files in an 'audio' folder
 * 2. Update the audioUrl in playlistData below with your file paths
 * Example: audioUrl: "audio/thirumurugaatruppadai.mp3"
 */

// Add this helper function to create the audio element
function initAudioElement() {
    let audio = document.getElementById('audioPlayer');
    if (!audio) {
        audio = document.createElement('audio');
        audio.id = 'audioPlayer';
        audio.preload = 'metadata';
        document.body.appendChild(audio);
    }
    return audio;
}

// Add volume control
function addVolumeControl() {
    const audioPlayerContainer = document.querySelector('.audio-player');
    if (!audioPlayerContainer || document.getElementById('volumeControl')) return;

    const volumeHTML = `
        <div class="volume-control" style="margin-top: 1rem; display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 1.2rem;">🔊</span>
            <input type="range" id="volumeSlider" min="0" max="100" value="70" 
                   style="flex: 1; cursor: pointer;">
            <span id="volumeValue" style="font-family: 'Poppins', sans-serif; font-size: 0.9rem;">70%</span>
        </div>
    `;

    audioPlayerContainer.insertAdjacentHTML('beforeend', volumeHTML);

    const volumeSlider = document.getElementById('volumeSlider');
    const volumeValue = document.getElementById('volumeValue');

    volumeSlider.addEventListener('input', (e) => {
        const volume = e.target.value / 100;
        if (audioPlayer) audioPlayer.volume = volume;
        volumeValue.textContent = e.target.value + '%';
    });
}

// Call this after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        addVolumeControl();
    }, 100);
});

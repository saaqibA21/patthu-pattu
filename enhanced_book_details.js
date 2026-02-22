// Enhanced Book Details Function with Full Text Support
// Add this to app.js or replace the existing openBookDetails function

function openBookDetailsEnhanced(bookId) {
    const book = booksData.find(b => b.id === bookId);
    if (!book) return;

    // Get full text data
    const textData = pathuPattuTexts[bookId] || {};
    const fullText = currentLang === 'ta' ? textData.fullTextTa : textData.fullTextEn;
    const sampleVerses = currentLang === 'ta' ? textData.sampleVersesTa : textData.sampleVersesEn;

    // Create modal
    const modal = document.createElement('div');
    modal.className = 'book-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeBookModal()"></div>
        <div class="modal-content">
            <button class="modal-close" onclick="closeBookModal()">✕</button>
            <div class="modal-header">
                <h1>${currentLang === 'ta' ? book.titleTa : book.titleEn}</h1>
                <p class="modal-subtitle">${currentLang === 'ta' ? book.subtitleTa : book.subtitleEn}</p>
            </div>
            <div class="modal-body">
                <!-- Description Section -->
                <div class="modal-section">
                    <h3>${currentLang === 'ta' ? 'விவரம்' : 'Description'}</h3>
                    <p>${currentLang === 'ta' ? book.descriptionTa : book.descriptionEn}</p>
                    <p>${currentLang === 'ta' ? book.detailsTa : book.detailsEn}</p>
                </div>
                
                <!-- Info Grid -->
                <div class="modal-info-grid">
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'கவிஞர்' : 'Poet'}</h4>
                        <p>${currentLang === 'ta' ? book.poetTa : book.poetEn}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'வரிகள்' : 'Lines'}</h4>
                        <p>${book.lines}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'காலம்' : 'Period'}</h4>
                        <p>${currentLang === 'ta' ? book.periodTa : book.periodEn}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'கருப்பொருள்' : 'Theme'}</h4>
                        <p>${currentLang === 'ta' ? book.themeTa : book.themeEn}</p>
                    </div>
                </div>
                
                <!-- Sample Verses Section -->
                ${sampleVerses ? `
                <div class="modal-section">
                    <h3>📜 ${currentLang === 'ta' ? 'மாதிரி வரிகள்' : 'Sample Verses'}</h3>
                    <div class="verses-container">
                        ${sampleVerses.map((verse, index) => `
                            <div class="verse-item">
                                <span class="verse-number">${index + 1}</span>
                                <p class="verse-text">${verse}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
                
                <!-- Full Text Section -->
                ${fullText ? `
                <div class="modal-section">
                    <h3>📖 ${currentLang === 'ta' ? 'முழு பாடல்' : 'Full Text'}</h3>
                    <div class="full-text-container">
                        <pre class="full-text">${fullText}</pre>
                    </div>
                </div>
                ` : ''}
                
                <!-- Audio Section -->
                ${textData.audioUrl ? `
                <div class="modal-section">
                    <h3>🎵 ${currentLang === 'ta' ? 'பாராயணம் கேளுங்கள்' : 'Listen to Recitation'}</h3>
                    <div class="audio-section">
                        <audio controls style="width: 100%; margin-top: 1rem;">
                            <source src="${textData.audioUrl}" type="audio/mpeg">
                            ${currentLang === 'ta' ? 'உங்கள் உலாவி ஆடியோவை ஆதரிக்கவில்லை.' : 'Your browser does not support audio.'}
                        </audio>
                        <p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem; font-style: italic;">
                            ${textData.audioNote || (currentLang === 'ta' ? 'பாரம்பரிய பாராயணம்' : 'Traditional recitation')}
                        </p>
                    </div>
                </div>
                ` : ''}
                
                <!-- Download/Share Buttons -->
                <div class="modal-actions">
                    <button class="action-btn" onclick="printBookText(${bookId})">
                        🖨️ ${currentLang === 'ta' ? 'அச்சிடு' : 'Print'}
                    </button>
                    <button class="action-btn" onclick="shareBook(${bookId})">
                        📤 ${currentLang === 'ta' ? 'பகிர்' : 'Share'}
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

// Helper functions for actions
function printBookText(bookId) {
    window.print();
}

function shareBook(bookId) {
    const book = booksData.find(b => b.id === bookId);
    if (!book) return;

    const shareText = currentLang === 'ta'
        ? `${book.titleTa} - பத்து பாட்டு நூல்களில் ஒன்று`
        : `${book.titleEn} - One of the Pathu Pattu books`;

    if (navigator.share) {
        navigator.share({
            title: currentLang === 'ta' ? book.titleTa : book.titleEn,
            text: shareText,
            url: window.location.href
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareText + '\n' + window.location.href)
            .then(() => alert(currentLang === 'ta' ? 'இணைப்பு நகலெடுக்கப்பட்டது!' : 'Link copied!'))
            .catch(err => console.log('Error copying:', err));
    }
}

// Replace the original function call in loadBooks
// Change: bookCard.onclick = () => openBookDetails(book.id);
// To: bookCard.onclick = () => openBookDetailsEnhanced(book.id);

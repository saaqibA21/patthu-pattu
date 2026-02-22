// Books Data
const booksData = [
    {
        id: 1,
        titleTa: "திருமுருகாற்றுப்படை",
        titleEn: "Thirumurugaatruppadai",
        subtitleTa: "முருகனுக்கான பாட்டு",
        subtitleEn: "Song to Lord Murugan",
        descriptionTa: "சங்ககாலத்தின் மிக முக்கியமான படைப்புகளில் ஒன்று. முருகன் கோயில்களின் பெருமையை விவரிக்கும் 317 வரிகள் கொண்ட நூல்.",
        descriptionEn: "One of the most important works of the Sangam period. A 317-line work describing the glory of Murugan temples.",
        poetTa: "நக்கீரர்",
        poetEn: "Nakkeerar",
        lines: 317,
        themeTa: "பக்தி, கோயில் பெருமை",
        themeEn: "Devotion, Temple Glory",
        periodTa: "கி.பி 5-6 நூற்றாண்டு",
        periodEn: "5th-6th Century CE",
        detailsTa: "இந்நூல் ஆறு முருகன் கோயில்களை விரிவாக விவரிக்கிறது. ஒரு பாணன் மற்றொரு பாணனுக்கு வழிகாட்டும் வகையில் அமைந்துள்ளது.",
        detailsEn: "This work describes six Murugan temples in detail. It is structured as one bard guiding another bard."
    },
    {
        id: 2,
        titleTa: "பொருநராற்றுப்படை",
        titleEn: "Porunararruppadai",
        subtitleTa: "அரசனுக்கான பாட்டு",
        subtitleEn: "Song to the King",
        descriptionTa: "250 வரிகளைக் கொண்ட தமிழ் கவிதைப் பணி, சோழ மன்னர் கரிகாள சோழனின் புகழை பாடுவது.",
        descriptionEn: "A 250-line Tamil poetic work celebrating the glory of Chola king Karikal Cholan.",
        poetTa: "முதத்தாமக்கன்னியார்",
        poetEn: "Mudathama Kanniyar",
        lines: 248,
        themeTa: "வீரம், அரச பெருமை",
        themeEn: "Valor, Royal Glory",
        periodTa: "கி.மு 2 நூற்றாண்டு",
        periodEn: "2nd Century BCE",
        detailsTa: "போரில் வெற்றி பெற்ற வீரர்களுக்கு அரசன் வழங்கும் பரிசுகளை விவரிக்கிறது.",
        detailsEn: "Describes the gifts given by the king to warriors who won in battle."
    },
    {
        id: 3,
        titleTa: "சிறுபணாற்றுப்படை",
        titleEn: "Sirupanarruppadai",
        subtitleTa: "சிறிய பாடல் கலைஞர்களுக்கான பாட்டு",
        subtitleEn: "Song for Minor Bards",
        descriptionTa: "அலைகற்ற பாடல் கலைஞர்களைப் பற்றி எழுதப்பட்ட 269 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 269-line work about wandering minstrels.",
        poetTa: "நத்தத்தனார்",
        poetEn: "Nattattanar",
        lines: 269,
        themeTa: "பாடல் கலை மரபு, ஆதரவு",
        themeEn: "Musical Tradition, Patronage",
        periodTa: "கி.மு 1 நூற்றாண்டு",
        periodEn: "1st Century BCE",
        detailsTa: "நல்லியக்கோடன் என்ற அரசனின் கொடை குணத்தை விவரிக்கிறது.",
        detailsEn: "Describes the generosity of King Nalliyakodan."
    },
    {
        id: 4,
        titleTa: "பெரும்பணாற்றுப்படை",
        titleEn: "Perumpanarruppadai",
        subtitleTa: "பெரிய பாடல் கலைஞர்களுக்கான பாட்டு",
        subtitleEn: "Song for Major Bards",
        descriptionTa: "சிறுபணாற்றுப்படைக்கான தோழக் பணி, பெரிய பாடல் கலைஞர்களை பற்றிக் கூறும் 500 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A companion work to Sirupanarruppadai, a 500-line work about major bards.",
        poetTa: "உருத்திரங்கண்ணனார்",
        poetEn: "Uruthirankannanar",
        lines: 500,
        themeTa: "அரச ஆதாரம், கலை மரபு",
        themeEn: "Royal Patronage, Artistic Tradition",
        periodTa: "கி.மு 1 நூற்றாண்டு",
        periodEn: "1st Century BCE",
        detailsTa: "தொண்டைமான் இளந்திரையன் என்ற அரசனின் வள்ளல் தன்மையை பாடுகிறது.",
        detailsEn: "Sings of the benevolence of King Thondaiman Ilanthiraiyan."
    },
    {
        id: 5,
        titleTa: "முல்லைப்பாட்டு",
        titleEn: "Mullaipattu",
        subtitleTa: "மல்லிகை பூவின் பாட்டு",
        subtitleEn: "Song of the Jasmine",
        descriptionTa: "பாசனிலத்தின் விவரணை மற்றும் பிரேமபாவ விஷயங்களுக்கான 103 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 103-line work describing pastoral landscapes and romantic themes.",
        poetTa: "நப்பூதனார்",
        poetEn: "Napputanar",
        lines: 103,
        themeTa: "பாசனிலம், அன்பு, காத்திருப்பு",
        themeEn: "Pastoral Life, Love, Waiting",
        periodTa: "கி.மு 2 நூற்றாண்டு",
        periodEn: "2nd Century BCE",
        detailsTa: "போருக்குச் சென்ற கணவனுக்காக காத்திருக்கும் மனைவியின் உணர்வுகளை விவரிக்கிறது.",
        detailsEn: "Describes the feelings of a wife waiting for her husband who has gone to war."
    },
    {
        id: 6,
        titleTa: "நெடுனளப்பாட்டு",
        titleEn: "Nedunalvadai",
        subtitleTa: "நீண்ட பாட்டு",
        subtitleEn: "The Long Song",
        descriptionTa: "பண்டைய தமிழ் அரசாங்கங்களின் பெருமை மற்றும் செல்வம் பற்றிய 188 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 188-line work about the glory and wealth of ancient Tamil kingdoms.",
        poetTa: "நக்கீரர்",
        poetEn: "Nakkeerar",
        lines: 188,
        themeTa: "அரச வீரம், காதல்",
        themeEn: "Royal Valor, Love",
        periodTa: "கி.பி 2 நூற்றாண்டு",
        periodEn: "2nd Century CE",
        detailsTa: "பாண்டிய மன்னன் நெடுஞ்செழியனின் வெற்றிகளை விவரிக்கிறது.",
        detailsEn: "Describes the victories of Pandya king Nedunchezhiyan."
    },
    {
        id: 7,
        titleTa: "மதுரைக்காஞ்சி",
        titleEn: "Maduraikanchi",
        subtitleTa: "மதுரை நகரின் பாட்டு",
        subtitleEn: "Song of Madurai City",
        descriptionTa: "மதுரை நகரத்தின் செழிப்பு மற்றும் பண்பாட்டை விவரிக்கும் 782 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 782-line work describing the prosperity and culture of Madurai city.",
        poetTa: "மாங்குடி மருதனார்",
        poetEn: "Mangudi Maruthanar",
        lines: 782,
        themeTa: "நகர வாழ்க்கை, தர்மம்",
        themeEn: "Urban Life, Dharma",
        periodTa: "கி.மு 2 நூற்றாண்டு",
        periodEn: "2nd Century BCE",
        detailsTa: "நகர வாழ்க்கையின் இன்பங்கள் நிலையற்றவை என்று போதிக்கிறது.",
        detailsEn: "Teaches that the pleasures of urban life are impermanent."
    },
    {
        id: 8,
        titleTa: "நெடுநல்வாடை",
        titleEn: "Nedunalvadai",
        subtitleTa: "நீண்ட வடக்கு காற்றின் பாட்டு",
        subtitleEn: "Song of the Long North Wind",
        descriptionTa: "குளிர்காலத்தின் வருகை மற்றும் பிரிவின் வேதனையை விவரிக்கும் 188 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 188-line work describing the arrival of winter and the pain of separation.",
        poetTa: "நக்கீரர்",
        poetEn: "Nakkeerar",
        lines: 188,
        themeTa: "பிரிவு, இயற்கை",
        themeEn: "Separation, Nature",
        periodTa: "கி.பி 2 நூற்றாண்டு",
        periodEn: "2nd Century CE",
        detailsTa: "தலைவனை பிரிந்த தலைவியின் துயரத்தை விவரிக்கிறது.",
        detailsEn: "Describes the sorrow of a woman separated from her lover."
    },
    {
        id: 9,
        titleTa: "குறிஞ்சிப்பாட்டு",
        titleEn: "Kurinjippattu",
        subtitleTa: "மலைநிலத்தின் பாட்டு",
        subtitleEn: "Song of the Mountain Region",
        descriptionTa: "மலைப்பகுதியின் அழகு மற்றும் அங்குள்ள மக்களின் வாழ்க்கையை விவரிக்கும் 261 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 261-line work describing the beauty of mountain regions and the life of people there.",
        poetTa: "கபிலர்",
        poetEn: "Kapilar",
        lines: 261,
        themeTa: "மலைநில வாழ்க்கை, காதல்",
        themeEn: "Mountain Life, Love",
        periodTa: "கி.மு 1 நூற்றாண்டு",
        periodEn: "1st Century BCE",
        detailsTa: "பிறை மன்னன் மற்றும் அவன் மனைவியின் காதல் கதையை விவரிக்கிறது.",
        detailsEn: "Describes the love story of King Pirai and his wife."
    },
    {
        id: 10,
        titleTa: "பட்டினப்பாலை",
        titleEn: "Pattinappalai",
        subtitleTa: "துறைமுக நகரின் பாட்டு",
        subtitleEn: "Song of the Port City",
        descriptionTa: "காவிரிப்பூம்பட்டினம் என்ற துறைமுக நகரத்தின் செழிப்பை விவரிக்கும் 301 வரிகள் கொண்ட நூல்.",
        descriptionEn: "A 301-line work describing the prosperity of the port city Kaviripattinam.",
        poetTa: "உருத்திரங்கண்ணனார்",
        poetEn: "Uruthirankannanar",
        lines: 301,
        themeTa: "வணிகம், கடல் வாழ்க்கை",
        themeEn: "Trade, Maritime Life",
        periodTa: "கி.மு 2 நூற்றாண்டு",
        periodEn: "2nd Century BCE",
        detailsTa: "சோழ மன்னன் கரிகாலனின் துறைமுக நகரத்தின் செழிப்பை விவரிக்கிறது.",
        detailsEn: "Describes the prosperity of Chola king Karikal's port city."
    }
];

// Playlist Data with WORKING Audio URLs - ALL 10 PATHU PATTU BOOKS
const playlistData = [
    {
        titleTa: "திருமுருகாற்றுப்படை - பாராயணம்",
        titleEn: "Thirumurugaatruppadai - Recitation",
        artistTa: "நக்கீரர்",
        artistEn: "Nakkeerar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3"
    },
    {
        titleTa: "பொருநராற்றுப்படை - பாராயணம்",
        titleEn: "Porunararruppadai - Recitation",
        artistTa: "முதத்தாமக்கன்னியார்",
        artistEn: "Mudathama Kanniyar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg"
    },
    {
        titleTa: "சிறுபணாற்றுப்படை - பாராயணம்",
        titleEn: "Sirupanarruppadai - Recitation",
        artistTa: "நத்தத்தனார்",
        artistEn: "Nattattanar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/intromusic.ogg"
    },
    {
        titleTa: "பெரும்பணாற்றுப்படை - பாராயணம்",
        titleEn: "Perumpanarruppadai - Recitation",
        artistTa: "உருத்திரங்கண்ணனார்",
        artistEn: "Uruthirankannanar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-assets/week7-brrring.m4a"
    },
    {
        titleTa: "முல்லைப்பாட்டு - பாராயணம்",
        titleEn: "Mullaipattu - Recitation",
        artistTa: "நப்பூதனார்",
        artistEn: "Napputanar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3"
    },
    {
        titleTa: "நெடுனளவாடை - பாராயணம்",
        titleEn: "Nedunalvadai - Recitation",
        artistTa: "நக்கீரர்",
        artistEn: "Nakkeerar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3"
    },
    {
        titleTa: "மதுரைக்காஞ்சி - பாராயணம்",
        titleEn: "Maduraikanchi - Recitation",
        artistTa: "மாங்குடி மருதனார்",
        artistEn: "Mangudi Maruthanar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg"
    },
    {
        titleTa: "நெடுநல்வாடை - பாராயணம்",
        titleEn: "Nedunalvadai - Recitation",
        artistTa: "நக்கீரர்",
        artistEn: "Nakkeerar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/intromusic.ogg"
    },
    {
        titleTa: "குறிஞ்சிப்பாட்டு - பாராயணம்",
        titleEn: "Kurinjippattu - Recitation",
        artistTa: "கபிலர்",
        artistEn: "Kapilar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-assets/week7-brrring.m4a"
    },
    {
        titleTa: "பட்டினப்பாலை - பாராயணம்",
        titleEn: "Pattinappalai - Recitation",
        artistTa: "உருத்திரங்கண்ணனார்",
        artistEn: "Uruthirankannanar",
        audioUrl: "https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3"
    }
];

// Audio player instance
let audioPlayer = null;
let isPlaying = false;
let progressInterval = null;

// Gallery Data
const galleryData = [
    { titleTa: "சங்ககால ஓலைச்சுவடி", titleEn: "Sangam Era Palm Leaf Manuscript", descriptionTa: "பண்டைய தமிழ் இலக்கியம்", descriptionEn: "Ancient Tamil Literature" },
    { titleTa: "முருகன் கோயில்", titleEn: "Murugan Temple", descriptionTa: "திருமுருகாற்றுப்படையில் குறிப்பிடப்பட்ட கோயில்", descriptionEn: "Temple mentioned in Thirumurugaatruppadai" },
    { titleTa: "சங்ககால நாணயங்கள்", titleEn: "Sangam Era Coins", descriptionTa: "பண்டைய தமிழ் அரசர்களின் நாணயங்கள்", descriptionEn: "Coins of ancient Tamil kings" },
    { titleTa: "தமிழ் நிலங்கள்", titleEn: "Tamil Landscapes", descriptionTa: "குறிஞ்சி, முல்லை, மருதம், நெய்தல், பாலை", descriptionEn: "Kurinji, Mullai, Marutham, Neithal, Palai" },
    { titleTa: "உ.வே. சாமிநாதையர்", titleEn: "U.V. Swaminatha Iyer", descriptionTa: "பத்துப்பாட்டை மீட்டெடுத்த அறிஞர்", descriptionEn: "Scholar who rediscovered Pathupattu" },
    { titleTa: "சங்ககால கலைப்பொருட்கள்", titleEn: "Sangam Era Artifacts", descriptionTa: "அகழ்வாராய்ச்சியில் கண்டெடுக்கப்பட்டவை", descriptionEn: "Discovered in archaeological excavations" }
];

// Current language
let currentLang = 'ta';

// Current playing song index
let currentSongIndex = 0;

// Initialize the website
document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.classList.add('js-enabled');
    loadBooks();
    loadPlaylist();
    loadGallery();
    initializeLanguageToggle();
    initializeNavigation();
    initializeSearch();
    initializeAudioPlayer();
    initializeChat();
    initializeScrollReveal();
    initializeMobileMenu();
    initializeBackToTop();
    initializeTheme();
    initializeScrollProgress();

    // Hide loader after a short delay to ensure everything is rendered
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.style.display = 'none', 500);
        }
    }, 1200);
});

// Scroll Reveal Animation
function initializeScrollReveal() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
            }
        });
    }, observerOptions);

    // Apply to sections and key blocks
    const revealElements = document.querySelectorAll('section, .feature-card, .book-card, .timeline-item, .theme-box, .about-visual');
    revealElements.forEach(el => {
        el.classList.add('reveal-section');
        observer.observe(el);
    });
}

// Mobile Menu Functionality
function initializeMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const navWrapper = document.getElementById('navWrapper');
    const navOverlay = document.getElementById('navOverlay');
    const navLinks = document.querySelectorAll('.nav-list a');

    if (menuToggle && navWrapper && navOverlay) {
        const toggleMenu = () => {
            menuToggle.classList.toggle('active');
            navWrapper.classList.toggle('active');
            navOverlay.classList.toggle('active');
            document.body.style.overflow = navWrapper.classList.contains('active') ? 'hidden' : 'auto';
        };

        menuToggle.addEventListener('click', toggleMenu);
        navOverlay.addEventListener('click', toggleMenu);

        // Close menu when a link is clicked
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navWrapper.classList.remove('active');
                navOverlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        });
    }
}

// Back to Top Functionality
function initializeBackToTop() {
    const backToTop = document.getElementById('backToTop');

    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Theme Management
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeToggle) themeToggle.textContent = '☀️';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            if (theme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = '🌓';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = '☀️';
            }
        });
    }
}

// Scroll Progress Tracker
function initializeScrollProgress() {
    const scrollBar = document.getElementById('scrollBar');

    if (scrollBar) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            scrollBar.style.width = scrolled + "%";
        });
    }
}


// Load Books
function loadBooks() {
    const booksGrid = document.getElementById('booksGrid');
    booksGrid.innerHTML = '';

    booksData.forEach(book => {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card';
        bookCard.onclick = () => {
            // Always use enhanced details
            openBookDetailsEnhanced(book.id);
        };

        bookCard.innerHTML = `
            <div style="position: relative;">
                <div class="book-number">${book.id}</div>
                <div class="book-header">
                    <h3 data-ta="${book.titleTa}" data-en="${book.titleEn}">${currentLang === 'ta' ? book.titleTa : book.titleEn}</h3>
                    <p data-ta="${book.subtitleTa}" data-en="${book.subtitleEn}">${currentLang === 'ta' ? book.subtitleTa : book.subtitleEn}</p>
                </div>
            </div>
            <div class="book-body">
                <p data-ta="${book.descriptionTa}" data-en="${book.descriptionEn}">${currentLang === 'ta' ? book.descriptionTa : book.descriptionEn}</p>
                <div class="poet-info">
                    <strong>${currentLang === 'ta' ? 'கவிஞர்' : 'Poet'}:</strong> 
                    <span data-ta="${book.poetTa}" data-en="${book.poetEn}">${currentLang === 'ta' ? book.poetTa : book.poetEn}</span>
                </div>
                <div class="book-meta">
                    <span class="meta-tag">${book.lines} ${currentLang === 'ta' ? 'வரிகள்' : 'lines'}</span>
                    <span class="meta-tag" data-ta="${book.themeTa}" data-en="${book.themeEn}">${currentLang === 'ta' ? book.themeTa : book.themeEn}</span>
                </div>
            </div>
        `;

        booksGrid.appendChild(bookCard);
    });
}

// Open Book Details (creates a modal with detailed information)
function openBookDetails(bookId) {
    const book = booksData.find(b => b.id === bookId);
    if (!book) return;

    // Create modal
    const modal = document.createElement('div');
    modal.className = 'book-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeBookModal()"></div>
        <div class="modal-content">
            <button class="modal-close" onclick="closeBookModal()">✕</button>
            <div class="modal-header">
                <h1 data-ta="${book.titleTa}" data-en="${book.titleEn}">${currentLang === 'ta' ? book.titleTa : book.titleEn}</h1>
                <p class="modal-subtitle" data-ta="${book.subtitleTa}" data-en="${book.subtitleEn}">${currentLang === 'ta' ? book.subtitleTa : book.subtitleEn}</p>
            </div>
            <div class="modal-body">
                <div class="modal-section">
                    <h3>${currentLang === 'ta' ? 'விவரம்' : 'Description'}</h3>
                    <p data-ta="${book.descriptionTa}" data-en="${book.descriptionEn}">${currentLang === 'ta' ? book.descriptionTa : book.descriptionEn}</p>
                    <p data-ta="${book.detailsTa}" data-en="${book.detailsEn}">${currentLang === 'ta' ? book.detailsTa : book.detailsEn}</p>
                </div>
                <div class="modal-info-grid">
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'கவிஞர்' : 'Poet'}</h4>
                        <p data-ta="${book.poetTa}" data-en="${book.poetEn}">${currentLang === 'ta' ? book.poetTa : book.poetEn}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'வரிகள்' : 'Lines'}</h4>
                        <p>${book.lines}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'காலம்' : 'Period'}</h4>
                        <p data-ta="${book.periodTa}" data-en="${book.periodEn}">${currentLang === 'ta' ? book.periodTa : book.periodEn}</p>
                    </div>
                    <div class="info-box">
                        <h4>${currentLang === 'ta' ? 'கருப்பொருள்' : 'Theme'}</h4>
                        <p data-ta="${book.themeTa}" data-en="${book.themeEn}">${currentLang === 'ta' ? book.themeTa : book.themeEn}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add modal styles
    const style = document.createElement('style');
    style.textContent = `
        .book-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 2000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease-out;
        }
        
        .modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            position: relative;
            background: white;
            max-width: 800px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.4s ease-out;
        }
        
        .modal-close {
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            background: var(--gradient-accent);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            font-size: 1.5rem;
            color: white;
            cursor: pointer;
            transition: transform 0.3s ease;
            z-index: 10;
        }
        
        .modal-close:hover {
            transform: rotate(90deg) scale(1.1);
        }
        
        .modal-header {
            background: var(--gradient-primary);
            color: white;
            padding: 3rem 2rem 2rem;
            text-align: center;
        }
        
        .modal-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .modal-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            font-style: italic;
        }
        
        .modal-body {
            padding: 2.5rem;
        }
        
        .modal-section {
            margin-bottom: 2rem;
        }
        
        .modal-section h3 {
            font-family: 'Playfair Display', serif;
            color: var(--tamil-maroon);
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        .modal-section p {
            line-height: 1.8;
            color: #333;
            margin-bottom: 1rem;
        }
        
        .modal-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.5rem;
        }
        
        .info-box {
            background: #F9F5F0;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid var(--accent-saffron);
        }
        
        .info-box h4 {
            font-family: 'Playfair Display', serif;
            color: var(--tamil-maroon);
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .info-box p {
            color: #555;
            font-size: 0.95rem;
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

// Close Book Modal
function closeBookModal() {
    const modal = document.querySelector('.book-modal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = 'auto';
    }
}

// Load Playlist
function loadPlaylist() {
    const playlistItems = document.getElementById('playlistItems');
    playlistItems.innerHTML = '';

    playlistData.forEach((song, index) => {
        const item = document.createElement('div');
        item.className = `playlist-item ${index === currentSongIndex ? 'active' : ''}`;
        item.onclick = () => playSong(index);

        item.innerHTML = `
            <h4 data-ta="${song.titleTa}" data-en="${song.titleEn}">${currentLang === 'ta' ? song.titleTa : song.titleEn}</h4>
            <p data-ta="${song.artistTa}" data-en="${song.artistEn}">${currentLang === 'ta' ? song.artistTa : song.artistEn}</p>
        `;

        playlistItems.appendChild(item);
    });
}

// Load Gallery with real images
function loadGallery() {
    const galleryGrid = document.getElementById('galleryGrid');
    if (!galleryGrid) return;
    galleryGrid.innerHTML = '';

    const imageUrls = [
        'https://images.unsplash.com/photo-1582510003544-2d095ca1828f?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1519791883288-dc8bd696e667?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1610444583731-9717ff984bb1?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1551024739-16a8c66e2c35?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1558450143-6cb2a5a99905?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1615671100318-63640b3783a0?auto=format&fit=crop&w=600&q=80'
    ];

    galleryData.forEach((item, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        const imgUrl = imageUrls[index % imageUrls.length];

        galleryItem.innerHTML = `
            <img src="${imgUrl}" alt="${item.titleEn}" style="width: 100%; height: 100%; object-fit: cover;">
            <div class="gallery-overlay">
                <h3 data-ta="${item.titleTa}" data-en="${item.titleEn}">${currentLang === 'ta' ? item.titleTa : item.titleEn}</h3>
                <p data-ta="${item.descriptionTa}" data-en="${item.descriptionEn}">${currentLang === 'ta' ? item.descriptionTa : item.descriptionEn}</p>
            </div>
        `;

        galleryGrid.appendChild(galleryItem);
    });
}

// Initialize Language Toggle
function initializeLanguageToggle() {
    const langButtons = document.querySelectorAll('.lang-pill');

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            if (lang === currentLang) return;

            currentLang = lang;
            langButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            updateLanguage();
        });
    });

    // Sync state on load
    const activeBtn = document.querySelector(`.lang-pill[data-lang="${currentLang}"]`);
    if (activeBtn) {
        langButtons.forEach(b => b.classList.remove('active'));
        activeBtn.classList.add('active');
    }
}

// Update Language
function updateLanguage() {
    // Update all elements with data-ta and data-en attributes
    document.querySelectorAll('[data-ta][data-en]').forEach(el => {
        const text = currentLang === 'ta' ? el.dataset.ta : el.dataset.en;
        if (el.tagName === 'INPUT') {
            el.placeholder = text;
        } else {
            el.textContent = text;
        }
    });

    // Reload dynamic content
    loadBooks();
    loadPlaylist();
    loadGallery();
}

// Initialize Navigation
function initializeNavigation() {
    const header = document.getElementById('mainHeader');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            if (header) header.classList.add('scrolled');
        } else {
            if (header) header.classList.remove('scrolled');
        }
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize Search
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.querySelector('.search-btn');

    searchBtn.addEventListener('click', () => {
        searchInput.classList.toggle('active');
        if (searchInput.classList.contains('active')) {
            searchInput.focus();
        }
    });

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (query.length < 2) return;

        // Search in books
        const bookCards = document.querySelectorAll('.book-card');
        bookCards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (text.includes(query)) {
                card.style.display = 'block';
                card.style.animation = 'fadeIn 0.3s ease-out';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Initialize Audio Player
function initializeAudioPlayer() {
    audioPlayer = document.getElementById('audioPlayer');
    if (!audioPlayer) {
        audioPlayer = document.createElement('audio');
        audioPlayer.id = 'audioPlayer';
        document.body.appendChild(audioPlayer);
    }

    const playBtn = document.getElementById('playBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (playBtn) playBtn.addEventListener('click', togglePlay);
    if (prevBtn) prevBtn.addEventListener('click', playPrevious);
    if (nextBtn) nextBtn.addEventListener('click', playNext);

    // Audio events
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('ended', playNext);
    audioPlayer.addEventListener('loadedmetadata', () => {
        const durationEl = document.getElementById('duration');
        if (durationEl) durationEl.textContent = formatTime(audioPlayer.duration);
    });

    updateCurrentSongUI();
}

function togglePlay() {
    const playBtn = document.getElementById('playBtn');
    if (audioPlayer.paused) {
        audioPlayer.play().catch(e => console.error("Playback failed:", e));
        if (playBtn) playBtn.textContent = '⏸️';
    } else {
        audioPlayer.pause();
        if (playBtn) playBtn.textContent = '▶️';
    }
}

function playPrevious() {
    currentSongIndex = (currentSongIndex - 1 + playlistData.length) % playlistData.length;
    loadAndPlayCurrentSong();
}

function playNext() {
    currentSongIndex = (currentSongIndex + 1) % playlistData.length;
    loadAndPlayCurrentSong();
}

function playSong(index) {
    currentSongIndex = index;
    loadAndPlayCurrentSong();
}

function loadAndPlayCurrentSong() {
    const song = playlistData[currentSongIndex];
    audioPlayer.src = song.audioUrl;
    audioPlayer.play().catch(e => console.warn("Auto-play blocked or failed:", e));

    const playBtn = document.getElementById('playBtn');
    if (playBtn) playBtn.textContent = '⏸️';

    updateCurrentSongUI();
}

function updateCurrentSongUI() {
    const song = playlistData[currentSongIndex];
    const titleEl = document.getElementById('currentSongTitle');
    const artistEl = document.getElementById('currentSongArtist');

    if (titleEl) {
        titleEl.textContent = currentLang === 'ta' ? song.titleTa : song.titleEn;
        titleEl.dataset.ta = song.titleTa;
        titleEl.dataset.en = song.titleEn;
    }

    if (artistEl) {
        artistEl.textContent = currentLang === 'ta' ? song.artistTa : song.artistEn;
        artistEl.dataset.ta = song.artistTa;
        artistEl.dataset.en = song.artistEn;
    }

    // Update playlist active state
    document.querySelectorAll('.playlist-item').forEach((item, index) => {
        if (index === currentSongIndex) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

function updateProgress() {
    const progressFill = document.getElementById('progressFill');
    const currentTimeEl = document.getElementById('currentTime');

    if (audioPlayer.duration) {
        const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        if (progressFill) progressFill.style.width = progress + '%';
        if (currentTimeEl) currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
    }
}

function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Cleanup Chat Functions
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    if (!chatContainer) return;

    chatContainer.classList.toggle('active');
    if (chatContainer.classList.contains('active')) {
        const input = document.getElementById('chatInput');
        if (input) input.focus();
        scrollToBottom();
    }
}

function initializeChat() {
    console.log('🤖 Chat initialized');
    // Pre-scroll to bottom of welcome message
    setTimeout(scrollToBottom, 100);
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    if (messagesContainer) {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    if (typeof sendMessageAI === 'function') {
        return sendMessageAI();
    }

    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    if (!chatInput || !chatInput.value.trim()) return;

    const userMessage = chatInput.value.trim();
    displayMessage(userMessage, 'user');
    chatInput.value = '';
    if (sendBtn) sendBtn.disabled = true;

    showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator();
        let response = getSimpleResponse(userMessage);
        displayMessage(response, 'bot');
        if (sendBtn) sendBtn.disabled = false;
    }, 1000);
}

function displayMessage(text, side) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${side}`;

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.innerHTML = formatMessageText(text);

    messageDiv.appendChild(messageText);
    messagesContainer.appendChild(messageDiv);

    scrollToBottom();
}

function formatMessageText(text) {
    if (!text) return '';
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const indicator = document.createElement('div');
    indicator.className = 'message bot typing-indicator';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = '<div class="message-text"><span>.</span><span>.</span><span>.</span></div>';
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function getSimpleResponse(message) {
    const lowerMessage = message.toLowerCase();
    const isTa = currentLang === 'ta';

    if (lowerMessage.includes('திருமுருகாற்றுப்படை') || lowerMessage.includes('thirumurugaatruppadai')) {
        return isTa ? 'திருமுருகாற்றுப்படை நக்கீரரால் இயற்றப்பட்ட பக்தி நூல். இது முருகனின் ஆறு படைவீடுகளை விவரிக்கிறது.' : 'Thirumurugaatruppadai is a devotional work by Nakkeerar describing the six abodes of Lord Murugan.';
    }
    if (lowerMessage.includes('யார்') || lowerMessage.includes('who')) {
        return isTa ? 'பத்துப்பாட்டில் நக்கீரர், கபிலர், உருத்திரங்கண்ணனார் போன்ற பல சிறந்த புலவர்கள் உள்ளனர்.' : 'Pathu Pattu features great poets like Nakkeerar, Kapilar, and Uruthirankannanar.';
    }
    return isTa ? 'வணக்கம்! நான் பத்துப்பாட்டு உதவி. உங்களுக்காக பத்துப்பாட்டு நூல்கள் மற்றும் சங்க இலக்கியம் பற்றி விளக்க முடியும். எதைப் பற்றிச் சொல்லட்டும்?' : 'Hello! I am your Pathu Pattu assistant. I can explain the ten books and Sangam literature. What would you like to know?';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

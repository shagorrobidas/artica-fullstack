document.addEventListener('DOMContentLoaded', () => {
    const mediaModalEl   = document.getElementById('mediaModal');
    const mediaModalLabel = document.getElementById('mediaModalLabel');
    const mediaModalBody  = document.getElementById('mediaModalBody');

    if (!mediaModalEl) return;

    function getYoutubeEmbedUrl(url) {
        if (!url) return '';
        const m = url.match(/(?:youtu\.be\/|v\/|watch\?v=|embed\/)([^#&?]{11})/);
        return m ? `https://www.youtube.com/embed/${m[1]}?autoplay=1` : url;
    }

    function buildContent(type, src, text, title) {
        // Auto-detect from extension when type may be wrong
        if (src) {
            const ext = src.split('?')[0].split('.').pop().toLowerCase();
            if (['jpg','jpeg','png','gif','webp','svg'].includes(ext)) type = 'image';
            else if (['mp4','webm','mov'].includes(ext))               type = 'video';
            else if (['mp3','wav','aac','m4a','ogg'].includes(ext))    type = 'audio';
            else if (src.includes('youtube.com') || src.includes('youtu.be')) type = 'youtube';
        }

        switch (type) {
            case 'image':
                return `<img src="${src}" class="img-fluid w-100" style="object-fit:contain;max-height:80vh;" alt="${title}">`;
            case 'video':
                return `<video class="w-100" controls autoplay style="max-height:80vh;">
                            <source src="${src}" type="video/mp4">
                        </video>`;
            case 'audio':
                return `<div class="p-5 text-center bg-light">
                            <i class="bx bx-headphone fs-1 text-primary mb-3 d-block"></i>
                            <audio controls autoplay class="w-100">
                                <source src="${src}" type="audio/mpeg">
                            </audio>
                        </div>`;
            case 'youtube':
                return `<div class="ratio ratio-16x9">
                            <iframe src="${getYoutubeEmbedUrl(src)}" title="${title}"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowfullscreen></iframe>
                        </div>`;
            case 'text':
                return `<div class="p-4 lh-lg">${(text || '').replace(/\n/g, '<br>')}</div>`;
            default:
                return `<div class="p-4 text-center text-muted">No content available.</div>`;
        }
    }

    // Handle clicks on any .media-btn — populate the modal BEFORE Bootstrap opens it
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.media-btn');
        if (!btn) return;

        const type  = btn.getAttribute('data-media-type')  || '';
        const title = btn.getAttribute('data-media-title') || '';
        const src   = btn.getAttribute('data-media-src')   || '';
        const text  = btn.getAttribute('data-media-text')  || '';

        // Write content NOW — before Bootstrap's show.bs.modal fires
        mediaModalLabel.textContent  = title;
        mediaModalBody.innerHTML     = buildContent(type, src, text, title);
    }, true); // capture phase = runs before Bootstrap

    // Clear on close so stale content / video/audio stops playing
    mediaModalEl.addEventListener('hidden.bs.modal', () => {
        mediaModalBody.innerHTML = '';
    });
});

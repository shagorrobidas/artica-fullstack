document.addEventListener('DOMContentLoaded', () => {
    const mediaModalEl = document.getElementById('mediaModal');
    const mediaModalLabel = document.getElementById('mediaModalLabel');
    const mediaModalBody = document.getElementById('mediaModalBody');
    
    if (!mediaModalEl) return;
    
    const mediaModal = new bootstrap.Modal(mediaModalEl);

    // YouTube regex parser
    function getYoutubeEmbedUrl(url) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        if (match && match[2].length == 11) {
            return 'https://www.youtube.com/embed/' + match[2] + '?autoplay=1';
        }
        return url;
    }

    document.querySelectorAll('.media-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            const type = btn.getAttribute('data-media-type');
            const title = btn.getAttribute('data-media-title');
            const src = btn.getAttribute('data-media-src');
            const text = btn.getAttribute('data-media-text');

            mediaModalLabel.textContent = title;
            mediaModalBody.innerHTML = ''; // Clear previous

            let contentHTML = '';

            switch(type) {
                case 'image':
                    contentHTML = `<img src="${src}" class="img-fluid w-100" style="object-fit: contain; max-height: 80vh;" alt="${title}">`;
                    break;
                case 'video':
                    contentHTML = `
                        <video class="w-100" controls autoplay style="max-height: 80vh;">
                            <source src="${src}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>`;
                    break;
                case 'audio':
                    contentHTML = `
                        <div class="p-5 text-center bg-light">
                            <i class='bx bx-headphone fs-1 text-primary mb-3 d-block'></i>
                            <audio controls class="w-100" autoplay>
                                <source src="${src}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>`;
                    break;
                case 'youtube':
                    const embedUrl = getYoutubeEmbedUrl(src);
                    contentHTML = `
                        <div class="ratio ratio-16x9">
                            <iframe src="${embedUrl}" title="${title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                        </div>`;
                    break;
                case 'text':
                    contentHTML = `<div class="p-4">${text.replace(/\\n/g, '<br>')}</div>`;
                    break;
            }

            mediaModalBody.innerHTML = contentHTML;
            // No need to call modal.show() because btn has data-bs-toggle="modal" Target
        });
    });

    // Cleanup when closing
    mediaModalEl.addEventListener('hidden.bs.modal', () => {
        mediaModalBody.innerHTML = '<div class="p-4 text-center text-muted">Loading...</div>';
    });
});

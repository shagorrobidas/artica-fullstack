document.addEventListener('DOMContentLoaded', () => {
    const termModalEl = document.getElementById('termModal');
    if (!termModalEl) return;

    const termModal = new bootstrap.Modal(termModalEl);
    const termModalLabel = document.getElementById('termModalLabel');
    const termModalBody = termModalEl.querySelector('.modal-body');

    // Use Event Delegation for better robustness
    document.addEventListener('click', (e) => {
        // Find the closest .interactive-term element (handles clicking the icon inside)
        const termEl = e.target.closest('.interactive-term');
        if (!termEl) return;

        e.preventDefault();

        // Access the globally populated terms data
        const termsData = window.articleTerms || {};
        const slug = termEl.getAttribute('data-term-slug');
        const data = termsData[slug];

        console.log('Clicked term:', slug, data); // Debugging

        if (data) {
            termModalLabel.textContent = data.term;
            
            let bodyHTML = '';
            
            // Media section
            if (data.type === 'image' && data.image) {
                bodyHTML += `<div class="mb-4 shadow-sm rounded overflow-hidden">
                                <img src="${data.image}" class="img-fluid w-100" style="max-height: 350px; object-fit: contain; background: #f8f9fa;" alt="${data.term}">
                             </div>`;
            } else if (data.type === 'video') {
                if (data.video) {
                    bodyHTML += `<div class="mb-4 shadow-sm rounded overflow-hidden bg-dark">
                                    <video controls class="w-100" style="max-height: 350px;">
                                        <source src="${data.video}" type="video/mp4">
                                        Your browser does not support the video tag.
                                    </video>
                                 </div>`;
                } else if (data.youtube) {
                    let vidId = '';
                    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
                    const match = data.youtube.match(regExp);
                    if (match && match[2].length === 11) vidId = match[2];
                    
                    if (vidId) {
                        bodyHTML += `<div class="mb-4 shadow-sm rounded overflow-hidden ratio ratio-16x9">
                                        <iframe src="https://www.youtube.com/embed/${vidId}?autoplay=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                                     </div>`;
                    }
                }
            }

            // Explanation section
            if (data.explanation) {
                bodyHTML += `<div class="term-content p-2 lh-lg text-dark fs-6">${data.explanation}</div>`;
            }
            
            // Audio section
            if (data.audio) {
                bodyHTML += `
                    <div class="mt-4 p-3 bg-light rounded-3 border-start border-primary border-4">
                        <label class="form-label fw-bold small text-primary mb-2 d-flex align-items-center gap-2">
                            <i class='bx bx-volume-full'></i> Audio Preview
                        </label>
                        <audio controls class="w-100" style="height: 35px;">
                            <source src="${data.audio}" type="audio/mpeg">
                        </audio>
                    </div>`;
            }

            // External Link
            if (data.link) {
                bodyHTML += `
                    <div class="mt-4 text-center">
                        <a href="${data.link}" target="_blank" class="btn btn-primary px-4 py-2 rounded-pill shadow-sm">
                            <i class='bx bx-link-external me-2'></i> Learn More & Details
                        </a>
                    </div>`;
            }

            termModalBody.innerHTML = bodyHTML;
            termModal.show();
        } else {
            console.warn('Data not found for term slug:', slug);
        }
    });

    // Stop media on close
    termModalEl.addEventListener('hidden.bs.modal', function () {
        termModalBody.innerHTML = '';
    });
});

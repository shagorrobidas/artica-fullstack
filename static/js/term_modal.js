document.addEventListener('DOMContentLoaded', () => {
    const termModalEl = document.getElementById('termModal');
    if (!termModalEl) return;
    
    const termModalLabel = document.getElementById('termModalLabel');
    const termModalBody = document.getElementById('termModalBody');
    const termModal = new bootstrap.Modal(termModalEl);

    // We expect window.articleTerms to be populated by the Django template
    const termsData = window.articleTerms || {};

    document.querySelectorAll('.interactive-term').forEach(termEl => {
        termEl.addEventListener('click', (e) => {
            const slug = termEl.getAttribute('data-term-slug');
            const data = termsData[slug];

            if (data) {
                termModalLabel.textContent = data.term;
                
                let bodyHTML = `<div class="term-content">${data.explanation}</div>`;
                
                if (data.image) {
                    bodyHTML = `<img src="${data.image}" class="img-fluid rounded mb-3 w-100" alt="${data.term}">` + bodyHTML;
                }
                
                if (data.audio) {
                    bodyHTML += `
                        <div class="mt-4 border-top pt-3">
                            <label class="form-label small text-muted">Pronunciation / Audio Note</label>
                            <audio controls class="w-100 mx-auto" style="height: 40px;">
                                <source src="${data.audio}" type="audio/mpeg">
                            </audio>
                        </div>`;
                }

                if (data.link) {
                    bodyHTML += `
                        <div class="mt-3 text-end">
                            <a href="${data.link}" target="_blank" class="btn btn-sm btn-outline-primary">Learn More <i class='bx bx-link-external'></i></a>
                        </div>`;
                }

                termModalBody.innerHTML = bodyHTML;
                termModal.show();
            }
        });
    });
});

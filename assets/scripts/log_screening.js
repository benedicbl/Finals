document.addEventListener('DOMContentLoaded', function() {
    
    // DATA SOURCE (Contoh)
    // Di aplikasi nyata, data ini akan datang dari database/API.
    const logData = [
        { 
            id: 1, petugas: 'YANTO', tanggal: '27/07/2025', supplier: '001', 
            details: { 'Grade A': 1500, 'Grade B': 100,'Grade BK': 100, 'Grade Retak': 75, 'Grade BS': 50 } 
        },
        { 
            id: 2, petugas: 'ALIM', tanggal: '30/07/2025', supplier: '007',
            details: { 'Grade A': 2000, 'Grade B': 100,'Grade BK': 250, 'Grade Retak': 100, 'Grade BS': 80 }
        },
        // Tambahkan data lainnya di sini
    ];

    const detailButtons = document.querySelectorAll('.btn-detail');
    const modal = document.getElementById('screening-modal');
    
    if (!modal) return; // Keluar jika modal tidak ada

    const closeModalBtn = modal.querySelector('.modal-close-btn');

    const openModal = (logId) => {
        // 1. Cari data log berdasarkan ID yang diklik
        const log = logData.find(item => item.id == logId);
        if (!log) return;

        // 2. Lakukan kalkulasi
        let totalButir = 0;
        let totalLayak = 0;
        let detailsHtml = '';

        for (const [grade, jumlah] of Object.entries(log.details)) {
            // Tambahkan ke total butir
            totalButir += jumlah;

            // Tambahkan ke total layak jika bukan Grade BS
            if (grade !== 'Grade BS') {
                totalLayak += jumlah;
            }

            // Buat HTML untuk setiap baris detail
            const gradeClass = grade.toLowerCase().replace(' ', '-');
            detailsHtml += `
                <div class="detail-item">
                    <div>
                        <span class="grade-circle grade-${gradeClass}"></span>
                        ${grade}
                    </div>
                    <span>${jumlah.toLocaleString('de-DE')}</span>
                </div>
            `;
        }

        // 3. Update konten modal dengan data yang dinamis
        modal.querySelector('#modal-supplier-code span').textContent = log.supplier;
        modal.querySelector('#modal-date').textContent = `Tanggal Pencatatan : ${log.tanggal}`;
        modal.querySelector('#modal-petugas-info strong').textContent = log.petugas;
        
        modal.querySelector('#modal-screening-details').innerHTML = detailsHtml;

        modal.querySelector('#modal-total-butir').textContent = totalButir.toLocaleString('de-DE');
        modal.querySelector('#modal-total-layak').textContent = totalLayak.toLocaleString('de-DE');
        
        // 4. Tampilkan modal
        modal.classList.add('active');
    };

    const closeModal = () => {
        modal.classList.remove('active');
    };

    detailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const logId = this.dataset.logId; // Ambil ID dari atribut data-log-id
            openModal(logId);
        });
    });

    closeModalBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
});
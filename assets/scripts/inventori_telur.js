document.addEventListener('DOMContentLoaded', function() {
    
    // --- Logika untuk Accordion ---
    const accordionTriggers = document.querySelectorAll('.accordion-trigger');
    accordionTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const parentItem = this.parentElement;
            parentItem.classList.toggle('active');
        });
    });

    // --- Fungsi BARU untuk menghitung total per ruangan ---
    function calculateRoomTotals() {
        // 1. Ambil semua item accordion (setiap ruangan)
        const accordionItems = document.querySelectorAll('.accordion-item');

        // 2. Loop untuk setiap ruangan
        accordionItems.forEach(item => {
            // Inisialisasi subtotal untuk ruangan ini
            let roomSubtotal = 0;
            
            // Ambil elemen-elemen yang relevan DI DALAM ruangan ini
            const detailRows = item.querySelectorAll('.content-row');
            const roomTotalElement = item.querySelector('.room-total');

            // Loop setiap baris detail di dalam ruangan ini
            detailRows.forEach(row => {
                // Ambil elemen span yang berisi jumlah butir (elemen span kedua)
                const amountElement = row.querySelector('span:last-child');
                if (amountElement) {
                    const textValue = amountElement.textContent.replace(/\./g, '');
                    const numericValue = parseInt(textValue, 10);

                    if (!isNaN(numericValue)) {
                        roomSubtotal += numericValue;
                    }
                }
            });

            // Update total untuk ruangan ini di DOM
            if (roomTotalElement) {
                if (roomSubtotal > 0) {
                    roomTotalElement.textContent = roomSubtotal.toLocaleString('de-DE');
                } else {
                    roomTotalElement.textContent = '-'; // Tampilkan strip jika total 0
                }
            }
        });
    }

    // --- Fungsi untuk menghitung total fisik keseluruhan ---
    function calculateGrandTotal() {
        // 1. Ambil semua elemen yang berisi jumlah butir per ruangan
        const roomTotals = document.querySelectorAll('.room-total');
        const grandTotalElement = document.getElementById('grand-total');

        if (!grandTotalElement) return;

        // 2. Inisialisasi total
        let grandTotal = 0;

        // 3. Loop setiap elemen, bersihkan format, dan tambahkan ke total
        roomTotals.forEach(element => {
            const textValue = element.textContent.replace(/\./g, '');
            const numericValue = parseInt(textValue, 10);

            if (!isNaN(numericValue)) {
                grandTotal += numericValue;
            }
        });

        // 4. Format total akhir
        const formattedTotal = grandTotal.toLocaleString('de-DE');

        // 5. Tampilkan hasilnya di elemen target
        grandTotalElement.innerHTML = `TOTAL FISIK : ${formattedTotal} BUTIR`;
    }

    // --- Panggil Fungsi Saat Halaman Dimuat ---
    
    // PENTING: Hitung total per ruangan DULU
    calculateRoomTotals();
    
    // BARU hitung total keseluruhan berdasarkan hasil di atas
    calculateGrandTotal();
});
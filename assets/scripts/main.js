document.addEventListener('DOMContentLoaded', function() {
    // Cari elemen navigasi sidebar yang bisa di-scroll
    const sidebarNav = document.querySelector('.sidebar-nav');

    // Jika elemennya tidak ada, hentikan eksekusi
    if (!sidebarNav) {
        return;
    }

    // --- BAGIAN 1: MENERAPKAN POSISI SCROLL YANG TERSIMPAN ---
    // Ambil posisi scroll yang tersimpan dari sessionStorage
    const savedScrollPosition = sessionStorage.getItem('sidebarScroll');

    // Jika ada posisi yang tersimpan, terapkan ke sidebar
    if (savedScrollPosition !== null) {
        sidebarNav.scrollTop = parseInt(savedScrollPosition, 10);
    }

    // --- BAGIAN 2: MENYIMPAN POSISI SCROLL SAAT LINK DIKLIK ---
    // Ambil semua link di dalam navigasi sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');

    // Tambahkan event listener ke setiap link
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Simpan posisi scroll saat ini ke sessionStorage
            sessionStorage.setItem('sidebarScroll', sidebarNav.scrollTop);
        });
    });
});
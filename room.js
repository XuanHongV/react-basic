// Hàm lọc p dựa trên trạng thái
function filterRooms(status) {
    const rooms = document.querySelectorAll('.room');
    rooms.forEach(room => {
      if (status === 'all') {
        room.classList.remove('hidden');
      } else if (!room.classList.contains(status)) {
        room.classList.add('hidden');
      } else {
        room.classList.remove('hidden');
      }
    });
  
    // Cập nhật trạng thái lọc
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(button => {
      button.classList.remove('active');
    });
  
    document.querySelector(`.filter-btn[onclick="filterRooms('${status}')"]`).classList.add('active');
  }
  
  const roomsPerPage = 3; // Số p mỗi trang
let currentPage = 1;

function goToPage(page) {
    const rooms = document.querySelectorAll('.room');
    const totalRooms = rooms.length;
    const totalPages = Math.ceil(totalRooms / roomsPerPage);

    if (page === 'next') {
        if (currentPage < totalPages) currentPage++;
    } else if (page === 'prev') {
        if (currentPage > 1) currentPage--;
    } else {
        currentPage = page;
    }

    rooms.forEach((room, index) => {
        room.classList.add('hidden');
        if (index >= (currentPage - 1) * roomsPerPage && index < currentPage * roomsPerPage) {
            room.classList.remove('hidden');
        }
    });

    // Cập nhật trạng thái của các nút phân trang
    const pageButtons = document.querySelectorAll('.page-btn');
    pageButtons.forEach(button => {
        button.classList.remove('active');
    });

    document.querySelector(`.page-btn[onclick="goToPage(${currentPage})"]`).classList.add('active');
}

// Gọi hàm để hiển thị trang đầu tiên khi trang tải lần đầu
goToPage(1);



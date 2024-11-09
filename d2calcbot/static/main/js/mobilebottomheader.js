window.addEventListener('resize', function() {
  const headerRow = document.querySelector('.header-row');
  const bottomHeader = document.querySelector('.bottom-header-bottom');
  const windowHeight = window.innerHeight;

  if (headerRow) { // Проверяем, что headerRow существует
    // Вычисляем необходимую высоту для .bottom-header
    const bottomHeaderHeight = windowHeight - headerRow.offsetHeight;
    // Устанавливаем высоту .bottom-header
    bottomHeader.style.height = bottomHeaderHeight + 'px';
  } else {
    // Если headerRow отсутствует, устанавливаем высоту .bottom-header на полную высоту окна
    bottomHeader.style.height = windowHeight + 'px';
  }
});

// Выполняем функцию при загрузке страницы
window.onload = function() {
  window.dispatchEvent(new Event('resize')); // Инициализируем функцию при загрузке
};
document.getElementById('cart-link').addEventListener('click', function() {
    fetch('/cart/get_cart/')  // Отправляем GET-запрос на Django-сервер
        .then(response => response.json())  // Преобразуем ответ в JSON
        .then(data => {
            let cartItemsContainer = document.getElementById('cart-items');
            cartItemsContainer.innerHTML = '';

            if (data.cart.length > 0) {
                data.cart.forEach(item => {
                    let itemDiv = document.createElement('div');
                    itemDiv.classList.add('cart-item');

                    // Создаем текст с информацией о товаре
                    let itemText = document.createElement('span');
                    itemText.textContent = `${item.product_name} - ${item.quantity} шт. - ${item.total_price} руб.`;

                    // Создаем крестик для удаления
                    let removeButton = document.createElement('span');
                    removeButton.innerHTML = '<i class="fas fa-times"></i>';  // Иконка крестика
                    removeButton.classList.add('remove-btn');
                    removeButton.addEventListener('click', function() {
                        removeItemFromCart(item.product_id);  // Удалить товар из корзины
                    });

                    // Добавляем текст и кнопку в контейнер товара
                    itemDiv.appendChild(itemText);
                    itemDiv.appendChild(removeButton);

                    // Добавляем товар в контейнер
                    cartItemsContainer.appendChild(itemDiv);
                });
            } else {
                cartItemsContainer.innerHTML = '<p>Ваша корзина пуста.</p>';
            }

            // Показываем окно корзины
            document.getElementById('cart-modal').style.right = '0';
        })
        .catch(error => console.error('Ошибка загрузки корзины:', error));
});
// Закрытие окна корзины
document.getElementById('close-cart').addEventListener('click', function() {
    document.getElementById('cart-modal').style.right = '-300px';
});
function removeItemFromCart(productId){
    fetch(`/cart/remove_from_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken() // CSRF-токен для Django
        },
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            changeCount(data.cartCount)
            // Обновляем корзину после удаления товара
            document.getElementById('cart-link').click();  // Перезагружаем корзину
        } else {
            alert('Не удалось удалить товар из корзины');
        }
    })
    .catch(error => console.error('Ошибка при удалении товара:', error));
}


document.getElementById('add-to-cart-listener').addEventListener('click', function () {
    const productId = this.getAttribute("data-product-id");
    addToCart(productId)
});

function addToCart(productId){
    fetch(`/cart/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() // CSRF-токен для Django
            },
        // body: `product_id=${productId}`
    }).then(response => response.json())
    .then(data => {// Проверяем, что приходит
        changeCount(data.cartCount);
        document.getElementById('cart-link').click();  // Перезагружаем корзину
    })
    .catch(error => console.error('Ошибка добавления в корзину:', error));
}
// Функция для получения CSRF-токена из cookies
function getCSRFToken() {
    let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : '';
}
function changeCount(count) {
    var countItems = document.getElementById('cart-link');
    if (count === '0') {
        countItems.innerHTML = 'Корзина'
    } else {
        countItems.innerHTML = `Корзина ${count}`;
    }
}
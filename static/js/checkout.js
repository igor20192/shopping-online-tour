document.addEventListener('DOMContentLoaded', function () {
    let cityField = $('#id_line4');
    let line1Field = $('#id_line1');

    // Инициализация Select2 для поля выбора города
    cityField.select2();

    // Инициализация Select2 для поля выбора отделения
    line1Field.select2();

    // Обработчик события изменения значения поля "город"
    cityField.on('select2:select', function (e) {
        let city = e.params.data.text;
        // Отправляем запрос к API Новой Почты для получения списка отделений в выбранном городе
        fetch(`/checkout/api_nova_poshta_warehouses/${encodeURIComponent(city)}`)
            .then(response => response.json())
            .then(data => {
                let warehouses = data.warehouses.data;
                let options = '';
                for (let i = 0; i < warehouses.length; i++) {
                    options += `<option value="${warehouses[i].Number}">${warehouses[i].Description}</option>`;
                }

                // Уничтожаем текущий Select2 и создаем новый с обновленным содержимым
                line1Field.html(options).select2('destroy').select2();
            })
            .catch(error => {
                console.error('Error fetching warehouses:', error);
            });
    });

    // Обновление списка городов при загрузке страницы
    fetch('/checkout/api_nova_poshta_cities/')
        .then(response => response.json())
        .then(data => {
            let cities = data.cities;
            let options = '';
            for (let i = 0; i < cities.length; i++) {
                options += `<option value="${cities[i]}">${cities[i]}</option>`;
            }

            cityField.html(options).trigger('change');
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
        });
});

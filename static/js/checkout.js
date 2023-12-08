document.addEventListener('DOMContentLoaded', function () {
    let line1Field = document.querySelector('#id_line1');
    let cityField = document.querySelector('#id_line4');

    // Инициализация Select2 для поля выбора отделения
    $(line1Field).select2();

    // Обработчик события изменения значения поля "line4"
    cityField.addEventListener('change', function () {
        let city = this.value;

        // Отправляем запрос к API Новой Почты
        fetch(`/checkout/api_nova_poshta_warehouses/${encodeURIComponent(city)}`)
            .then(response => response.json())
            .then(data => {
                // Заполняем поле "Branch number of Nova Poshta" полученными отделениями
                // Предполагается, что в data будет список отделений
                // Пожалуйста, адаптируйте это к вашему API
                let warehouses = data.warehouses.data; // Предполагаемая структура данных
                let options = '';
                for (let i = 0; i < warehouses.length; i++) {
                    options += `<option value="${warehouses[i].Number}">${warehouses[i].Description}</option>`;
                }

                // Обновляем содержимое Select2
                //$(line1Field).html(options).trigger('change');
                $(line1Field).html(options).select2('destroy').select2();
            })
            .catch(error => {
                console.error('Error fetching warehouses:', error);
            });
    });
});

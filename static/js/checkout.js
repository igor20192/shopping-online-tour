
document.addEventListener('DOMContentLoaded', function () {
    // Обработчик события изменения значения поля "line4"
    document.querySelector('#id_line4').addEventListener('change', function () {
        let city = this.value;
        let line1Field = document.querySelector('#id_line1');
        console.log(city)
        // Очищаем поле "Branch number of Nova Poshta"
        line1Field.value = '';

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

                line1Field.innerHTML = `<select name="line1" id="id_line1">${options}</select>`;
                console.log(options)
            })
            .catch(error => {
                console.error('Error fetching warehouses:', error);
            });
    });
});

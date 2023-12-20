document.addEventListener('DOMContentLoaded', function () {
    // Initialize Select2 for the city selection field
    let cityField = $('#id_line4');
    let line1Field = $('#id_line1');

    function formatState(state) {
        // Custom formatting for Select2 options
        if (!state.id) {
            return state.text;
        }

        var baseUrl = "/user/pages/images/flags";
        var $state = $('<span><img class="img-flag" /> <span></span></span>');

        // Use .text() instead of HTML string concatenation to avoid script injection issues
        $state.find("span").text(state.text);
        //$state.find("img").attr("src", baseUrl + "/" + state.element.value.toLowerCase() + ".png");

        return $state;
    };

    // Initialize Select2 for the city selection field with custom formatting
    cityField.select2({ tags: true, templateSelection: formatState });

    // Initialize Select2 for the branch selection field with tagging and custom formatting
    line1Field.select2({ tags: true, templateSelection: formatState });

    // Event handler for the "city" field value change
    cityField.on('select2:select', function (e) {
        let city = e.params.data.text;
        cityField.val(city).trigger('change');

        // Send a request to Nova Poshta API to get a list of branches in the selected city
        fetch(`/checkout/api_nova_poshta_warehouses/${encodeURIComponent(city)}`)
            .then(response => response.json())
            .then(data => {
                let warehouses = data.warehouses.data;
                let options = '';
                for (let i = 0; i < warehouses.length; i++) {
                    options += `<option value="${warehouses[i].Number}">${warehouses[i].Description}</option>`;
                }

                // Destroy the current Select2 and create a new one with updated content
                line1Field.html(options).select2('destroy').select2();
            })
            .catch(error => {
                console.error('Error fetching warehouses:', error);
            });
    });

    // Event handler for the "branch" field value change
    line1Field.on('select2:select', function (e) {
        let selectedBranch = e.params.data.text;
        line1Field.val(selectedBranch).trigger('change');
    });

    // Update the list of cities when the page loads
    fetch('/checkout/api_nova_poshta_cities/')
        .then(response => response.json())
        .then(data => {
            let cities = data.cities;
            let options = '';
            for (let i = 0; i < cities.length; i++) {
                options += `<option value="${cities[i]}">${cities[i]}</option>`;
            }

            // Update the city field with the list of cities
            cityField.html(options).trigger('change');
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
        });
});

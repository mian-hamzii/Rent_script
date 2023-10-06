$(function () {
    $('.datepicker').datepicker();
    $('.timepicker').timepicker({
        timeFormat: 'h:mm p',
        interval: 10,
        minTime: '08',
        maxTime: '6:00pm',
        defaultTime: '9',
        startTime: '08:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });

    $('#disabledAddress').on('change', function () {
        if ($(this).prop('checked') == false) {
            $('#id_return_location').attr('disabled', false)
        } else {
            $('#id_return_location').attr('disabled', true)
        }
    })

    $('#my_form').submit(function () {
        $("#my_form :disabled").removeAttr('disabled');
    });
    $('#button-id').on('click', function () {
        document.getElementById('show-data').style.display = 'block'
        document.getElementById('crFormExtras').style.display = 'none'
        $(this).hide()

    })
    $(document).on('click', '#car-submit', function (e) {
        e.preventDefault()
        var car_id = $(this).parent().find('#car-id').val()
        var url = $(this).parent().find('#car-url').val()
        $.ajax({
            type: "POST", url: url, data: {
                'car_id': car_id
            }, success: function (data) {
                var newDoc = document.open("text/html", "replace");
                newDoc.write(data);
                newDoc.close();
            }
        });
    });
    var add = $('#extraAdd')
    $('.addExtra').on('click', function () {
        var url = $(this).parent().find('#extra-url').val()
        var extra = $(this).parent().find('.addExtra').val()
        add.text(Number(extra) + Number(add.text()))
        $(this).parent().find('.removeExtra').removeClass('d-none')
        $(this).addClass('d-none')
        $.ajax({
            type: 'GET', url: url, success: function (data) {
                $('#table-receipt').html(data)
            }
        })
    });
    $('.removeExtra').on('click', function () {
        var extra = $(this).parent().find('.addExtra').val()
        $('#extraAdd').html(Number($('#extraAdd').text()) - Number(extra))
        $(this).parent().find('.addExtra').removeClass('d-none')
        $(this).addClass('d-none')
    });
    $('#termsCheckbox').change(function () {
        if ($(this).is(":checked")) {
            $('#crBtnConfirm').prop("disabled", false);
        } else {
            $('#crBtnConfirm').prop("disabled", true);
        }
    });
    $('#sort').on('change', function () {
        var url = $(this).find('#price_asc').val()
        var selectedOption = $(this).val();
        console.log(url)
        $.ajax({
            type: 'post',
            url: url,
            data: {
                'sort_option': selectedOption,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                // Update the car list with the new sorted data
                $('.pjCrPanelRight  ').html(data);
            }
        })
    });


});

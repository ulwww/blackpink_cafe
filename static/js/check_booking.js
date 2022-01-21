function book() {
    var name = document.getElementById('name').value;
    var phone = document.getElementById('phone').value;
    var date = document.getElementById('date').value;
    var time = document.getElementById('time').value;
    var table = document.getElementById('table').value;
    var comment = document.getElementById('comment').value;

    if (name.length == 0 || phone.length == 0 || date.length == 0 || time.length == 0) {
        alert('Не во все необходимые для записи поля введены данные. Пожалуйста заполните все поля, помеченные символом *.');
        return;
    }

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('POST', '/booking/?name=' + name + '&phone=' + phone +
        '&date=' + date + '&time=' + time + '&table=' + table + '&comment=' + comment, false);
    xmlHttp.send(null);
    var response = JSON.parse(xmlHttp.responseText);
    console.log(response);

    if (response['status'] == 'ok') {
        alert('Поздравляем. Вами успешно был забронирован ' +
            table + ' на ' + date + ' ' + time + '!');
        window.location.replace('/booking/' + response['uuid']);
    } else if (response['status'] == 'booked') {
        alert('Стол на выбранную Вами дату и время забронирован.')
    } else {
        alert('Произошла ошибка! Проверьте корректность введённых Вами данных.')
    }
}
var weather_types = ['Дождь', 'Гроза', 'Ясно' , 'Небольшая Облачность', 'Туман',
'Переменная Облачность', 'Облачно'];


function getData(month) {
    var days = $(".dateText");
    var data = {};
    days.each(function (i, e) {
        var $e = $(e);
        var par = $e.parent().parent();
        var dayNum = $e.text().trim();
        var weather = par.find(".show-for-large-up").text().trim();
        var sPar = par.parent().parent().parent();
        console.log(1);
        var val = $(sPar.find(".high .wx-value")[0]).text().trim().replace('°', '');
        data['' + dayNum] = {'weather': weather, 'temperature': val};
    });
    return '"' + month + '":' + JSON.stringify(data);
}

getData(2);
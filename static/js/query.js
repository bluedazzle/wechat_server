/**
 * Created by Toxni on 28/05/2018.
 */

(function () {
    var button = document.getElementById('submit');
    var phone = document.getElementById('phone');
    var token = document.getElementById('token');

    button.onclick = function () {
        if (!/^1[345678]\d{9}$/.test(phone.value)) {
            alert('手机号码不正确！');
            return
        }

        var query = new XMLHttpRequest();
        var address = location.origin + '/api/v1/phone/?phone=' + phone.value + '&token=' + token.value;
        query.open("GET", address, true);
        query.send();
        query.onreadystatechange = function () {
            if (query.readyState == 4 && query.status == 200) {
                alert(JSON.parse(query.responseText).msg);
                if (JSON.parse(query.responseText).status == 1){
                    location.href = '/page/hint/'
                }
            }
        };

    }
})();
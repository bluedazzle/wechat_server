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
    if (query.status !== (200 || 304)) {
      if (JSON.stringify(query.responseText).msg) {
        alert(JSON.stringify(query.responseText).msg)
      }
      else {
        alert('领取失败！')
      }
    } else {
      alert('领券成功！');
      location.href = '/page/hint/'
    }
  }
})();
function dateToday() {
    let dateGenerator = new Date();
    let day = ("0" + dateGenerator.getDate()).slice(-2);
    let month = ("0" + (dateGenerator.getMonth() + 1)).slice(-2);
    let today = dateGenerator.getFullYear() + "-" + (month) + "-" + (day);

    return today;
}
function basicInfo(target) {
    let formalign = document.getElementById("formalign");
        formalign.style.display = "block";
    if (target) {
        let clist = target.parentNode.parentNode.children;

        // id
        let id = document.getElementById("id");
        id.value = clist[0].innerText;
    }

    // Username
    let username = document.getElementById("username");
    username.value = document.getElementById("logo").dataset.username;

    // date
    let date = document.getElementById("date");
    date.value = dateToday();
    console.log(date.value);
}

const submitBtn = document.querySelector('#btn');
submitBtn.onclick = function() {
    basicInfo(null);
    // sqlType
    let sqlType = document.getElementById("sqlType");
    sqlType.value = 0;
}

const content = document.querySelector('.content');
content.onclick = function(ev) {
    ev = ev || window.event;
    let target = ev.target || ev.srcElement;
    // 打开表单的时候还要把数据自动填进去
       let clist = target.parentNode.parentNode.children;
    if (target.id == 'modify') {
        basicInfo(target);

        // Words
        let words = document.getElementById("words");
        words.value = clist[2].innerText;
        // sqlType
        let sqlType = document.getElementById("sqlType");
        sqlType.value = 1;
    }
    else if (target.id == 'delete') {
        if (!confirm(language == 'EN' ? "Confirm to DELETE?" : "是否删除？"))
            return false;
        // ajax向后端请求数据库

        let formData = new FormData();
        formData.append('id', clist[0].innerText);
        xhr = new XMLHttpRequest();
        xhr.responseType = 'json';
        xhr.open('POST', '/delete');
        xhr.send(formData);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    let status = xhr.response.status;
                    if (status == 'fail') {
                        let logout = document.getElementById('/logout');
                        logout.click();
                    }
                    else {
                        prepare();
                    }
                }
            }
        }
    }
};

// 关闭表单
var submitReset = document.getElementById("submitReset");
submitReset.onclick = function() {
    let formalign = document.getElementById("formalign");
    formalign.style.display = "none";
};

// 确认提交表单
let submitScore = document.getElementById("submitScore");
submitScore.onclick = function() {
    if (!confirm(language == 'EN' ? "Confirm to SUBMIT?" : "是否提交？")) {
        return false;
    }
    let id = document.getElementById('id');
    let username = document.getElementById('username');
    if (id.value == '' && username.value == '') {
        submitReset.click();
        return false;
    }
    return true;
};
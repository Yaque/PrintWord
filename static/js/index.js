var textData = [":_()<>ABC", "|}]{[", "#$@!?/", ";-+=*&", "overflow", "password密码", "username用户名", "margin", "padding", "placeholder", "text", "input", "int", "python", "for", "in", "output", "select", "script脚本", "green", "background", "color颜色", "string", "tuple元组", "array数组", "float", "value", "element元素", "counter", "for", "in", "from", "as", "if如果", "else那么", "with", "import", "finally", "return", "def", "try尝试", "continue继续", "break:打破", "global", "and", "or", "while", "except", "print", "class", "main", "pass", "lambda", "assert", "not", "window", "fixed", "table", "number", "html", "screen", "age", "data", "date", "boolean", "math数学", "this"];
textData.sort(function() {
     return (0.5-Math.random());
});
var MAX = 66;
//一共67个
var counter = 59;
var nowScoreData = 0;
var historyBestScoreData = 0;

var nowScore = document.getElementById('now_score');
var historyScore = document.getElementById('history_best_score');
var textNow = document.getElementById('text_now');
var textIn = document.getElementById('text_in');
var textOut = document.getElementById('text_out');

// localStorage.setItem("now_score", nowScoreData);//设置b为"isaac"
var historyBestScoreData = parseInt(localStorage.getItem("history_best_score"));//获取b的值,为"isaac"
if (isNaN(historyBestScoreData)) {
    historyBestScoreData = 0;
}
historyScore.innerHTML = "历史分数：<span>" + historyBestScoreData + "</span>";
// var a = localStorage.key(0); // 获取第0个数据项的键名，此处即为“b”
// localStorage.removeItem("b");//清除b的值
// localStorage.clear();//清除当前域名下的所有localstorage数据

textNow.innerHTML = textData[counter];

if('oninput' in textIn){
        textIn.addEventListener("input",getWord,false);
}else{
    textIn.onpropertychange = getWord;
}

function getWord(){
    if (textData[counter] == textIn.value) {
        counter++;
        nowScoreData ++;
        nowScore.innerHTML = "分数：<span>" + nowScoreData + "</span>";
        up_score("{{md_username}}", nowScoreData);
        if (nowScoreData > historyBestScoreData) {
            historyBestScoreData = nowScoreData;
            localStorage.setItem("history_best_score", historyBestScoreData);
        }
        historyScore.innerHTML = "历史分数：<span>" + historyBestScoreData + "</span>";

        textOut.innerHTML = textIn.value + "<span>√</span>";
        textOut.style.color = "green";
        textIn.value="";

        if (counter > MAX) {
            counter = 0;
        }
        textNow.innerHTML = textData[counter];

    } else {
        textOut.innerHTML = textIn.value;
        textOut.style.color = "red";
    }
}

function clearBestScoreData() {
    localStorage.clear();//清除当前域名下的所有localstorage数据
    historyScore.innerHTML = "历史分数：<span>0</span>";
}

function up_score(md_username, now_score){
     $.post({
        //给哪个页面发送网络请求  url取  域名后面的所有东西
        'url': '/up_score',
        //data是发送过去的数据s
        'data':{
            'md_username': md_username,
            'now_score': now_score
        },
        //如果网络请求发送成功，就会执行success里面的函数
        //请求成功 是状态码等于200就会执行success里面的函数
        // {#否则执行fail里面的函数#}
        'success': function(data){
             //data是服务器发送过来的数据
             //如果服务器发送过来的是json数据，那么JS底层会将json进行解析
             //比如 服务器发送过来的是JSON类型的字典，那么JS底层会将JSOn数据转换成一个对象
            if(data['code']==200){
                console.log(data);
             }else{
                alert(data['message']);
             }
             console.log(data);
        },
        //如果网络请求发送失败，就会执行fail里面的函数
        'fail': function(error){
            console.log(error)
        }
     });
}
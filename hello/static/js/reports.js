<script>
function numberWithCommas(x) {
    x = "" + x;
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}
var img = document.createElement('img');
img.setAttribute("id", "img-load-tracker");
img.setAttribute("src", "https://www.voya.ie/Interface/Icons/LoadingBasketContents.gif");
document.getElementById("div-data-buzztrackerjson").appendChild(img);
function onkeyupFunction(){
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    var links = document.getElementsByClassName("link-hit-sentence");
    for (i = 0; i < links.length; i++) {
        txtValue = links[i].textContent || links[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            links[i].parentNode.parentNode.style.display = "";
        } else {
            links[i].parentNode.parentNode.style.display = "none";
        }
    }    
}
function closeModal(){
    //var div = document.getElementsByClassName("div-modal");
    [].forEach.call(document.querySelectorAll('.div-modal'), function (el) {
      el.style.display = 'none';
    });
}
function onClickFunction(id){
   //console.log(window.dataReport[id]['Similar']);
   var datos = window.dataReport[id]['Similar'];
   var divv = document.createElement('div');
   divv.setAttribute("id", "modal-iframe");
   var newDiv = jQuery(document.createElement('div'));
   var father = document.getElementById("div-data-buzztrackerjson");
   divv.setAttribute("class", "div-modal");
   datos.sort(function(a,b) {
       return b['Twitter Followers'] - a['Twitter Followers'];
   });
   for (const property in datos) {
        var divcontainer = document.createElement('div');
        divcontainer.setAttribute("class", "div-modal-container");
        var div = document.createElement('div');
        div.setAttribute("class", "div-inside-modal-left");
        var link = document.createElement('a');
        link.setAttribute("target", "_blank");
        link.setAttribute("href", datos[property]["User Profile Url"]);
        link.innerHTML += datos[property]['Influencer'];//Twitter Bio, Twitter Followers
        div.appendChild(link);
        var div2 = document.createElement('div');
        div2.innerHTML += datos[property]['Twitter Bio'];//Twitter Bio, Twitter Followers
        div2.setAttribute("class", "div-inside-modal-center");
        var div3 = document.createElement('div');
        if (datos[property]['Source'] == "Twitter"){
          div3.innerHTML += numberWithCommas(datos[property]['Twitter Followers']);//Twitter Bio, Twitter Followers
        } 
        if (datos[property]['Source'] == "Facebook"){
          div3.innerHTML += numberWithCommas(datos[property]['Reach']);//Twitter Bio, Twitter Followers
        } 
        div3.setAttribute("class", "div-inside-modal-right");
       
        divcontainer.appendChild(div);
        divcontainer.appendChild(div2);
        divcontainer.appendChild(div3);
        divv.appendChild(divcontainer);
   }
  var div4 = document.createElement('div');
   div4.setAttribute("class", "div-inside-modal-close");
   div4.innerHTML += "x  ";
   div4.setAttribute("onclick", "closeModal()");
   divv.appendChild(div4);
   document.body.appendChild(divv);
};
jQuery(document).ready(function() {
    //console.log('load');
    var namFile = document.getElementById("div-data-buzztrackerjson");
    namFile = namFile.getAttribute('class');
    var request = jQuery.ajax({
      method: "GET",
      url: "https://ec2-52-38-13-82.us-west-2.compute.amazonaws.com:5000/buzztrackerjson/"+namFile+"/",
      dataType: "json"
  });
    
    request.done(function( msg ) {
        console.log(msg);
        document.getElementById("img-load-tracker").style.display = "none";
        var listRt = [];
        var data = {};
        var arrayData = [];
        for (const property in msg) {
            if (!listRt.includes(msg[property]["Hit Sentence"])){
                listRt.push(msg[property]["Hit Sentence"]);
                arrayData.push(msg[property]);//guarda un retweet sin que se repitan las sentence
                data[msg[property]["Hit Sentence"]] = msg[property];
                data[msg[property]["Hit Sentence"]]["Similar"] = [];
                data[msg[property]["Hit Sentence"]]["SimilarCant"] = 0;
            } else {
                data[msg[property]["Hit Sentence"]]["Similar"].push(msg[property]);
                data[msg[property]["Hit Sentence"]]["SimilarCant"] += 1;
          }    
        }  
        console.log("data");
        console.log(data);
        console.log("arraydata");
        console.log(arrayData);
        window.dataReport = data; 
        var byCont = arrayData.slice(0);
        
        console.log("consola loco");
        console.log(byCont);
        //console.log(window.dataReport);
        for (i = 0; i < byCont.length; i++) {
            var sentence = byCont[i]["Hit Sentence"];
            if (sentence.startsWith("RT @")){
                //console.log("sentence sin split");
                //console.log(sentence);
                sentence = sentence.split(/:(.+)/)[1];
                var stringSearch = sentence.trim();
                //console.log("sentence");
                //console.log(sentence);
                var similar =  byCont[i]["Similar"];
                var similarCant =  byCont[i]["SimilarCant"];
                
                //console.log(window.dataReport[stringSearch]);
                if (stringSearch in window.dataReport){
                    console.log(stringSearch);
                    console.log(byCont[i]);
                    for (e = 0; e < byCont.length; e++) {
                        var sentence2 = byCont[e]["Hit Sentence"];
                        if (stringSearch == sentence2){
                            byCont[i]["Similar"] = [];
                        byCont[i]["SimilarCant"] = 0;
                            let copy = Object.assign({}, byCont[i]);
                            similar.push(copy);
                          byCont[e]["Similar"] = similar;
                        byCont[e]["SimilarCant"] = similarCant + 1;
                            byCont.splice(i, 1); 
                            break;
                      }        
                    }
                    //byCont[i] = window.dataReport[stringSearch];
                    //byCont[i]["Similar"] = similar;
                    //byCont[i]["SimilarCant"] = similarCant;
              }    
            }
        }   
        byCont.sort(function(a,b) {
            return b.SimilarCant - a.SimilarCant;
        });
        var colors = ['rgb(237,216,18,0.6)','rgb(237,216,18,0.4)','rgb(237,216,18,0.2)','rgb(237,216,18,0.1)'];
      for (const property in byCont) {
            //console.log(property);
            var str = byCont[property]["URL"];
            if (str.includes("http") || str.includes("https")){
                var div = document.createElement('div');
                //div.innerHTML += msg[property]["Hit Sentence"]; Twitter Screen Name
                div.setAttribute("class", "container-iframe");
                var divp = document.createElement('div');
                divp.setAttribute("class", "puser-name");
                var link = document.createElement('a');
                link.setAttribute("target", "_blank");
                var img = document.createElement('img');
                img.setAttribute("class", "img-tracker");
                if (byCont[property]["Source"] == "Twitter"){
                    link.innerHTML += byCont[property]["Twitter Screen Name"];
                    img.setAttribute("src", "data:image/png;base64,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c291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjEtMDMtMjRUMTc6NTg6MjkrMDE6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjEtMDMtMjRUMTc6NTg6MjkrMDE6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDIxLTAzLTI0VDE3OjU4OjI5KzAxOjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjEwMmU5MmI0LThjYzktNGEyYS05ZGVkLTRhYzMyY2ZjMmIzZSIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjcxNmM2MzE3LTJkMGEtOGI0NS1hMzY1LTE1MThkZDhiNDlhYyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmM5MDRlMTMwLTk3MjEtNGUxNS05NGE5LTE4ZjgxNzU5YmFiMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJEaXNwbGF5Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpjOTA0ZTEzMC05NzIxLTRlMTUtOTRhOS0xOGY4MTc1OWJhYjAiIHN0RXZ0OndoZW49IjIwMjEtMDMtMjRUMTc6NTg6MjkrMDE6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChNYWNpbnRvc2gpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDoxMDJlOTJiNC04Y2M5LTRhMmEtOWRlZC00YWMzMmNmYzJiM2Ui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");
                }  
                if (byCont[property]["Source"] == "Facebook"){
                    link.innerHTML += byCont[property]["Influencer"];
                    img.style.top = "0.5rem";
                    img.style.width = "32px";
                    img.setAttribute("src", "data:image/png;base64,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c291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoTWFjaW50b3NoKSIgeG1wOkNyZWF0ZURhdGU9IjIwMjEtMDMtMjRUMTc6NTk6NDUrMDE6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjEtMDMtMjRUMTc6NTk6NDUrMDE6MDAiIHhtcDpNb2RpZnlEYXRlPSIyMDIxLTAzLTI0VDE3OjU5OjQ1KzAxOjAwIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjg3ZjU3ZGIwLTI2ZjQtNDhmNi05MTVjLTljMDg3NTQwYWZlZSIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOmRkNTZlYTYzLWUyOTItYzE0Mi05ZWEzLTFiOWM5YjQ1YTRiMyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjE4NTNlNzJiLTI4NDAtNGY1ZS05MjdmLThhNmViM2EzMDQ5MSIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJEaXNwbGF5Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDoxODUzZTcyYi0yODQwLTRmNWUtOTI3Zi04YTZlYjNhMzA0OTEiIHN0RXZ0OndoZW49IjIwMjEtMDMtMjRUMTc6NTk6NDUrMDE6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChNYWNpbnRvc2gpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo4N2Y1N2RiMC0yNmY0LTQ4ZjYtOTE1Yy05YzA4NzU0MGFmZWUi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");
                }
                if (!["Twitter","Facebook"].includes(byCont[property]["Source"])){
                    img = document.createElement('div');
                  img.setAttribute("class", "img-tracker");
                    img.innerHTML += byCont[property]["Source"];
                }
                link.setAttribute("href", byCont[property]["User Profile Url"]);
                link.style.fontSize = "16px";
                divp.appendChild(link);
                var p2 = document.createElement('p');
                p2.innerHTML += byCont[property]["Date"];
                var p3 = document.createElement('p');
                var link2 = document.createElement('a');
                link2.setAttribute("target", "_blank");
                link2.style.fontSize = "12px";
                link2.style.cssText = "color: #56380f !important;font-size: 12px;";
                link2.setAttribute("href", byCont[property]["URL"]);
                link2.setAttribute("class", "link-hit-sentence");
                //var sentences = byCont[property]["Hit Sentence"];
                link2.innerHTML += byCont[property]["Hit Sentence"];
                p3.appendChild(link2);
                p2.style.padding = "0px 0px 0px 0px";
                p2.style.color = "#55adee";
                p3.style.padding = "0px 0px 0px 0px";
                var div2 = document.createElement('div');
                if (str.includes("twitter")){
                  div2.innerHTML += byCont[property]["SimilarCant"] + " RT";
                } else {
                    div2.innerHTML += byCont[property]["SimilarCant"] + " Share";
                }
                if (byCont[property]["SimilarCant"] > 10){
                    //document.getElementsByClassName('similar-cant')[0].parentNode.style.backgroundColor = colors[0];
                }
                if (byCont[property]["SimilarCant"] > 7){
                    //document.getElementsByClassName('similar-cant')[0].parentNode.style.backgroundColor = colors[1];
                }
                if (byCont[property]["SimilarCant"] > 5){
                    //document.getElementsByClassName('similar-cant')[0].parentNode.style.backgroundColor = colors[2];
                }
                if (byCont[property]["SimilarCant"] > 2){
                    //document.getElementsByClassName('similar-cant')[0].parentNode.style.backgroundColor = colors[3];
                }
                div2.setAttribute("class", "similar-cant");
                div2.setAttribute("title", byCont[property]["SimilarCant"] + " ReTweets");
                var div3 = document.createElement('div');
                div3.setAttribute("class", "similar-cant");
                var link3 = document.createElement('a');
                //link3.setAttribute("href", "#");
                link3.setAttribute("class", "a-similar-cant");
                link3.setAttribute("data", byCont[property]["Hit Sentence"]);
                var hit = byCont[property]["Hit Sentence"];
                link3.setAttribute("onclick", "onClickFunction("+"'"+hit+"'"+")");
                if (byCont[property]["SimilarCant"] > 0){
                    link3.setAttribute("title", "Haga click!");
                  link3.innerHTML += "+  ";
                }
                var div4 = document.createElement('div');
                div4.setAttribute("class", "followers");
                div4.innerHTML += "Followers: ";
                div4.innerHTML += numberWithCommas(byCont[property]['Twitter Followers']);
                
                div3.appendChild(link3);
                div.appendChild(divp);
                div.appendChild(img);
                div.appendChild(div4);
                div.appendChild(div2);
                div.appendChild(div3);
                
                div.appendChild(p2);
                div.appendChild(p3);
                
                
                document.getElementById("div-data-buzztrackerjson").appendChild(div);
            }
        //console.log(`${property}: ${msg[property]}`);
    }
        var divInput = document.createElement('div');
        divInput.setAttribute("class", "div-input");
        var input = document.createElement('input');
        input.setAttribute("onkeyup", "onkeyupFunction()");
        input.setAttribute("id", "myInput");
        input.setAttribute("placeholder", "Buscar");
        divInput.appendChild(input);
        document.getElementById("div-data-buzztrackerjson").parentNode.insertBefore(divInput, document.getElementById("div-data-buzztrackerjson"));
  });
    request.fail(function( jqXHR, textStatus ) {
      document.getElementById("div-data-buzztrackerjson").innerHTML += textStatus;
        document.getElementById("div-data-buzztrackerjson").innerHTML += jqXHR.responseText;
        console.log(jqXHR.responseText);
  });
    
    
    
});
</script>
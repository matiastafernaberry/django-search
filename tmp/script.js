<script>
var img = document.createElement('img');
img.setAttribute("id", "img-load-tracker");
img.setAttribute("src", "https://www.voya.ie/Interface/Icons/LoadingBasketContents.gif");
document.getElementById("div-data-buzztrackerjson").appendChild(img);
    
jQuery(document).ready(function() {
    console.log('load');
   //jQuery.get( "http://ec2-52-38-13-82.us-west-2.compute.amazonaws.com:5000/buzztrackerjson/", function( data ) {
   //    console.log(data);
    //  jQuery("#div-data-buzztrackerjson").html( data );
   //});
    var request = jQuery.ajax({
        method: "GET",
        url: "https://ec2-52-38-13-82.us-west-2.compute.amazonaws.com:5000/buzztrackerjson/",
        dataType: "json"
    });
    request.done(function( msg ) {
        console.log(msg);
         document.getElementById("img-load-tracker").style.display = "none";
        for (const property in msg) {
            var str = property;
            if (str.includes("http") || str.includes("https")){
                var div = document.createElement('div');
                //div.innerHTML += msg[property]["Hit Sentence"]; Twitter Screen Name
                div.setAttribute("class", "container-iframe");
                var p = document.createElement('p');
                p.setAttribute("class", "puser-name");
                p.innerHTML += msg[property]["Influencer"];
                var img = document.createElement('img');
                img.setAttribute("class", "img-tracker");
                if (str.includes("twitter")){
                    img.setAttribute("src", "data:image/png;base64,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");
                }
                if (str.includes("facebook")){
                    img.style.top = "0.5rem";
                    img.setAttribute("src", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATYAAACjCAMAAAA3vsLfAAAAaVBMVEX///86VZ80UZ1perEpSZrBxtzp7PQrTJv4+fwxUJ6apcucqMs4U56ToMpBXaWuuNgiRZjL0OJgc61WbKvy9PmPnMbY3erg5O/s7/Z1hrvFzOGostF9jL1HYaemsdJTaqy6wt2Aj74WP5bhAZYmAAADDklEQVR4nO3c7XKaQBiG4airuIoRMcaPaNv0/A+yojFJhXdlnzJq5b5/M7BzDQizrDw9Ef2Xzfp33OzWOmZ55u62LL+1jlmv27nbur1b65jBJgWbFGxSsEnBJgWbFGxSsEnBJgWbFGxSsEnBJgWbFGxSsEnBJgWbFGxSV2ZLK4PN9Or6xDmXVGa4tZ7Nu2S+mM5el4OqVs+wlUuTZL1ZhQbxXH26tZrNdd6GFwYB23k+mV4eBGxnZduXGoOA7a9S1681CNi+53eDeoOA7bva/NKt4BRsihpsX6W72mqwfeVq/q4VwXYqq3cPPQbbR/49ZhCwndjqPOV+Btsx9xY1CNiO+bhBwHYo+RE3CNiKUhf1ywbbMb+OHARsRW4TOQjYOsUkeOQ1CtuB7WfsIGDb5xfhQw7607N4c7UvCT7rbuZZ6W2psaN2sbnQ30C3mfUOvu1s2dI+XG6dWbAF2CYuZkftYkvMCcpVxBUK22fjmEsUtlN51MkG20fGYy1sQbahj9sRbIeGnrMNNtiig00KNinYpGCTgk0KNinYpGCTgk0KNinYpJg4kvpHttSXSjKTzSXlzfdZQ3hYtrQ3HpWamEtAytsWjbfGWfiwbH7SxBh+GW9mYAs24mxT4iKVmrftEwPNsFnPJbCFeslgE3q11tPAFmoDm9Jb61ZTNsK24JagtIZNade6L2o1wWZPJ8EWaGCu54UtkPnYBlsoa9oItmD2OmjYAr1zS1Cypo1gC2YvH4fNbmV9BxW2UEtrtg22UOa0EWyhpvb/sB6WLc3H5Ubm6+WKjceBATwsW/Ep4lL2YoasYuvA8R+XrSqWzjTNxkIt2GCLDjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KRgk4JNCjYp2KTyzDXdb/tjPXE7yvKrUsQ06zff0DpY7I5m15Qgaq4/5rp8lQU7GZoAAAAASUVORK5CYII=");
                }
                
                var p2 = document.createElement('p');
                p2.innerHTML += msg[property]["Date"];
                p2.innerHTML += msg[property]["Hit Sentence"];
                p2.style.padding = "0px 0px 0px 0px";
                div.appendChild(p);
                div.appendChild(img);
                div.appendChild(p2);
                document.getElementById("div-data-buzztrackerjson").appendChild(div);
            }
            console.log(`${property}: ${msg[property]}`);
        }

    });

});
</script>
$(document).ready(function(){
$.ajax({ url: "http://localhost:8080/question",
        context: document.body,
        success: function(result){
           $("#question").text(JSON.stringify(result))
        }});


$("#submitbtn").click(function(e) {
    
	alert("clicked button")
    $.ajax({
        type: "POST",
        url: "http://localhost:8080/question",
        data: { 
            question: $("#question").text(),
            answer: $("#exampleFormControlTextarea1").text() 
        },
        success: function(result) {
            alert(JSON.stringify(result))
        },
        error: function(result) {
            alert('error');
        }
    });
});

});



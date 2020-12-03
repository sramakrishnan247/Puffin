$(document).ready(function(){
$.ajax({ url: "http://18.205.246.12:8080/question",
        context: document.body,
        success: function(result){
           $("#question").text(result["question"])
        }});


$("#submitbtn").click(function(e) {
    
	var question = $("#question").text()
	var answer = $("#exampleFormControlTextarea1").val()

	data = JSON.stringify({ "question":question, "answer":answer})

	
    $.ajax({
        type: "POST",
        url: "http://18.205.246.12:8080/question",
        data: data 
        ,
	contentType:"application/json; charset=utf-8",
	dataType:"json",
        success: function(result) {
             $("#question").text(result["question"])
	     console.log(JSON.stringify(result))
        },
        error: function(result) {
            console.log('error');
        }
    });
});

});



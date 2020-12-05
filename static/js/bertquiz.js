$(document).ready(function(){
	
$('#alertdiv').hide()

correctAnswer = ""
$.ajax({ url: "http://18.205.246.12:8080/bertquiz/question",
        context: document.body,
        success: function(result){
		   $("#paragraph").text(result["paragraph"])
           $("#question").text(result["question"])
		   correctAnswer = result["answer"]
        }});


$("#submitbtn").click(function(e) {
    
	var question = $("#question").text()
	var answer = $("#exampleFormControlTextarea1").val()

	data = JSON.stringify({ "correctAnswer":correctAnswer, "userAnswer":answer})

	
    $.ajax({
        type: "POST",
        url: "http://18.205.246.12:8080/bertquiz/question",
        data: data 
        ,
	contentType:"application/json; charset=utf-8",
	dataType:"json",
        success: function(result) {
			 $("#paragraph").text(result["paragraph"])
             $("#question").text(result["question"])
			console.log(JSON.stringify(result))
			
			$('#alertdiv').show()
			$('#alerterrbox').hide()
			$('#alertmsg').text(result["sentiment"]+", Similarity: "+ result["similarity"])
			$('#alertmsg').show()
		 
        },
        error: function(result) {
            console.log('error');
			$('#alerterrmsg').show()
			$('#alertsuccessbox').hide()
			$('#alertdiv').show()
			
        }
    });
});

});



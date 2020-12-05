$(document).ready(function(){
	
$('#alertdiv').hide()

var correctAnswer = ""

$.ajax({ url: "http://localhost:5000/bertquiz/question",
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
    console.log("24"+", "+correctAnswer)
	
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/bertquiz/question",
        data: data,
        cache: false
        ,
	contentType:"application/json; charset=utf-8",
	dataType:"json",
        success: function(result) {
			 $("#paragraph").text(result["paragraph"])
             $("#question").text(result["question"])
            prevCorrectAnswer = correctAnswer 
            correctAnswer = result["answer"]
            
            var msg = ""
            if(result["sentiment"] === "entailment" && parseFloat(result["similarity"]) > 0.65){
                msg = "Correct Answer!!"
            }
            else{
                msg = "Not so accurate!" + "\n" + "Correct Answer is:  " + prevCorrectAnswer  
            }

			$('#alertdiv').show()
			$('#alerterrbox').hide()
			$('#alertmsg').text(msg)
			$('#alertmsg').show()
            $("#exampleFormControlTextarea1").val('') 
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



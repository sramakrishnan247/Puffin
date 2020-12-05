$(document).ready(function(){
	
$('#alertdiv').hide()

$.ajax({ url: "http://localhost:5000/bertmatch/question",
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
        url: "http://localhost:5000/bertmatch/question",
        data: data 
        ,
	contentType:"application/json; charset=utf-8",
	dataType:"json",
        success: function(result) {
             $("#question").text(result["question"])
			console.log(JSON.stringify(result))
			
			$('#alertdiv').show()
			$('#alerterrbox').hide()
			$('#alertmsg').text(result["sentiment"]+", Similarity: "+ result["similarity"])
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



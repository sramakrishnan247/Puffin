$(document).ready(function(){
$.ajax({ url: "http://localhost:5000/question",
        context: document.body,
        success: function(result){
           $("#question").text(result.data[0].employee_name)
        }});


$("#submitbtn").click(function(e) {
    
	alert("clicked button")
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/question",
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



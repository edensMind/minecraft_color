// Create Script

function createScript() {
	// console.log("createScript: "+drawingDoc+" : "+drawingDoc.length);
	var drawingDocJSON = JSON.stringify(drawingDoc);
	console.log(drawingDocJSON);

	$.ajax({
		url: "/ahk",
		method: "POST",
		data:{
			"drawingDocJSON":drawingDocJSON
			// "drawingDocJSON":"test"
		},
		success: function(data) {
			console.log("Sent JSON to python");
		},
		error: function(error) {
		    console.log(error);
		}
	});
}
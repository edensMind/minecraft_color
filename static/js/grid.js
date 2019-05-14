// Coloring Grid
////////////////////////////////////////////////////////////////////////////
// Global vars
var drawingDoc = {};
var this_x = 35;
var this_y = 35;

var mouseIsDown = false;

// onload function
(function () {
	// init grid on page load 
    setGrid(this_x,this_y);
    
})();

////////////////////////////////////////////////////////////////////////////
function setGridSize() {
	var x = document.getElementById("x_form").value;	
	var y = document.getElementById("y_form").value;	
	setGrid(parseInt(x),parseInt(y));
}

////////////////////////////////////////////////////////////////////////////
function setGrid(x,y) {

	this_x = x;
	this_y = y;


	var grid_parent = document.getElementById("grid");

	console.log("Setting Grid..\nSize: "+x+" by "+y);

	//start html
	var grid_list_html = "<table id='grid_table'>\n";

	// row numbers
	var column_num = 1;
	var row_num = 1;
	for(var iy=0; iy<=y; iy++) {
		grid_list_html += "<tr class='row'>\n";
		// # columns
		for(var ix=0; ix<=x; ix++) {
			if (ix===0 && iy===0) {
				grid_list_html += "<td align='right'><div  class='cell cell-edge top-edge'></div></td>\n";
			}
			else if (iy===0) {
				grid_list_html += "<td align='right'><div  class='cell cell-edge top-edge'>"+column_num+"</div></td>\n";
				column_num += 1;
			}
			else if (ix===0 && iy>0) {
				grid_list_html += "<td align='right'><div  class='cell cell-edge left-edge'>"+row_num+"</div></td>\n";
				row_num += 1;
			}
			else {	
				grid_list_html += "<td><div id='x"+ix+"y"+iy+"' onclick='setColor(this)' oncontextmenu='return removeColor(this)' ondrag='setColor(this)' class='cell cell-color'></td>\n";
			}

		}
		grid_list_html += "</tr>\n";

	}

	//end html
	grid_list_html += "</div><table>\n";

	// set grid html
	grid_parent.innerHTML = grid_list_html;

	// get grid colors
	setDrawingDocument();
	getDrawingDocument(x,y);


}

////////////////////////////////////////////////////////////////////////////
function setColor(this_cell) {
	//console.log("Setting Color: "+this_cell.id);
	this_cell.style.backgroundColor = "rgb("+selectedColor+")";

	setDrawingDocument();
}

////////////////////////////////////////////////////////////////////////////
function removeColor(this_cell) {
	//console.log("Removing Color: "+this_cell.id);
	this_cell.style.backgroundColor = "transparent";

	setDrawingDocument();

	return false;
}

////////////////////////////////////////////////////////////////////////////
function setDrawingDocument() {
	//console.log("Setting Document... ");
	drawingDoc = {};
	var cells = document.getElementsByClassName("cell-color");

	for(var i=0; i<cells.length; i++) {
		drawingDoc[cells[i].id] = cells[i].style.backgroundColor;
	}
}

////////////////////////////////////////////////////////////////////////////
function getDrawingDocument(x,y) {
	//console.log("Getting Document Data... ");
	for(var cell_id in drawingDoc) {
		var color = drawingDoc[cell_id];
		//console.log(cell_id + " : " +color);

		let matches = cell_id.match(/(\d+)/g);
	  
	  	try {
	  		var x = document.getElementById(cell_id).style.backgroundColor = color;
		}
		catch(err) {
			console.log(err.message);
		}
	}
}

////////////////////////////////////////////////////////////////////////////
function clearGrid() {
	drawingDoc = {};
	var cells = document.getElementsByClassName("cell-color");
	console.log("len: "+cells.length);
	for(var i=0; i<cells.length; i++) {
		cells[i].style.backgroundColor = "transparent";
	}
}





grid.addEventListener('mousedown', e => {
	console.log("mouseIsDown");
	mouseIsDown = true;
});

document.addEventListener('mouseup', e => {
	console.log("mouseIsUP");
	mouseIsDown = false;
});

$(document).mousemove(function(event){
	if (mouseIsDown) {
		//console.log(event.button)
		var x = event.clientX
		var y = event.clientY

		var elementMouseIsOver = document.elementFromPoint(x, y);
		//console.log("CELL: " +elementMouseIsOver.id);

		if (elementMouseIsOver.id.match(/^x\d+y\d+$/g)) {
			if (event.which == 1) { // left mouse
				setColor(elementMouseIsOver);
			}
			else if (event.which == 3) { // right mouse
				console.log("removeColor");
				removeColor(elementMouseIsOver);
			}
		}
	}
});


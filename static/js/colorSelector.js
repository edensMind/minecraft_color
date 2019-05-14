// ColorSelector
////////////////////////////////////////////////////////////////////////////
// Global vars
var selectedColor = "25, 25, 25"; // default black

// onload function
(function () {
	console.log("ColorSelector");

})();

function selectColor(this_color_option, rgb) {
	selectedColor = rgb;
}
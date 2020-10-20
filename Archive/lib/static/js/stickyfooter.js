// ------------------------------------------
// Return total viewport size, aka the screen size
function getViewPortHeight() {
  return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
}
// ------------------------------------------
// Return how much HTML we're actually presenting
function getBodyHeight() {
  var body = document.body;
  var height = body.offsetHeight;
  return height;
}
// ------------------------------------------
// Get the difference between screen size and what we're presenting
function calculateOffset(viewportHeight, actualHeight) {
  return viewportHeight - actualHeight;
}
// ------------------------------------------
// Adds a 'push' to the last section on a page if it doesn't fill the viewport
function updateOffset(difference) {
  // console.log('In update offsetHeight')

  // Make reference to body and retrieve all elements with this tag as a vector
  var body = document.body;
  /*
  Was adding padding to the last section before, but I prefer the way it looks
  adding padding to the footer instead. Keeps the layout more consistent.
  */
  var sections = body.getElementsByTagName('footer');

  // Retrieve last element from vector and log it's styling if it exists
  var lastElement = sections[sections.length-1];
  // Access computed style to see embedded CSS from class
  style = getComputedStyle(lastElement)

  // Now let's check and see if some value already exists
  var existingPadding = String(style.paddingBottom);
  if (existingPadding != "") {
    // console.log('There was existing padding')
    // This means we have some existing padding
    // Parse existingPadding as a substring to remove the 'px'
    existingPadding = existingPadding.substring(0,existingPadding.length-2);

    // Cast to Integer then check its type to be sure
    existingPadding = parseInt(existingPadding);
    // console.log(typeof existingPadding);

    // Then add it to the 'difference' variable to account for it
    difference = difference + existingPadding;
  }

  // Once we've checked for existing value, we can mve forward with updating the styling
  differenceAsString = String(difference)+"px"; // Make a string out of it
  // console.log('About to update padding with value: '+differenceAsString)
  lastElement.style.paddingBottom = differenceAsString; // Apply styling
}
// ------------------------------------------
var vw = getViewPortHeight();
var realheight = getBodyHeight();

// If content is less than the screen size in height, apply correction
if (realheight < vw) {
  // console.log('We have an overflow');
  var diff = calculateOffset(vw, realheight);
  // console.log('Overflow amount is '+ String(diff));
  updateOffset(diff);
}
// ------------------------------------------

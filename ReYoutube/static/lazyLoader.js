// @credit: Julian Nash https://pythonise.com/categories/javascript/infinite-lazy-loading

// Get references to the dom elements
var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');

// Set a counter to count the items loaded
var counter = 0;
const video_id = document.querySelector('meta[name="video_id"]').content;
// Function to request new items and render to the dom
function loadItems() {

 const data = {
    video_id: video_id,
    counter: counter,
};

 const options = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
        'Content-Type': 'application/json'
    }
}

  const url = '/api/comments/load';
  // Use fetch to request data and pass the counter value in the QS
  fetch(url, options).then((response) => {

    // Convert the response data to JSON
    response.json().then((data) => {

      // If empty JSON, exit the function
      if (!data.length) {

        // Replace the spinner with "No more posts"
        sentinel.innerHTML = "No more comments";
        return;
      }

      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {

        // Clone the HTML template
        let template_clone = template.content.cloneNode(true);
        console.log(data[i]);
        // Query & update the template content
        template_clone.querySelector("#comment-title").innerHTML = `${data[i].user.username}: ${data[i].created_at[1]}`;
        template_clone.querySelector("#comment-content").innerHTML = data[i].comment;

        // TODO: load user profile picture, if the css fits
        //template_clone.querySelector("#comment-picture").src = data[i].user.profile_picture;

        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;

        // Update the counter in the navbar
        //loaded.innerText = `${counter} items loaded`;

      }
    })
  })
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {

  // Uncomment below to see the entry.intersectionRatio when
  // the sentinel comes into view

  // entries.forEach(entry => {
  //   console.log(entry.intersectionRatio);
  // })

  // If intersectionRatio is 0, the sentinel is out of view
  // and we don't need to do anything. Exit the function
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  // Call the loadItems function
  loadItems();

});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);
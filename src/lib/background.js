var latestImage;

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
	  if (request.command === 'screenGrab') {
			chrome.tabs.captureVisibleTab(sender.tab.windowId, {format: 'jpeg', quality: 50}, function (image) {
				 // You can add that image HTML5 canvas, or Element.
				latestImage = image;
				console.log(request);
			});
		} else if (request.command === 'log' ) {
			console.log(request);
			$.ajax({
				url: 'http://localhost:3000/save', 
				data: JSON.stringify({
				  image: latestImage,
				  event: request
				}),
        type: 'POST',
        contentType : 'application/json',
			});
		}
	}
);


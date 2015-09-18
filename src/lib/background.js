chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    chrome.tabs.captureVisibleTab(null, {}, function (image) {
       // You can add that image HTML5 canvas, or Element.
    	console.log('called');
    });
	}
);


var latestImages = {};

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.command === 'screenGrab') {
      chrome.tabs.captureVisibleTab(sender.tab.windowId, {format: 'jpeg', quality: 90}, function (image) {
         // You can add that image HTML5 canvas, or Element.
        latestImages[sender.tab.windowId] = image;
      });
    } else if (request.command === 'log' && latestImages[sender.tab.windowId] ) {
      $.ajax({
        url: 'http://localhost:3000/save', 
        data: JSON.stringify({
          image: latestImages[sender.tab.windowId],
          data: request
        }),
        type: 'POST',
        contentType : 'application/json',
      });
      delete latestImages[sender.tab.windowId];
    }
  }
);


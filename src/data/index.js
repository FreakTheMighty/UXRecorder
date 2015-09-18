debugger;
console.log('background');
chrome.runtime.sendMessage({greeting: "hello"}, function(response) {
  console.log(response.farewell);
});



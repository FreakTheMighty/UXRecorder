console.log('background');
document.addEventListener('click', function(e){
  chrome.runtime.sendMessage({
		  command: 'log',
			event:{
				eventName: 'click', 
		    mouseX: e.pageX/window.innerWidth,
		    mouseY: e.pageY/window.innerHeight,
		  }
	});
});

setInterval(function(){
	chrome.runtime.sendMessage({command: 'screenGrab'});
}, 1000);

document.onload = function(){
	chrome.runtime.sendMessage({command: 'screenGrab'});
};

$(document).ready(function(){
	chrome.runtime.sendMessage({command: 'screenGrab'});
});

chrome.runtime.sendMessage({command: 'screenGrab'});



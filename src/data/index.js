console.log('background');
document.addEventListener('click', function(e){
  chrome.runtime.sendMessage({
      command: 'log',
      event:{
        eventName: 'click', 
        mouseX: e.clientX/window.innerWidth,
        mouseY: e.clientY/window.innerHeight,
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

$(document).on('scrollstop',function(){
  chrome.runtime.sendMessage({command: 'screenGrab'});
});

$(window).resize( _.debounce( function(){
  chrome.runtime.sendMessage({command: 'screenGrab'});
}, 250 ));



chrome.runtime.sendMessage({command: 'screenGrab'});



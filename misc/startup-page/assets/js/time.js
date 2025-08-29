// ┌┬┐┬┌┬┐┌─┐
//  │ ││││├┤
//  ┴ ┴┴ ┴└─┘
// Set time

const displayClock = () => {
  const now = new Date();
  const timeString = now.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
  
  document.getElementById('time').innerText = timeString;

  setTimeout(displayClock, 1000);
}

window.addEventListener("DOMContentLoaded", displayClock);

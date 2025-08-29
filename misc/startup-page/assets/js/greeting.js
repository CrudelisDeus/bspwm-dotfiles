// ┌─┐┬─┐┌─┐┌─┐┌┬┐┬┌┐┌┌─┐┌─┐
// │ ┬├┬┘├┤ ├┤  │ │││││ ┬└─┐
// └─┘┴└─└─┘└─┘ ┴ ┴┘└┘└─┘└─┘
// Function to set Greetings

const today = new Date();
const hour = today.getHours();
const name = 'dmytro'; // Можно изменить на ваше имя

let greeting = '';

if (hour >= 23 || hour < 6) {
	greeting = 'Good night, ';
} else if (hour >= 6 && hour < 12) {
	greeting = 'Good morning, ';
} else if (hour >= 12 && hour < 17) {
	greeting = 'Good afternoon, ';
} else {
	greeting = 'Good evening, ';
}

document.getElementById('greetings').innerText = greeting + name;

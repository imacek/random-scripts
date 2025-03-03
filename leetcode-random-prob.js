// Select random problem from study plan
const els = document.querySelectorAll('[href*=problems]');
const ridx = Math.floor(Math.random() * els.length)
els[ridx].scrollIntoView();
els[ridx].click()

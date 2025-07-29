window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll)

function handleScroll() {
  const upElements = document.querySelectorAll('.fade-in-up');
  upElements.forEach((element, index) => {
    const position = element.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.2;

    if (position < screenPosition) {
      element.style.setProperty('--delay', index);
      element.classList.add('visible');
    }
    
  });

  const downElements = document.querySelectorAll('.fade-in-down');
  downElements.forEach((element, index) => {
    const position = element.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.2;

    if (position < screenPosition) {
      element.classList.add('visible');
    }
  });

  const rightElements = document.querySelectorAll('.fade-in-right');
  rightElements.forEach((element, index) => {
    const position = element.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.2;

    if (position < screenPosition) {
      element.classList.add('visible');
    }
  });

  const leftElements = document.querySelectorAll('.fade-in-left');
  leftElements.forEach((element, index) => {
    const position = element.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.2;

    if (position < screenPosition) {
      element.classList.add('visible');
    }
  });
}
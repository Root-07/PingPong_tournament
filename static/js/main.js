// Fonction pour afficher ou masquer certaines sections de la page
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');
    
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
      activeSection.style.display = 'block';
    }
  }
  
  // Fonction pour gérer la navigation entre différentes sections
  function handleNavigation(event) {
    const targetSection = event.target.getAttribute('data-section');
    if (targetSection) {
      showSection(targetSection);
    }
  }
  
  // Initialisation de la navigation
  function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', handleNavigation);
    });
  }
  
  // Exécuter les fonctions de base au chargement de la page
  document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    showSection('tournaments-section'); // Par défaut, afficher la section des tournois
  });
  
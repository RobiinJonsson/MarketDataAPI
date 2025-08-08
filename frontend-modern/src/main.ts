import './styles/main.css';
import { SearchComponent } from './components/SearchComponent.js';

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('MarketData Frontend initialized');
  
  // Initialize search component if search container exists
  const searchContainer = document.getElementById('search-container');
  if (searchContainer) {
    new SearchComponent('search-container');
  }
  
  // Initialize tab functionality
  initializeTabs();
});

function initializeTabs(): void {
  const tabButtons = document.querySelectorAll('[data-tab]');
  const tabPanes = document.querySelectorAll('[data-tab-pane]');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabName = button.getAttribute('data-tab');
      
      // Update active tab button
      tabButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      
      // Update active tab pane
      tabPanes.forEach(pane => {
        pane.classList.remove('active');
        if (pane.getAttribute('data-tab-pane') === tabName) {
          pane.classList.add('active');
        }
      });
    });
  });
}

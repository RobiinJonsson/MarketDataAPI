import './styles/main.css';
import { Router } from './router/Router';
import { Navigation } from './components/navigation/Navigation';

// Import page components
import HomePage from './pages/HomePage';
import InstrumentsPage from './pages/InstrumentsPage';
import InstrumentDetailPage from './pages/InstrumentDetailPage';
import EntityDetailPage from './pages/EntityDetailPage';
import AnalyticsPage from './pages/AnalyticsPage';
import DataOpsPage from './pages/DataOpsPage';
import SwaggerPage from './pages/SwaggerPage';


// Dynamic import for EntitiesPage to avoid module resolution issues
const EntitiesPageImport = () => import('./pages/EntitiesPage');

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('MarketData Modern Frontend initialized');
  
  try {
    // Initialize navigation
    const navigation = new Navigation('navigation-container');
    
    // Initialize router
    const router = new Router('main-content');
    
    // Register routes
    router.addRoute({
      path: '/',
      title: 'Dashboard',
      component: () => Promise.resolve({ default: HomePage }),
      icon: 'home',
      description: 'System overview and quick access to all features'
    });

    router.addRoute({
      path: '/instruments',
      title: 'Instruments Hub',
      component: () => Promise.resolve({ default: InstrumentsPage }),
      icon: 'instruments',
      description: 'Comprehensive instrument analysis and management'
    });

    router.addRoute({
      path: '/instruments/:isin',
      title: 'Instrument Details',
      component: () => Promise.resolve({ default: InstrumentDetailPage }),
      description: 'Detailed instrument information and analysis'
    });

    router.addRoute({
      path: '/entities',
      title: 'Entity Management',
      component: EntitiesPageImport,
      icon: 'entities',
      description: 'Legal entity relationships and LEI information'
    });

    router.addRoute({
      path: '/entities/:lei',
      title: 'Entity Details',
      component: () => Promise.resolve({ default: EntityDetailPage }),
      description: 'Detailed entity information and corporate relationships'
    });

    router.addRoute({
      path: '/analytics',
      title: 'Analytics Dashboard',
      component: () => Promise.resolve({ default: AnalyticsPage }),
      icon: 'analytics',
      description: 'Multi-dimensional analytics and visualizations'
    });

    router.addRoute({
      path: '/dataops',
      title: 'DataOps Center',
      component: () => Promise.resolve({ default: DataOpsPage }),
      icon: 'dataops',
      description: 'Data operations and file management'
    });

    router.addRoute({
      path: '/swagger',
      title: 'API Documentation',
      component: () => Promise.resolve({ default: SwaggerPage }),
      icon: 'swagger',
      description: 'Interactive API documentation and testing'
    });





    // Custom router event to update navigation
    const originalHandleRoute = router['handleRoute'].bind(router);
    router['handleRoute'] = async function(path: string) {
      navigation.setActiveRoute(path);
      return originalHandleRoute(path);
    };

    // Initialize router
    router.init();
    
  } catch (error) {
    console.error('Error initializing application:', error);
    
    // Show error state
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.innerHTML = `
        <div class="min-h-screen flex items-center justify-center">
          <div class="bg-red-50 border border-red-200 rounded-lg p-8 max-w-md">
            <div class="flex items-center mb-4">
              <svg class="w-6 h-6 text-red-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
              </svg>
              <h2 class="text-red-800 text-lg font-semibold">Application Error</h2>
            </div>
            <p class="text-red-700 mb-4">There was an error initializing the application.</p>
            <button 
              onclick="window.location.reload()" 
              class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
            >
              Reload Application
            </button>
          </div>
        </div>
      `;
    }
  }
});

/**
 * Main Navigation Component
 * Professional navigation with mobile responsiveness
 */

export class Navigation {
  private container: HTMLElement;
  private isMobileMenuOpen: boolean = false;

  constructor(containerId: string) {
    const container = document.getElementById(containerId);
    if (!container) {
      throw new Error(`Container element with ID '${containerId}' not found`);
    }
    this.container = container;
    this.render();
    this.initializeEventListeners();
  }

  private render(): void {
    this.container.innerHTML = `
      <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            
            <!-- Logo and Brand -->
            <div class="flex items-center">
              <div class="flex-shrink-0 flex items-center">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
                  </svg>
                </div>
                <div>
                  <h1 class="text-xl font-bold text-gray-900">MarketData API</h1>
                  <p class="text-xs text-gray-500 hidden sm:block">Enterprise Market Data Platform</p>
                </div>
              </div>
            </div>

            <!-- Desktop Navigation -->
            <div class="hidden md:flex items-center space-x-1">
              <a href="#" data-route="/" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
                </svg>
                Dashboard
              </a>
              
              <a href="#" data-route="/instruments" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Instruments
              </a>
              
              <a href="#" data-route="/entities" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"></path>
                </svg>
                Entities
              </a>
              
              <a href="#" data-route="/analytics" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
                </svg>
                Analytics
              </a>
              
              <a href="#" data-route="/dataops" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"></path>
                </svg>
                DataOps
              </a>
              
              <a href="#" data-route="/swagger" class="nav-link px-3 py-2 rounded-md text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
                API Docs
              </a>
            </div>

            <!-- Mobile Menu Button -->
            <div class="md:hidden flex items-center">
              <button 
                id="mobile-menu-button"
                class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="md:hidden hidden">
          <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-200">
            <a href="#" data-route="/" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
              </svg>
              Dashboard
            </a>
            
            <a href="#" data-route="/instruments" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Instruments
            </a>
            
            <a href="#" data-route="/entities" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"></path>
              </svg>
              Entities
            </a>
            
            <a href="#" data-route="/analytics" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
              </svg>
              Analytics
            </a>
            
            <a href="#" data-route="/dataops" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"></path>
              </svg>
              DataOps
            </a>
            
            <a href="#" data-route="/swagger" class="mobile-nav-link block px-3 py-2 rounded-md text-base font-medium transition-colors">
              <svg class="w-4 h-4 mr-3 inline" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
              </svg>
              API Documentation
            </a>
          </div>
        </div>
      </nav>
    `;

    // Apply initial styling
    this.updateNavStyles();
  }

  private initializeEventListeners(): void {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
      mobileMenuButton.addEventListener('click', () => {
        this.isMobileMenuOpen = !this.isMobileMenuOpen;
        
        if (this.isMobileMenuOpen) {
          mobileMenu.classList.remove('hidden');
        } else {
          mobileMenu.classList.add('hidden');
        }
      });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      if (!target.closest('nav') && this.isMobileMenuOpen && mobileMenu) {
        this.isMobileMenuOpen = false;
        mobileMenu.classList.add('hidden');
      }
    });

    // Close mobile menu when navigating
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      if (target.hasAttribute('data-route') && this.isMobileMenuOpen && mobileMenu) {
        this.isMobileMenuOpen = false;
        mobileMenu.classList.add('hidden');
      }
    });
  }

  private updateNavStyles(): void {
    // Set default nav link styles
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.classList.add('text-gray-600', 'hover:text-gray-900', 'hover:bg-gray-50');
    });

    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach(link => {
      link.classList.add('text-gray-600', 'hover:text-gray-900', 'hover:bg-gray-50');
    });
  }

  /**
   * Update active navigation item
   */
  public setActiveRoute(path: string): void {
    // Remove active styles from all nav links
    const allNavLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
    allNavLinks.forEach(link => {
      link.classList.remove('bg-blue-100', 'text-blue-700');
      link.classList.add('text-gray-600');
    });

    // Find and activate current links
    const activeDesktopLink = document.querySelector(`.nav-link[data-route="${path}"]`);
    const activeMobileLink = document.querySelector(`.mobile-nav-link[data-route="${path}"]`);
    
    if (activeDesktopLink) {
      activeDesktopLink.classList.add('bg-blue-100', 'text-blue-700');
      activeDesktopLink.classList.remove('text-gray-600');
    }
    
    if (activeMobileLink) {
      activeMobileLink.classList.add('bg-blue-100', 'text-blue-700');
      activeMobileLink.classList.remove('text-gray-600');
    }
  }
}
/**
 * Simple SPA Router for MarketData Frontend
 * Handles client-side routing without external dependencies
 */

export interface Route {
  path: string;
  title: string;
  component: () => Promise<any>;
  icon?: string;
  description?: string;
}

export class Router {
  private routes: Map<string, Route> = new Map();
  private currentRoute: string = '/';
  private container: HTMLElement | null = null;

  constructor(containerId: string) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      throw new Error(`Container element with ID '${containerId}' not found`);
    }

    // Listen for browser navigation
    window.addEventListener('popstate', () => {
      this.handleRoute(this.getHashPath());
    });

    // Listen for hash changes
    window.addEventListener('hashchange', () => {
      this.handleRoute(this.getHashPath());
    });

    // Listen for navigation clicks
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      const link = target.closest('[data-route]') as HTMLElement;
      
      if (link) {
        e.preventDefault();
        const route = link.getAttribute('data-route');
        if (route) {
          this.navigate(route);
        }
      }
    });
  }

  /**
   * Register a route
   */
  addRoute(route: Route): void {
    this.routes.set(route.path, route);
  }

  /**
   * Navigate to a route
   */
  navigate(path: string): void {
    // Update browser hash
    if (path !== this.currentRoute) {
      window.location.hash = '#' + path;
    } else {
      this.handleRoute(path);
    }
  }

  /**
   * Get path from hash, defaulting to root
   */
  private getHashPath(): string {
    const hash = window.location.hash;
    return hash ? hash.substring(1) : '/';
  }

  /**
   * Handle route change
   */
  private async handleRoute(path: string): Promise<void> {
    this.currentRoute = path;
    
    // Find matching route (support both exact match and parameterized routes)
    let matchedRoute: Route | undefined;
    let params: Record<string, string> = {};

    // First try exact match
    matchedRoute = this.routes.get(path);
    
    // If no exact match, try parameterized routes
    if (!matchedRoute) {
      for (const [routePath, route] of this.routes) {
        const match = this.matchRoute(routePath, path);
        if (match) {
          matchedRoute = route;
          params = match;
          break;
        }
      }
    }

    if (!matchedRoute) {
      // Fallback to home route
      matchedRoute = this.routes.get('/') || this.routes.get('/instruments');
    }

    if (matchedRoute && this.container) {
      try {
        // Update page title
        document.title = `${matchedRoute.title} - MarketData API`;
        
        // Update active navigation
        this.updateActiveNavigation(path);
        
        // Show loading state
        this.container.innerHTML = `
          <div class="flex items-center justify-center h-64">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <span class="ml-3 text-gray-600">Loading ${matchedRoute.title}...</span>
          </div>
        `;

        // Load and render component
        const component = await matchedRoute.component();
        const instance = new component.default(this.container, params);
        
        if (typeof instance.render === 'function') {
          await instance.render();
        }
      } catch (error) {
        console.error('Error loading route:', error);
        this.container.innerHTML = `
          <div class="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 class="text-red-800 text-lg font-semibold mb-2">Error Loading Page</h2>
            <p class="text-red-600">There was an error loading this page. Please try again.</p>
            <button 
              onclick="window.location.reload()" 
              class="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Reload Page
            </button>
          </div>
        `;
      }
    }
  }

  /**
   * Match parameterized routes like /instruments/:isin
   */
  private matchRoute(routePath: string, actualPath: string): Record<string, string> | null {
    const routeParts = routePath.split('/');
    const actualParts = actualPath.split('/');

    if (routeParts.length !== actualParts.length) {
      return null;
    }

    const params: Record<string, string> = {};

    for (let i = 0; i < routeParts.length; i++) {
      const routePart = routeParts[i];
      const actualPart = actualParts[i];

      if (routePart.startsWith(':')) {
        // Parameter
        const paramName = routePart.slice(1);
        params[paramName] = actualPart;
      } else if (routePart !== actualPart) {
        // Mismatch
        return null;
      }
    }

    return params;
  }

  /**
   * Update active navigation highlighting
   */
  private updateActiveNavigation(currentPath: string): void {
    // Remove active class from all nav links
    document.querySelectorAll('[data-route]').forEach(link => {
      link.classList.remove('active', 'bg-blue-100', 'text-blue-700');
      link.classList.add('text-gray-600');
    });

    // Find and activate current link
    const activeLink = document.querySelector(`[data-route="${currentPath}"]`) ||
                      document.querySelector(`[data-route^="${currentPath.split('/')[1] ? '/' + currentPath.split('/')[1] : currentPath}"]`);
    
    if (activeLink) {
      activeLink.classList.add('active', 'bg-blue-100', 'text-blue-700');
      activeLink.classList.remove('text-gray-600');
    }
  }

  /**
   * Initialize router with initial route
   */
  init(): void {
    const initialPath = this.getHashPath();
    this.handleRoute(initialPath);
  }

  /**
   * Get all registered routes for navigation
   */
  getRoutes(): Route[] {
    return Array.from(this.routes.values());
  }
}
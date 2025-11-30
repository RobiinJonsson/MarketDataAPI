/**
 * Authentication Service
 * Handles JWT token management and authentication flow for the frontend
 */

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: string;
  username: string;
  email: string;
  roles: string[];
  permissions: string[];
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export class AuthService {
  private static instance: AuthService;
  private baseURL: string = 'http://127.0.0.1:5000/api/v1';
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private user: User | null = null;
  private tokenExpiry: number | null = null;

  private constructor() {
    // Load tokens from localStorage on initialization
    this.loadTokensFromStorage();
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * Login with username and password
   */
  public async login(credentials: LoginCredentials): Promise<{ success: boolean; error?: string }> {
    try {
      const response = await fetch(`${this.baseURL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          error: errorData.message || `Login failed: ${response.status}`
        };
      }

      const authData: AuthResponse = await response.json();
      
      // Store tokens and user data
      this.accessToken = authData.access_token;
      this.refreshToken = authData.refresh_token;
      this.user = authData.user;
      this.tokenExpiry = Date.now() + (authData.expires_in * 1000);
      
      // Persist to localStorage
      this.saveTokensToStorage();
      
      console.log('Login successful:', authData.user.username);
      return { success: true };
      
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown login error'
      };
    }
  }

  /**
   * Logout - clear all tokens and user data
   */
  public logout(): void {
    this.accessToken = null;
    this.refreshToken = null;
    this.user = null;
    this.tokenExpiry = null;
    this.clearTokensFromStorage();
    console.log('User logged out');
  }

  /**
   * Get current access token (refreshes if needed)
   */
  public async getAccessToken(): Promise<string | null> {
    if (!this.accessToken) {
      return null;
    }

    // Check if token is expired (with 60 second buffer)
    if (this.tokenExpiry && Date.now() > (this.tokenExpiry - 60000)) {
      const refreshed = await this.refreshAccessToken();
      if (!refreshed) {
        return null;
      }
    }

    return this.accessToken;
  }

  /**
   * Check if user is authenticated
   */
  public isAuthenticated(): boolean {
    return this.accessToken !== null && this.user !== null;
  }

  /**
   * Get current user data
   */
  public getCurrentUser(): User | null {
    return this.user;
  }

  /**
   * Get authorization header for API requests
   */
  public async getAuthHeader(): Promise<Record<string, string>> {
    const token = await this.getAccessToken();
    if (token) {
      return { 'Authorization': `Bearer ${token}` };
    }
    return {};
  }

  /**
   * Refresh access token using refresh token
   */
  private async refreshAccessToken(): Promise<boolean> {
    if (!this.refreshToken) {
      console.warn('No refresh token available');
      this.logout();
      return false;
    }

    try {
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.refreshToken}`,
        },
      });

      if (!response.ok) {
        console.warn('Token refresh failed:', response.status);
        this.logout();
        return false;
      }

      const authData: AuthResponse = await response.json();
      
      this.accessToken = authData.access_token;
      this.refreshToken = authData.refresh_token;
      this.tokenExpiry = Date.now() + (authData.expires_in * 1000);
      
      this.saveTokensToStorage();
      console.log('Token refreshed successfully');
      return true;
      
    } catch (error) {
      console.error('Token refresh error:', error);
      this.logout();
      return false;
    }
  }

  /**
   * Save tokens to localStorage
   */
  private saveTokensToStorage(): void {
    if (this.accessToken && this.refreshToken && this.user) {
      const authData = {
        access_token: this.accessToken,
        refresh_token: this.refreshToken,
        user: this.user,
        token_expiry: this.tokenExpiry,
      };
      localStorage.setItem('marketdata_auth', JSON.stringify(authData));
    }
  }

  /**
   * Load tokens from localStorage
   */
  private loadTokensFromStorage(): void {
    try {
      const stored = localStorage.getItem('marketdata_auth');
      if (stored) {
        const authData = JSON.parse(stored);
        this.accessToken = authData.access_token;
        this.refreshToken = authData.refresh_token;
        this.user = authData.user;
        this.tokenExpiry = authData.token_expiry;
        
        // Check if token is still valid
        if (this.tokenExpiry && Date.now() > this.tokenExpiry) {
          console.log('Stored token expired, clearing');
          this.logout();
        } else {
          console.log('Loaded authentication from storage:', this.user?.username);
        }
      }
    } catch (error) {
      console.error('Error loading auth from storage:', error);
      this.clearTokensFromStorage();
    }
  }

  /**
   * Clear tokens from localStorage
   */
  private clearTokensFromStorage(): void {
    localStorage.removeItem('marketdata_auth');
  }
}

// Export singleton instance
export const authService = AuthService.getInstance();
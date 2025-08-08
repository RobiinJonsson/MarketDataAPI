// DOM utilities
export function $(selector: string): HTMLElement | null {
  return document.querySelector(selector);
}

export function $$(selector: string): NodeListOf<HTMLElement> {
  return document.querySelectorAll(selector);
}

export function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className?: string,
  textContent?: string
): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (textContent) element.textContent = textContent;
  return element;
}

// Format utilities
export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatNumber(num: number, decimals: number = 2): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num);
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

// Validation utilities
export function isValidISIN(isin: string): boolean {
  const isinRegex = /^[A-Z]{2}[A-Z0-9]{9}\d$/;
  return isinRegex.test(isin);
}

export function validateRequired(value: string, fieldName: string): string | null {
  if (!value.trim()) {
    return `${fieldName} is required`;
  }
  return null;
}

// Loading state utilities
export function showLoading(element: HTMLElement, text: string = 'Loading...'): void {
  element.innerHTML = `
    <div class="flex items-center justify-center p-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mr-3"></div>
      <span class="text-gray-600">${text}</span>
    </div>
  `;
}

export function showError(element: HTMLElement, message: string): void {
  element.innerHTML = `
    <div class="alert alert-error">
      <strong>Error:</strong> ${message}
    </div>
  `;
}

export function showSuccess(element: HTMLElement, message: string): void {
  element.innerHTML = `
    <div class="alert alert-success">
      <strong>Success:</strong> ${message}
    </div>
  `;
}

// Toast notifications
export function showToast(message: string, type: 'success' | 'error' | 'info' = 'info'): void {
  const toast = createElement('div', `fixed top-4 right-4 p-4 rounded-md shadow-lg z-50 alert alert-${type}`, message);
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.remove();
  }, 5000);
}

// Local storage utilities
export function setStorage(key: string, value: any): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error('Failed to save to localStorage:', error);
  }
}

export function getStorage<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Failed to read from localStorage:', error);
    return defaultValue;
  }
}

// Debounce utility
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(null, args), wait);
  };
}

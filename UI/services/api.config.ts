const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export const getApiUrl = () => API_BASE_URL;

export const getAuthToken = (): string | null => {
  return localStorage.getItem('access_token');
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

export const removeAuthToken = (): void => {
  localStorage.removeItem('access_token');
};

export const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const token = getAuthToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));

      // Map HTTP status codes to user-friendly messages
      let errorMessage = error.detail || 'An error occurred';

      switch (response.status) {
        case 429:
          errorMessage = error.detail || 'Rate limit exceeded. Please try again later.';
          break;
        case 503:
          errorMessage = error.detail || 'Service temporarily unavailable. Please try again in a moment.';
          break;
        case 500:
          errorMessage = error.detail || 'Server error. Please try again later.';
          break;
        case 401:
          errorMessage = error.detail || 'Invalid credentials';
          break;
        case 403:
          errorMessage = 'You do not have permission to access this resource';
          break;
        case 404:
          errorMessage = error.detail || 'Resource not found';
          break;
        case 400:
          errorMessage = error.detail || 'Invalid request';
          break;
      }

      throw new Error(errorMessage);
    }

    // Handle 204 No Content responses (e.g., DELETE requests)
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  } catch (error) {
    // Handle network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Unable to connect to server. Please check your internet connection.');
    }
    // Re-throw other errors
    throw error;
  }
};

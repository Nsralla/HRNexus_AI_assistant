import { apiRequest, setAuthToken, removeAuthToken, getApiUrl } from './api.config';

export interface UserResponse {
  id: string;
  email: string;
  full_name: string;
  company_id: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
}

export const authService = {
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await apiRequest<TokenResponse>('/api/auth/login/json', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    setAuthToken(response.access_token);
    return response;
  },

  async register(data: RegisterRequest): Promise<TokenResponse> {
    const response = await apiRequest<TokenResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    setAuthToken(response.access_token);
    return response;
  },

  async getCurrentUser(): Promise<UserResponse> {
    return apiRequest<UserResponse>('/api/auth/me', {
      method: 'GET',
    });
  },

  logout(): void {
    removeAuthToken();
  },
};

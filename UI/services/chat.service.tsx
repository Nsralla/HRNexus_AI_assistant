import { apiRequest } from './api.config';

export interface ChatResponse {
  id: string;
  user_id: string;
  company_id: string;
  title: string;
  created_at: string;
}

export interface MessageResponse {
  id: string;
  chat_id: string;
  user_id: string;
  content: string;
  role: 'user' | 'assistant';
  created_at: string;
}

export interface ChatCreate {
  title: string;
}

export interface MessageCreate {
  chat_id: string;
  content: string;
  role?: 'user' | 'assistant';
}

export interface ChatUpdate {
  title: string;
}

export const chatService = {
  async createChat(data: ChatCreate): Promise<ChatResponse> {
    return apiRequest<ChatResponse>('/api/chat/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getUserChats(): Promise<ChatResponse[]> {
    return apiRequest<ChatResponse[]>('/api/chat/', {
      method: 'GET',
    });
  },

  async updateChat(chatId: string, data: ChatUpdate): Promise<ChatResponse> {
    return apiRequest<ChatResponse>(`/api/chat/${chatId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  async deleteChat(chatId: string): Promise<void> {
    await apiRequest<void>(`/api/chat/${chatId}`, {
      method: 'DELETE',
    });
  },

  async sendMessage(data: MessageCreate): Promise<MessageResponse> {
    return apiRequest<MessageResponse>('/api/chat/message', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getChatMessages(chatId: string): Promise<MessageResponse[]> {
    return apiRequest<MessageResponse[]>(`/api/chat/${chatId}/messages`, {
      method: 'GET',
    });
  },
};

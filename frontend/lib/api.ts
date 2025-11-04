import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
  use_tools?: boolean;
}

export interface ChatResponse {
  response: string;
  success: boolean;
  metadata?: any;
  timestamp: string;
}

export interface GameSearchRequest {
  query: string;
  limit?: number;
}

export interface GameDetailsRequest {
  app_id: number;
}

export interface GameAnalysisRequest {
  app_id: number;
}

// Chat endpoint
export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/chat', request);
  return response.data;
};

// Search games
export const searchGames = async (request: GameSearchRequest): Promise<any[]> => {
  const response = await api.post('/games/search', request);
  return response.data;
};

// Get game details
export const getGameDetails = async (request: GameDetailsRequest): Promise<any> => {
  const response = await api.post('/games/details', request);
  return response.data;
};

// Analyze game
export const analyzeGame = async (request: GameAnalysisRequest): Promise<any> => {
  const response = await api.post('/games/analyze', request);
  return response.data;
};

// Health check
export const healthCheck = async (): Promise<any> => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

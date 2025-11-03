'use client';

import { useState, useRef, useEffect } from 'react';
import { sendMessage, ChatMessage } from '@/lib/api';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage({
        message: userMessage.content,
        conversation_history: messages,
        use_tools: true,
      });

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700 p-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-purple-600 p-2 rounded-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Videogames AI Assistant</h1>
            <p className="text-sm text-slate-400">Pregúntame sobre cualquier juego de Steam</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <Bot className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-2">
                ¡Hola! Soy tu asistente de videojuegos
              </h2>
              <p className="text-slate-400 mb-6">
                Puedo ayudarte a buscar juegos, obtener información detallada y analizar reviews
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto text-left">
                <button
                  onClick={() => setInput('¿Qué sabes sobre Elden Ring?')}
                  className="p-4 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg border border-slate-700 text-white transition-colors"
                >
                  <div className="font-semibold mb-1">Información de un juego</div>
                  <div className="text-sm text-slate-400">¿Qué sabes sobre Elden Ring?</div>
                </button>
                <button
                  onClick={() => setInput('Recomiéndame juegos de terror indie')}
                  className="p-4 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg border border-slate-700 text-white transition-colors"
                >
                  <div className="font-semibold mb-1">Recomendaciones</div>
                  <div className="text-sm text-slate-400">Recomiéndame juegos de terror indie</div>
                </button>
                <button
                  onClick={() => setInput('¿Vale la pena Baldur\'s Gate 3?')}
                  className="p-4 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg border border-slate-700 text-white transition-colors"
                >
                  <div className="font-semibold mb-1">Análisis y opiniones</div>
                  <div className="text-sm text-slate-400">¿Vale la pena Baldur's Gate 3?</div>
                </button>
                <button
                  onClick={() => setInput('Compara Cyberpunk 2077 con The Witcher 3')}
                  className="p-4 bg-slate-800/50 hover:bg-slate-700/50 rounded-lg border border-slate-700 text-white transition-colors"
                >
                  <div className="font-semibold mb-1">Comparaciones</div>
                  <div className="text-sm text-slate-400">Compara Cyberpunk 2077 con The Witcher 3</div>
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="bg-purple-600 p-2 rounded-lg h-fit">
                  <Bot className="w-5 h-5 text-white" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-purple-600 text-white'
                    : 'bg-slate-800 text-white border border-slate-700'
                }`}
              >
                {message.role === 'user' ? (
                  <div className="whitespace-pre-wrap">{message.content}</div>
                ) : (
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
              {message.role === 'user' && (
                <div className="bg-slate-700 p-2 rounded-lg h-fit">
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="bg-purple-600 p-2 rounded-lg h-fit">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-slate-800 text-white border border-slate-700 rounded-lg p-4">
                <Loader2 className="w-5 h-5 animate-spin" />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-slate-800/50 backdrop-blur-sm border-t border-slate-700 p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pregúntame sobre videojuegos..."
              className="flex-1 bg-slate-700 text-white placeholder-slate-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Enviar
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

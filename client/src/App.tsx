import React, { useState, useEffect, useRef } from "react";
import { Send, Bot, User } from "lucide-react";
import axios from "axios";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
  sources?: {
    [sheetName: string]: {
      [key: string]: string | number;
    }[];
  };
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const addMessage = (
    text: string,
    sender: "user" | "bot",
    sources?: {
      [sheetName: string]: {
        [key: string]: string | number;
      }[];
    }
  ) => {
    const newMessage: Message = {
      id: Date.now(),
      text,
      sender,
      timestamp: new Date(),
      sources,
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const handleSendMessage = async () => {
    if (inputText.trim()) {
      addMessage(inputText, "user");
      const question = inputText;
      setInputText("");
      setLoading(true);

      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/chat?query=${encodeURIComponent(question)}`,
          {},
          {
            headers: { Accept: "application/json" },
          }
        );

        const data = response.data;

        const sourcesBySheet: {
          [sheetName: string]: { [key: string]: string | number }[];
        } = {};

        data.source_contexts.forEach((ctx: any) => {
          const obj: { [key: string]: string | number } = {};
          ctx.column_names.forEach((key: string, index: number) => {
            obj[key] = ctx.values[index];
          });

          if (!sourcesBySheet[ctx.sheet_name]) {
            sourcesBySheet[ctx.sheet_name] = [];
          }
          sourcesBySheet[ctx.sheet_name].push(obj);
        });

        addMessage(data.answer, "bot", sourcesBySheet);
      } catch (error) {
        console.error("API error:", error);
        addMessage("Sorry! Server Error.", "bot");
      } finally {
        setLoading(false);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-blue-500 to-blue-500">
      <div
        className={`absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%239C92AC" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="4"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20`}
      ></div>

      <div className="relative flex flex-col w-full max-w-4xl mx-auto px-4 py-6 h-screen">
        <div className="text-center mb-8 animate-fadeIn">
          
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-3 tracking-tight">
            Zeemart AI
          </h1>
          <p className="text-white/80 text-lg max-w-2xl mx-auto leading-relaxed">
            Your intelligent assistant for seamless data insights
          </p>
        </div>

        <div className="flex-1 overflow-y-auto mb-6 space-y-6 pr-2 scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-white/60 animate-pulse">
                <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-medium">Start a conversation...</p>
                <p className="text-sm mt-2">Ask me anything about your data</p>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 animate-slideUp ${
                message.sender === "user" ? "flex-row-reverse" : "flex-row"
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div
                className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-md ring-2 ring-white transition-all duration-300 ${
                  message.sender === "user"
                    ? ""
                    : "bg-gradient-to-br from-green-400 via-emerald-500 to-teal-500"
                }`}
              >
                {message.sender === "user" ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-white" />
                )}
              </div>

              <div
                className={`max-w-xl lg:max-w-2xl ${
                  message.sender === "user" ? "text-right" : "text-left"
                }`}
              >
                <div
                  className={`px-6 py-4 rounded-2xl shadow-xl backdrop-blur-md border border-white/10 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 ${
                    message.sender === "user"
                      ? "bg-white/10 text-white"
                      : "bg-white/10 text-white"
                  }`}
                >
                  <p className="text-sm md:text-base font-medium leading-relaxed whitespace-pre-wrap">
                    {message.text}
                  </p>

                  {message.sender === "bot" &&
                    message.sources &&
                    Object.keys(message.sources).length > 0 && (
                      <div className="mt-6 space-y-6">
                        {Object.entries(message.sources).map(
                          ([sheetName, rows], i) => (
                            <div
                              key={i}
                              className="bg-white/5 rounded-xl p-4 backdrop-blur-sm border border-white/10"
                            >
                              <h4 className="text-sm font-bold mb-3 text-emerald-300 flex items-center gap-2">
                                <div className="w-2 h-2 bg-emerald-400 rounded-full"></div>
                                {sheetName} Data
                              </h4>
                              <div className="overflow-x-auto rounded-lg">
                                <table className="min-w-full text-xs border-collapse">
                                  <thead>
                                    <tr className="bg-white/10">
                                      {Object.keys(rows[0]).map((key) => (
                                        <th
                                          key={key}
                                          className="px-4 py-3 text-left font-semibold text-white/90 border-b border-white/20"
                                        >
                                          {key}
                                        </th>
                                      ))}
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {rows.map((row, idx) => (
                                      <tr
                                        key={idx}
                                        className="hover:bg-white/5 transition-colors duration-200 border-b border-white/10 last:border-b-0"
                                      >
                                        {Object.values(row).map((value, i) => (
                                          <td
                                            key={i}
                                            className="px-4 py-3 text-white/80"
                                          >
                                            {String(value)}
                                          </td>
                                        ))}
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    )}
                </div>

                <p
                  className={`text-xs mt-2 text-white/50 ${
                    message.sender === "user" ? "text-right" : "text-left"
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-start gap-3 animate-slideUp">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white/10 backdrop-blur-md text-white px-6 py-4 rounded-2xl shadow-xl border border-white/10">
                <div className="flex items-center gap-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-white rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-white rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium">thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

      
        <div className="relative">
          <div className="flex items-center gap-4 p-4 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-2xl">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your data..."
              className="flex-1 bg-transparent text-white placeholder-white/60 focus:outline-none text-sm md:text-base font-medium"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || loading}
              className="bg-gradient-to-r from-green-600 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-green-400 disabled:to-green-500 text-white rounded-xl p-3 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 disabled:hover:scale-100 disabled:opacity-50"
            >
              <Send size={18} className={loading ? "animate-pulse" : ""} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

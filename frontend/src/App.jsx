import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Image as ImageIcon, ShieldAlert, ShieldCheck, Loader2 } from 'lucide-react';

const API_URL = import.meta.env.PROD ? '' : 'http://localhost:8000/api/v1';

function App() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            role: 'bot',
            content: "Hello! I am Guardian AI. Upload a screenshot or paste a text message, and I'll analyze if it's a potential scam.",
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = { id: Date.now(), role: 'user', content: input, type: 'text', timestamp: new Date() };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post(`${API_URL}/analyze/text`, { text: input });
            addBotResponse(response.data);
        } catch (error) {
            addErrorResponse();
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Show image preview immediately
        const imageUrl = URL.createObjectURL(file);
        const userMsg = {
            id: Date.now(),
            role: 'user',
            content: "Analyze this image",
            type: 'image',
            imageUrl: imageUrl,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMsg]);
        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_URL}/analyze/image`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            addBotResponse(response.data);
        } catch (error) {
            addErrorResponse();
        } finally {
            setIsLoading(false);
        }
    };

    const addBotResponse = (data) => {
        const isSafe = !data.is_fraud;
        const botMsg = {
            id: Date.now() + 1,
            role: 'bot',
            content: data.analysis,
            type: 'analysis',
            result: data, // Stores risk_score, detected_types
            timestamp: new Date()
        };
        setMessages(prev => [...prev, botMsg]);
    };

    const addErrorResponse = () => {
        setMessages(prev => [...prev, {
            id: Date.now() + 1,
            role: 'bot',
            content: "Sorry, I encountered an error analyzing that. Please try again.",
            type: 'text',
            timestamp: new Date()
        }]);
    };

    return (
        <div className="flex flex-col h-screen bg-slate-950 text-white">
            {/* Header */}
            <header className="p-4 border-b border-slate-800 bg-slate-900/50 backdrop-blur flex items-center gap-3 shadow-lg z-10">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-500 to-cyan-400 flex items-center justify-center shadow-blue-500/20 shadow-lg">
                    <ShieldCheck className="text-white" size={24} />
                </div>
                <div>
                    <h1 className="font-bold text-xl tracking-tight">Guardian AI</h1>
                    <p className="text-xs text-slate-400 font-medium">Fraud & Scam Detection System</p>
                </div>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] sm:max-w-[70%] rounded-2xl p-4 shadow-sm ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-none'
                                : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-none'
                            }`}>

                            {/* User Image Preview */}
                            {msg.type === 'image' && (
                                <div className="mb-3 rounded-lg overflow-hidden border border-white/20">
                                    <img src={msg.imageUrl} alt="Uploaded" className="max-w-full h-auto" />
                                </div>
                            )}

                            {/* Text Content */}
                            <div className="leading-relaxed whitespace-pre-wrap">{msg.content}</div>

                            {/* Analysis Result Card */}
                            {msg.type === 'analysis' && msg.result && (
                                <div className={`mt-4 p-3 rounded-xl border ${msg.result.is_fraud ? 'bg-red-500/10 border-red-500/30' : 'bg-green-500/10 border-green-500/30'}`}>
                                    <div className="flex items-center gap-2 mb-2">
                                        {msg.result.is_fraud ? <ShieldAlert className="text-red-400" size={20} /> : <ShieldCheck className="text-green-400" size={20} />}
                                        <span className={`font-bold ${msg.result.is_fraud ? 'text-red-400' : 'text-green-400'}`}>
                                            {msg.result.is_fraud ? 'POTENTIAL SCAM' : 'LIKELY SAFE'}
                                        </span>
                                    </div>
                                    <div className="text-sm opacity-90 space-y-1">
                                        <div className="flex justify-between">
                                            <span>Risk Score:</span>
                                            <span className="font-mono font-bold">{msg.result.risk_score}/100</span>
                                        </div>
                                        {msg.result.detected_types.length > 0 && (
                                            <div className="flex gap-1 flex-wrap mt-2">
                                                {msg.result.detected_types.map(tag => (
                                                    <span key={tag} className="px-2 py-0.5 rounded-full bg-slate-900/50 text-xs border border-white/10">{tag}</span>
                                                ))}
                                            </div>
                                        )}
                                        {msg.result.extracted_text && (
                                            <details className="mt-2 text-xs cursor-pointer">
                                                <summary className="opacity-70 hover:opacity-100 transition-opacity">Show Extracted Text</summary>
                                                <p className="mt-1 p-2 bg-slate-900/50 rounded italic text-slate-400 border border-white/5">
                                                    "{msg.result.extracted_text.substring(0, 100)}..."
                                                </p>
                                            </details>
                                        )}
                                    </div>
                                </div>
                            )}

                            <div className="text-[10px] mt-2 opacity-50 flex justify-end">
                                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-slate-800 rounded-2xl rounded-bl-none p-4 flex items-center gap-3">
                            <Loader2 className="animate-spin text-blue-400" size={20} />
                            <span className="text-sm text-slate-400 animate-pulse">Analyzing content...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </main>

            {/* Input Area */}
            <footer className="p-4 bg-slate-900 border-t border-slate-800">
                <div className="max-w-4xl mx-auto flex gap-3">
                    <input
                        type="file"
                        accept="image/*"
                        className="hidden"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                    />
                    <button
                        onClick={() => fileInputRef.current?.click()}
                        className="p-3 rounded-xl bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white transition-colors border border-slate-700"
                        title="Upload Image"
                    >
                        <ImageIcon size={20} />
                    </button>
                    <div className="flex-1 relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Paste a message or URL to check..."
                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/50 placeholder:text-slate-600 transition-all text-sm"
                        />
                    </div>
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() && !isLoading}
                        className="p-3 rounded-xl bg-blue-600 text-white hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/20"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </footer>
        </div>
    );
}

export default App;

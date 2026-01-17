import React, { useState, useRef, useEffect } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import axios from 'axios';
import { Shield, AlertTriangle, CheckCircle, Upload, Send, FileText, Image as ImageIcon, ExternalLink, RefreshCw } from 'lucide-react';

const GlobalStyle = createGlobalStyle`
  body {
    background-color: #f0f2f5;
    color: #1f2937;
    margin: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
`;

const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const Header = styled.header`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0;
`;

const Subtitle = styled.span`
  color: #6b7280;
  font-size: 14px;
  margin-left: auto;
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  flex: 1;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
`;

const Section = styled.section`
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 650px;
`;

const SectionHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #f3f4f6;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;

// Chat Styles
const ChatArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const MessageBubble = styled.div`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  background-color: ${props => props.isUser ? '#2563eb' : '#f3f4f6'};
  color: ${props => props.isUser ? 'white' : '#1f2937'};
  border-bottom-right-radius: ${props => props.isUser ? '4px' : '12px'};
  border-bottom-left-radius: ${props => props.isUser ? '12px' : '4px'};
`;

const InputArea = styled.div`
  padding: 20px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  gap: 12px;
  align-items: center;
`;

const TextInput = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
  transition: border-color 0.2s;

  &:focus {
    border-color: #2563eb;
  }
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  
  background-color: ${props => props.primary ? '#2563eb' : '#f3f4f6'};
  color: ${props => props.primary ? 'white' : '#4b5563'};

  &:hover {
    background-color: ${props => props.primary ? '#1d4ed8' : '#e5e7eb'};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Result Dashboard Styles
const Dashboard = styled.div`
  padding: 24px;
  overflow-y: auto;
`;

const StatusCard = styled.div`
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  text-align: center;
  
  background-color: ${props => props.risk === 'high' ? '#fee2e2' : props.risk === 'medium' ? '#fef3c7' : '#dcfce7'};
  border: 1px solid ${props => props.risk === 'high' ? '#fecaca' : props.risk === 'medium' ? '#fde68a' : '#bbf7d0'};
  color: ${props => props.risk === 'high' ? '#991b1b' : props.risk === 'medium' ? '#92400e' : '#166534'};
`;

const StatusIcon = styled.div`
  font-size: 48px;
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
`;

const StatusTitle = styled.h2`
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
`;

const ConfidenceBar = styled.div`
  background: rgba(0,0,0,0.1);
  height: 8px;
  border-radius: 4px;
  margin: 16px auto 8px;
  max-width: 200px;
  overflow: hidden;
`;

const ConfidenceFill = styled.div`
  height: 100%;
  width: ${props => props.percent}%;
  background-color: currentColor;
  transition: width 0.5s ease-out;
`;

const DetailList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const DetailItem = styled.div`
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
`;

const DetailLabel = styled.div`
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
  margin-bottom: 4px;
  font-weight: 600;
`;

const DetailValue = styled.div`
  color: #111827;
  font-size: 14px;
  font-weight: 500;
`;

const ImagePreview = styled.img`
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #e5e7eb;
`;

function App() {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm GuardianAI. Upload a screenshot or paste a message to verify its authenticity.", isUser: false }
  ]);
  const [inputText, setInputText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [evalStats, setEvalStats] = useState(null);
  const [showEval, setShowEval] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const addMessage = (text, isUser) => {
    setMessages(prev => [...prev, { text, isUser }]);
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const text = inputText;
    setInputText('');
    addMessage(text, true);
    setLoading(true);

    try {
      const isUrl = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/.test(text);
      if (isUrl) {
        // Handle Link
        const formData = new FormData();
        formData.append('url', text);
        const res = await axios.post('http://localhost:8000/analyze/link', formData);
        setAnalysis({ ...res.data, type: 'link' });
      } else {
        // Handle Text
        const res = await axios.post('http://localhost:8000/analyze/text', { text });
        setAnalysis({ ...res.data, type: 'text' });
      }
    } catch (err) {
      console.error(err);
      addMessage("Error analyzing content. Please try again.", false);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    addMessage(`Uploaded file: ${file.name}`, true);
    setLoading(true);
    setAnalysis(null); // Reset previous analysis

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Use verify/image endpoint which now supports OCR
      const res = await axios.post('http://localhost:8000/verify/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const result = res.data;

      // Determine fraud status
      const isFraud = !result.is_authentic;

      setAnalysis({
        type: 'image',
        is_fraud: isFraud,
        confidence: result.confidence,
        fraud_type: isFraud ? "Potential Fraud / Scam" : "Authentic Document",
        details: {
          issues: result.issues_found,
          recommendations: result.recommendations,
          extracted_text: result.extracted_text // Added for visibility
        },
        preview: URL.createObjectURL(file)
      });

    } catch (err) {
      console.error(err);
      addMessage("Error analyzing image. Please try again.", false);
    } finally {
      setLoading(false);
      // Reset input
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleRunEval = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/evaluate');
      setEvalStats(res.data);
      setShowEval(true);
    } catch (err) {
      console.error(err);
      addMessage("Error running evaluation.", false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Header>
          <Shield color="#2563eb" size={32} />
          <Title>GuardianAI</Title>
          <Subtitle>Fraud Prevention System</Subtitle>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '10px' }}>
            <ActionButton onClick={handleRunEval} title="Run System Evaluation">
              <RefreshCw size={20} className={loading ? 'spin' : ''} />
            </ActionButton>
          </div>
        </Header>

        {showEval && evalStats && (
          <div style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
          }}>
            <div style={{
              background: 'white', padding: '30px', borderRadius: '16px',
              width: '80%', maxWidth: '800px', maxHeight: '80vh', overflowY: 'auto',
              position: 'relative'
            }}>
              <button
                onClick={() => setShowEval(false)}
                style={{ position: 'absolute', top: '20px', right: '20px', border: 'none', background: 'none', cursor: 'pointer', fontSize: '24px' }}
              >
                &times;
              </button>

              <h2>Model Evaluation Report</h2>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginBottom: '30px' }}>
                <StatusCard risk="low">
                  <StatusTitle>{evalStats.accuracy}%</StatusTitle>
                  <div>Accuracy</div>
                </StatusCard>
                <StatusCard risk={evalStats.avg_latency_ms < 50 ? 'low' : 'medium'}>
                  <StatusTitle>{evalStats.avg_latency_ms}ms</StatusTitle>
                  <div>Avg Latency</div>
                </StatusCard>
                <StatusCard risk="low">
                  <StatusTitle>{evalStats.total_samples}</StatusTitle>
                  <div>Test Samples</div>
                </StatusCard>
              </div>

              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ textAlign: 'left', borderBottom: '2px solid #e5e7eb' }}>
                    <th style={{ padding: '12px' }}>Text</th>
                    <th style={{ padding: '12px' }}>Predicted</th>
                    <th style={{ padding: '12px' }}>Actual</th>
                    <th style={{ padding: '12px' }}>Result</th>
                  </tr>
                </thead>
                <tbody>
                  {evalStats.details.map((item, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid #f3f4f6' }}>
                      <td style={{ padding: '12px', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {item.text}
                      </td>
                      <td style={{ padding: '12px' }}>{item.predicted}</td>
                      <td style={{ padding: '12px' }}>{item.actual}</td>
                      <td style={{ padding: '12px' }}>
                        {item.result === 'PASS'
                          ? <span style={{ color: 'green', fontWeight: 'bold' }}>✓ PASS</span>
                          : <span style={{ color: 'red', fontWeight: 'bold' }}>✗ FAIL</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <MainContent>
          <Section>
            <SectionHeader>
              <FileText size={18} />
              Chat Analysis
            </SectionHeader>
            <ChatArea>
              {messages.map((msg, idx) => (
                <MessageBubble key={idx} isUser={msg.isUser}>
                  {msg.text}
                </MessageBubble>
              ))}
              {loading && <MessageBubble>Analyzing...</MessageBubble>}
              <div ref={chatEndRef} />
            </ChatArea>
            <InputArea>
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept="image/*"
                onChange={handleFileUpload}
              />
              <ActionButton onClick={() => fileInputRef.current.click()} title="Upload Image">
                <ImageIcon size={20} />
              </ActionButton>
              <TextInput
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type a message or paste a link..."
                disabled={loading}
              />
              <ActionButton primary onClick={handleSend} disabled={loading || !inputText.trim()}>
                <Send size={20} />
              </ActionButton>
            </InputArea>
          </Section>

          <Section>
            <SectionHeader>
              <AlertTriangle size={18} />
              Analysis Dashboard
            </SectionHeader>
            {analysis ? (
              <Dashboard>
                {analysis.type === 'image' && analysis.preview && (
                  <ImagePreview src={analysis.preview} />
                )}

                <StatusCard risk={analysis.is_fraud ? 'high' : 'low'}>
                  <StatusIcon>
                    {analysis.is_fraud ? <AlertTriangle size={48} /> : <CheckCircle size={48} />}
                  </StatusIcon>
                  <StatusTitle>{analysis.fraud_type || (analysis.is_fraud ? 'Fraud Detected' : 'No Threats Found')}</StatusTitle>
                  <div>Confidence Score: {(analysis.confidence * 100).toFixed(1)}%</div>
                  <ConfidenceBar>
                    <ConfidenceFill percent={analysis.confidence * 100} />
                  </ConfidenceBar>
                </StatusCard>

                <DetailList>
                  {analysis.details?.extracted_text && (
                    <DetailItem>
                      <DetailLabel>OCR Extracted Text</DetailLabel>
                      <DetailValue style={{ fontSize: '12px', color: '#4b5563', maxHeight: '100px', overflowY: 'auto' }}>
                        {analysis.details.extracted_text}
                      </DetailValue>
                    </DetailItem>
                  )}

                  {analysis.details?.issues?.length > 0 && (
                    <DetailItem>
                      <DetailLabel>Risk Factors</DetailLabel>
                      <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px', color: '#b91c1c' }}>
                        {analysis.details.issues.map((issue, i) => (
                          <li key={i}>{issue}</li>
                        ))}
                      </ul>
                    </DetailItem>
                  )}

                  {analysis.details?.recommendations?.length > 0 && (
                    <DetailItem>
                      <DetailLabel>Recommendations</DetailLabel>
                      <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px' }}>
                        {analysis.details.recommendations.map((rec, i) => (
                          <li key={i}>{rec}</li>
                        ))}
                      </ul>
                    </DetailItem>
                  )}
                </DetailList>
              </Dashboard>
            ) : (
              <div style={{ padding: '40px', textAlign: 'center', color: '#9ca3af' }}>
                <Shield size={64} style={{ marginBottom: '16px', opacity: 0.5 }} />
                <p>Upload an image or send a message to see detailed analysis here.</p>
              </div>
            )}
          </Section>
        </MainContent>
      </AppContainer>
    </>
  );
}

export default App;


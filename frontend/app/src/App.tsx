import { JSX, useState, useEffect } from "react";
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// Template configuration - automatically discovers backend port
const getApiBaseUrl = (): string => {
  const currentPort = window.location.port;
  const currentHost = window.location.hostname;
  
  // Dynamic port discovery based on template's port assignment pattern
  // Frontend typically gets first available port, backend gets next port
  const frontendPort = parseInt(currentPort) || 3000;
  const backendPort = frontendPort + 1;
  
  return `http://${currentHost}:${backendPort}`;
};

interface CounterData {
  count: number;
  message: string;
  timestamp: string;
}

function App(): JSX.Element {
  const [count, setCount] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('never');
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');

  const apiBaseUrl = getApiBaseUrl();

  // Check API connection on component mount
  useEffect(() => {
    checkApiConnection();
    loadCounter();
  }, []);

  const checkApiConnection = async (): Promise<void> => {
    try {
      const response = await fetch(`${apiBaseUrl}/`);
      if (response.ok) {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      console.warn('API connection check failed:', error);
      setApiStatus('error');
    }
  };

  const loadCounter = async (): Promise<void> => {
    if (apiStatus === 'error') return;
    
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(`${apiBaseUrl}/api/counter`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data: CounterData = await response.json();
      setCount(data.count);
      setLastUpdated(data.timestamp);
      
    } catch (error) {
      console.error('Failed to load counter:', error);
      setError(error instanceof Error ? error.message : 'Failed to load counter');
    } finally {
      setIsLoading(false);
    }
  };

  const incrementCounter = async (): Promise<void> => {
    if (apiStatus === 'error') {
      // Fallback to local state if API is not available
      setCount(prev => prev + 1);
      setLastUpdated(new Date().toISOString());
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(`${apiBaseUrl}/api/counter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ increment: 1 }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data: CounterData = await response.json();
      setCount(data.count);
      setLastUpdated(data.timestamp);
      
    } catch (error) {
      console.error('Failed to increment counter:', error);
      setError(error instanceof Error ? error.message : 'Failed to increment counter');
      // Fallback to local increment
      setCount(prev => prev + 1);
    } finally {
      setIsLoading(false);
    }
  };

  const resetCounter = async (): Promise<void> => {
    if (apiStatus === 'error') {
      // Fallback to local state if API is not available
      setCount(0);
      setLastUpdated(new Date().toISOString());
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(`${apiBaseUrl}/api/counter`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data: CounterData = await response.json();
      setCount(data.count);
      setLastUpdated(data.timestamp);
      
    } catch (error) {
      console.error('Failed to reset counter:', error);
      setError(error instanceof Error ? error.message : 'Failed to reset counter');
      // Fallback to local reset
      setCount(0);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string): string => {
    if (timestamp === 'never' || timestamp === 'initialized') return timestamp;
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return timestamp;
    }
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      
      <h1>DevContainer Serverless Template</h1>
      
      <div className="api-status">
        <p className={`status-indicator ${apiStatus}`}>
          API Status: {apiStatus === 'checking' ? 'Checking...' : 
                      apiStatus === 'connected' ? `Connected (${apiBaseUrl})` : 
                      'Offline - Using local state'}
        </p>
      </div>

      <div className="card">
        <div className="counter-section">
          <button 
            onClick={incrementCounter} 
            disabled={isLoading}
            className="counter-button"
          >
            {isLoading ? 'Loading...' : `count is ${count}`}
          </button>
          
          <button 
            onClick={resetCounter} 
            disabled={isLoading}
            className="reset-button"
          >
            Reset Counter
          </button>
        </div>

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
            <p>Using local state as fallback</p>
          </div>
        )}

        <div className="counter-info">
          <p>Last updated: {formatTimestamp(lastUpdated)}</p>
          <p className="integration-note">
            This counter is {apiStatus === 'connected' ? 'persisted in DynamoDB' : 'stored locally'}
          </p>
        </div>

        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      
      <p className="read-the-docs">
        This template demonstrates full-stack integration: React + FastAPI + DynamoDB.
        <br />
        The counter persists across sessions when the backend is running.
        <br />
        Click on the Vite and React logos to learn more.
      </p>
    </>
  );
}

export default App;
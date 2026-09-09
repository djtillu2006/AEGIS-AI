import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import App from './App.jsx'
import 'antd/dist/reset.css'
import './styles/index.css'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
const HAS_VALID_PUBLISHABLE_KEY = Boolean(
  PUBLISHABLE_KEY &&
  /^pk_(test|live)_[A-Za-z0-9_-]+$/.test(PUBLISHABLE_KEY) &&
  !/^pk_(test|live)_x+$/.test(PUBLISHABLE_KEY),
)

console.log("🚀 Main.jsx is executing!");

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ error, errorInfo });
    console.error("Uncaught error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 20, color: 'red' }}>
          <h1>Something went wrong.</h1>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

function ClerkConfigurationNotice() {
  return (
    <main style={{ padding: 32, maxWidth: 720, margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      <h1>Clerk configuration required</h1>
      <p>
        Add a real Clerk publishable key to <code>frontend/.env</code> and restart the Vite server.
      </p>
      <p>
        Set <code>VITE_CLERK_PUBLISHABLE_KEY</code> to a key beginning with <code>pk_test_</code> or{' '}
        <code>pk_live_</code>. The placeholder key is not accepted.
      </p>
    </main>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      {HAS_VALID_PUBLISHABLE_KEY ? (
        <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
          <App />
        </ClerkProvider>
      ) : (
        <ClerkConfigurationNotice />
      )}
    </ErrorBoundary>
  </React.StrictMode>,
)

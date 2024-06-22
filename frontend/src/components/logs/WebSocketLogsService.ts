import { SetStateAction } from 'react';

let logs = '';
let subscribers: any[] = [];
let ws: WebSocket;

function connect() {
  ws = new WebSocket('ws://127.0.0.1:8000/ws');

  ws.onopen = () => {
    console.log('WebSocket connection established');
    // Reset reconnection attempts count on successful connection
    reconnectAttempts = 0;
  };

  ws.onmessage = (event) => {
    logs += event.data;

    const textarea = document.getElementById('textarea_logs');
    if (!textarea) {
      return;
    }

    const shouldScroll =
      Math.abs(textarea.scrollHeight - textarea.offsetHeight - textarea.scrollTop) <= 80;
    if (shouldScroll) {
      setTimeout(() => {
        textarea.scrollTop = textarea.scrollHeight;
      }, 1);
    }
    subscribers.forEach((callback) => callback(logs));
  };

  ws.onclose = () => {
    console.log('WebSocket connection closed. Attempting to reconnect...');
    attemptReconnect();
  };

  ws.onerror = (error) => {
    console.error('WebSocket encountered an error:', error);
    ws.close(); // Ensure the connection is closed on error.
  };
}

// Attempt to reconnect with an exponential backoff
let reconnectAttempts = 0;

function attemptReconnect() {
  // Calculate backoff delay with a maximum delay of 10 seconds
  const delay = Math.min(1000 * 2 ** reconnectAttempts, 10000);
  setTimeout(() => {
    console.log(`Attempting to reconnect... Attempt ${reconnectAttempts + 1}`);
    reconnectAttempts++;
    connect(); // Attempt to reconnect
  }, delay);
}

// Initial connection attempt
connect();

export function subscribeToLogs(callback: {
  (value: SetStateAction<string>): void;
  (arg0: string): void;
}) {
  subscribers.push(callback);

  callback(logs);

  return () => {
    subscribers = subscribers.filter((sub) => sub !== callback);
  };
}

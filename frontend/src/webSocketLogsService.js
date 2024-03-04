let logs = '';
let subscribers = [];

const ws = new WebSocket('ws://127.0.0.1:8000/ws');

ws.onmessage = (event) => {
    logs += event.data;

    const textarea = document.getElementById('textarea_logs');

    if (!textarea) {return}
    let shouldScroll = Math.abs((textarea.scrollHeight - textarea.offsetHeight) - textarea.scrollTop) <= 80;
    if (shouldScroll) {
        setTimeout(() => {
            textarea.scrollTop = textarea.scrollHeight;
        }, 1)
    }

    subscribers.forEach((callback) => callback(logs));
};

export function subscribeToLogs(callback) {
    subscribers.push(callback);

    callback(logs);

    return () => {
        subscribers = subscribers.filter((sub) => sub !== callback);
    };
}
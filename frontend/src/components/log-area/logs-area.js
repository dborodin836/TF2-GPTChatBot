import React, {useState, useEffect} from 'react';
import {Textarea} from "@material-tailwind/react";

export function LogsArea() {

    const [logs, setLogs] = useState('');

    useEffect(() => {
        const ws = new WebSocket('ws://127.0.0.1:8000/ws');

        // When message is received, append it to the logs state
        ws.onmessage = (event) => {
            setLogs((currentLogs) => `${currentLogs}${event.data}`);
            const textarea = document.getElementById('textarea_logs');
            let shouldScroll = Math.abs((textarea.scrollHeight - textarea.offsetHeight) - textarea.scrollTop) <= 80;

            if (shouldScroll) {
                textarea.scrollTop = textarea.scrollHeight;
            }

        };

        // Clean up function to close WebSocket connection when the component unmounts
        return () => {
            ws.close();
        };
    }, []);

    return (
        <div className="flex flex-1 w-full flex-col gap-6 p-4">
            <Textarea
                className="min-w-[95%] min-h-[80vh] selection:bg-gray-400 selection:text-white"
                size="lg"
                label="App logs"
                value={logs}
                id="textarea_logs"
                readOnly
            />
        </div>
    );
}

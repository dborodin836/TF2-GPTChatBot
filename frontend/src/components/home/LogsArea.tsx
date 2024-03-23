import React, {useState, useEffect} from 'react';
import {Textarea} from "@material-tailwind/react";
import {subscribeToLogs} from "./WebSocketLogsService";

export function LogsArea() {
    const [logs, setLogs] = useState('');

    useEffect(() => {
        const unsubscribe = subscribeToLogs(setLogs);

        // Scroll to the end on mount
        setTimeout(() => {
            const textarea = document.getElementById('textarea_logs');
            if (textarea !== null){
                textarea.scrollTop = textarea.scrollHeight;
            }
        }, 5)

        return unsubscribe;
    }, []);

    return (
        <div className="flex flex-1 w-full gap-6 p-4">
            <Textarea
                className="min-w-[95%] selection:bg-gray-400 selection:text-white !border !border-gray-300"
                size="lg"
                label="App logs"
                value={logs}
                id="textarea_logs"
                readOnly
                labelProps={{
                    className: "hidden",
                }}
                style={{ fontFamily: 'monospace' }}
            />
        </div>
    );
}

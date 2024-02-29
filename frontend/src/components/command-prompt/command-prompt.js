import React, {useState} from "react";
import {Input, Button} from "@material-tailwind/react";


export function CommandPrompt() {
    const [command, setCommand] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        fetch('http://localhost:8000/cmd', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: command}),
        })
            .then(response => {
                if (!response.ok) {
                    console.error(`Error: ${response.status}`);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
            setCommand(''); // Reset command string here
        });
    };

    return (
        <div className="flex flex-1 w-full flex-row gap-6 p-4">
            <Input
                label="Type your commands here... Or start with 'help' command"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                className="pr-20"
                containerProps={{
                    className: "min-w-0",
                }}
            />
            <Button
                size="sm"
                color={command ? "gray" : "blue-gray"}
                disabled={!command}
                className="right-1 rounded"
                onClick={handleSubmit}
            >
                Send
            </Button>
        </div>
    );
}

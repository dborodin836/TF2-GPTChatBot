import React from "react";
import {Input, Button} from "@material-tailwind/react";

export function CommandPrompt() {
    const [email, setEmail] = React.useState("");
    const onChange = ({target}) => setEmail(target.value);

    return (
        <div className="flex flex-1 w-full flex-row gap-6 p-4">
            <Input
                label="Type your commands here... Or start with 'help' command"
                value={email}
                onChange={onChange}
                className="pr-20"
                containerProps={{
                    className: "min-w-0",
                }}
            />
            <Button
                size="sm"
                color={email ? "gray" : "blue-gray"}
                disabled={!email}
                className="right-1 rounded"
            >
                Send
            </Button>
        </div>
    );
}

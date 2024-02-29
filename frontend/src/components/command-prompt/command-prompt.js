import React from "react";
import {Input, Button} from "@material-tailwind/react";

export function CommandPrompt() {
    const [cnd, setCMD] = React.useState("");
    const onChange = ({target}) => setCMD(target.value);

    return (
        <div className="flex flex-1 w-full flex-row gap-6 p-4">
            <Input
                label="Type your commands here... Or start with 'help' command"
                value={cmd}
                onChange={onChange}
                className="pr-20"
                containerProps={{
                    className: "min-w-0",
                }}
            />
            <Button
                size="sm"
                color={cmd ? "gray" : "blue-gray"}
                disabled={!cmd}
                className="right-1 rounded"
            >
                Send
            </Button>
        </div>
    );
}

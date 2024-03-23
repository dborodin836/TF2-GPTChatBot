import {LogsArea} from "./LogsArea";
import {CommandPrompt} from "./CommandPrompt";
import React from "react";

export function Home() {
    return (
        <div className="h-[calc(100vh-2rem)] flex flex-col p-4 overflow-hidden">
            <LogsArea/>
            <CommandPrompt/>
        </div>
    );
}
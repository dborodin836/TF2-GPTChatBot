import {LogsArea} from "../log-area/logs-area";
import {CommandPrompt} from "../command-prompt/command-prompt";

export function PageHome() {
    return (
        <div className="h-[calc(100vh-2rem)] flex flex-col p-4 overflow-hidden">
            <LogsArea/>
            <CommandPrompt/>
        </div>
    );
}
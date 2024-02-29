import {LogsArea} from "../log-area/logs-area";
import {CommandPrompt} from "../command-prompt/command-prompt";

export function PageHome() {
    return (
        <div className="flex-1 overflow-hidden">
            <div>
                <LogsArea/>
            </div>
            <div>
                <CommandPrompt/>
            </div>
            {/*<div className="p-4 left-4">*/}
            {/*    <StickyLogsToggle/>*/}
            {/*</div>*/}
        </div>
    );
}
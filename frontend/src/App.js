import './App.css';
import {DefaultSidebar} from "./components/sidebar/sidebar";
import {LogsArea} from "./components/log-area/logs-area";
import {CommandPrompt} from "./components/command-prompt/command-prompt";
import {StickyLogsToggle} from "./components/sticky-logs-toggle/sticky-logs-toggle";

function App() {
    return (
        <div className="flex w-full h-screen">
            <div className="flex-none">
                <DefaultSidebar/>
            </div>
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
        </div>
    )
}

export default App;

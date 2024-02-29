import './App.css';
import {DefaultSidebar} from "./components/sidebar/sidebar";
import {Route, Routes} from 'react-router-dom';
import {PageHome} from "./components/page-home/page-home";
import {PageSettings} from "./components/page-settings/page-settings";
import {PageAbout} from "./components/page-about/page-about";

function App() {
    return (
        <div className="flex w-full h-screen">
            <div className="flex-none">
                <DefaultSidebar/>
            </div>
            <Routes>
                <Route path="/" element={<PageHome/>}/>
                <Route path="/settings" element={<PageSettings/>}/>
                <Route path="/about" element={<PageAbout/>}/>
            </Routes>
        </div>
    )
}

export default App;

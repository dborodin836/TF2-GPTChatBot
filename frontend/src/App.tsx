import './App.css';
import {DefaultSidebar} from "./components/sidebar";
import {Route, Routes} from 'react-router-dom';
import {Home} from "./components/home/Home";
import {PageSettings} from "./components/settings/PageSettings";
import {About} from "./components/about/About";
import React from 'react';

function App() {
    return (
        <div className="flex w-full h-screen">
            <div className="flex-none">
                <DefaultSidebar/>
            </div>
            <div className="flex-1 shadow-md rounded-xl ml-7 m-4 mt-0">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/settings" element={<PageSettings/>}/>
                    <Route path="/about" element={<About/>}/>
                </Routes>
            </div>
        </div>
    )
}

export default App;

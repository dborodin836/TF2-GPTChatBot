import './App.css';
import { DefaultSidebar } from './components/Sidebar';
import { Route, Routes } from 'react-router-dom';
import { LogsPage } from './components/logs/LogsPage';
import { PageSettings } from './components/settings/PageSettings';
import { About } from './components/about/About';
import React from 'react';
import { CommandAdd } from './components/commands/CommandAdd';
import { CommandList } from './components/commands/CommandList';
import { CommandEdit } from './components/commands/CommandEdit';
import { Dashboard } from './components/dashboard/dashboardPage';
import { Chats } from './components/chats/ChatsPage';

function App() {
  return (
    <div className="flex w-full h-screen">
      <div className="flex-none">
        <DefaultSidebar />
      </div>
      <div className="flex-1 shadow-md rounded-xl ml-7 m-4 mt-0">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/logs" element={<LogsPage />} />
          <Route path="/chats" element={<Chats />} />
          <Route path="/settings" element={<PageSettings />} />
          <Route path="/about" element={<About />} />
          <Route path="/command/add" element={<CommandAdd />} />
          <Route path="/command/list" element={<CommandList />} />
          <Route path="/command/edit/:command" element={<CommandEdit />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;

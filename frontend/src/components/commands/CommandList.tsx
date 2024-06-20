import React, { useEffect, useState } from 'react';
import { useAlert } from '../AlertContext';
import { Link } from 'react-router-dom';

export function CommandList() {
  const [commands, setCommands] = useState<Array<string>>([]);
  const { openAlert } = useAlert();

  const fetchCommands = async () => {
    const response = await fetch('http://127.0.0.1:8000/command/list');
    if (!response.ok) {
      console.error('Failed to fetch commands.');
      openAlert('Failed to fetch commands.');
    } else {
      const data = await response.json();
      setCommands(data);
    }
  };

  const deleteCommand = async (command: string) => {
    const response = await fetch(`http://127.0.0.1:8000/command/delete/${command}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const data = await response.json();
      console.log(data);
      openAlert(`Error occurred: ${JSON.stringify(data.err)}`);
    } else {
      setCommands((prevCommands) => prevCommands.filter((cmd) => cmd !== command));
      openAlert('Successfully deleted command.');
    }
  };

  useEffect(() => {
    fetchCommands();
  }, []);

  return (
    <div className="max-h-[calc(100vh-2rem)] text-gray-700 w-full gap-6 p-4 overflow-y-scroll">
      <ul className="space-y-3">
        <li
          className="flex items-center justify-between p-4 card rounded shadow">
          <span>Add new command!</span>
          <div>
            <Link className="w-36" to="/command/add">
              <button
                onClick={console.log}
                className="items-center min-w-[80px] hover:border-green-500 border-2 p-3 rounded-lg text-center leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none">
                Add
              </button>
            </Link>
          </div>
        </li>
        {commands.map((command, index) => (
          <li
            key={index}
            className="flex items-center justify-between p-4 card rounded shadow">
            <span>{command}</span>
            <div>
              <button
                onClick={console.log}
                className="items-center mx-3 min-w-[80px] text-center hover:border-amber-500 border-2 p-3 rounded-lg leading-tight transition-all hover:bg-amber-50 hover:bg-opacity-80 active:bg-amber-50 bg-opacity-80 hover:text-yellow-900 active:text-yellow-900 outline-none">
                Edit
              </button>
              <button
                onClick={() => deleteCommand(command)}
                className="items-center min-w-[80px] hover:border-red-500 border-2 p-3 rounded-lg text-center leading-tight transition-all hover:bg-red-50 hover:bg-opacity-80 active:bg-red-50 active:bg-opacity-80 hover:text-red-900 active:text-red-900 outline-none">
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Alert } from '@material-tailwind/react';

interface IAlertContext {
  openAlert: (message: string) => void;
}

const AlertContext = createContext<IAlertContext | undefined>(undefined);

export const useAlert = () => {
  const context = useContext(AlertContext);
  if (!context) throw new Error('useAlert must be used within an AlertProvider');
  return context;
};

export const AlertProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');

  window.electronAPI.onAlertMessage((value: string) => {
    openAlert(value);
  });

  const openAlert = (newMessage: string) => {
    setMessage(newMessage);
    setOpen(true);
    setTimeout(() => {
      setOpen(false);
      setMessage('');
    }, 7000);
  };

  return (
    <AlertContext.Provider value={{ openAlert }}>
      {open && (
        <Alert
          className="absolute top-0 right-0 w-1/3 z-10 m-3"
          animate={{
            mount: { y: 0 },
            unmount: { y: 100 },
          }}
          onClose={() => setOpen(false)}
        >
          {message}
        </Alert>
      )}
      {children}
    </AlertContext.Provider>
  );
};

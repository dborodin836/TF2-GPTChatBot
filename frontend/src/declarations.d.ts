interface Window {
  electronAPI: {
    onAlertMessage: (callback: (value: string) => void) => void;
  };
}

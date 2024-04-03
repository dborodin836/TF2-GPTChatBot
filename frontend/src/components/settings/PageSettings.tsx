import React, { useEffect, useState } from 'react';
import { RequireSettings } from './RequiredSettings';
import { RCONSettings } from './RCONSettings';
import { OpenAISettings } from './OpenAISettings';
import { TextgenWebUISettings } from './TextgenWebUISettings';
import { StatsSettings } from './StatsSettings';
import { RTDSettings } from './RTDSettings';
import { MiscellaneousSettings } from './MiscellaneousSettings';
import { ExperimentalSettings } from './ExperimentalSettings';
import { ChatSettings } from './ChatSettings';
import { Controls } from './Controls';
import { Settings } from './SettingsType';
import { useAlert } from '../AlertContext';

interface ValidationError {
  ctx: any;
  input: string;
  loc: string[];
  msg: string;
  type: string;
  url: string;
}

export function PageSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const { openAlert } = useAlert();

  const fetchSettings = async () => {
    const response = await fetch('http://127.0.0.1:8000/settings');
    if (!response.ok) {
      console.error('Failed to fetch settings');
      openAlert('Failed to fetch settings.');
    } else {
      const data = await response.json();
      setSettings(data);
    }
  };

  const fetchDefaultSettings = async () => {
    const response = await fetch('http://127.0.0.1:8000/settings/default');
    if (!response.ok) {
      console.error('Failed to fetch default settings');
      openAlert('Failed to fetch default settings.');
    } else {
      const data = await response.json();
      setSettings(data);
      console.log(data);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const discardChanges = () => {
    fetchSettings();
  };

  const submitSettings = async () => {
    // Ensure there are settings to submit
    if (!settings) {
      console.log('No settings to submit');
      return;
    }

    const response = await fetch('http://127.0.0.1:8000/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settings),
    });

    if (!response.ok) {
      console.error('Settings are invalid.');
      const data: ValidationError[] = await response.json();
      const fieldsWithErrors = data.map((element: ValidationError) => element.loc[0]);
      openAlert(`Settings are invalid. [${fieldsWithErrors.join(', ')}]`);
    } else {
      openAlert('Successfully saved settings.');
    }
  };

  const handleRTDModeChange = (mode: number) => {
    setSettings((prevSettings: any) => ({
      ...prevSettings,
      RTD_MODE: mode,
    }));
  };

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setSettings((prevSettings: any) => ({
      ...prevSettings,
      [name]: value,
    }));
  };

  const handleToggle = (e: any) => {
    const { name } = e.target;
    setSettings((prevSettings: any) => ({
      ...prevSettings,
      [name]: !prevSettings[name],
    }));
  };

  return (
    <>
      <Controls
        submit={submitSettings}
        discard={discardChanges}
        getDefaults={fetchDefaultSettings}
      />

      <div className="flex flex-1 max-h-[calc(100vh-7rem)] flex-col text-gray-700 w-full gap-6 p-4 overflow-y-scroll">
        <RequireSettings settings={settings} onChangeInput={handleInputChange} />

        <RCONSettings settings={settings} onChangeInput={handleInputChange} />

        <OpenAISettings
          settings={settings}
          onChangeToggle={handleToggle}
          onChangeInput={handleInputChange}
        />

        <ChatSettings
          settings={settings}
          onChangeInput={handleInputChange}
          onChangeToggle={handleToggle}
        />

        <TextgenWebUISettings
          settings={settings}
          onChangeToggle={handleToggle}
          onChangeInput={handleInputChange}
        />

        <StatsSettings
          settings={settings}
          onChangeToggle={handleToggle}
          onChangeInput={handleInputChange}
        />

        <RTDSettings
          settings={settings}
          onChangeRadio0={() => {
            handleRTDModeChange(0);
          }}
          onChangeRadio1={() => {
            handleRTDModeChange(1);
          }}
          onChangeRadio2={() => {
            handleRTDModeChange(2);
          }}
        />

        <MiscellaneousSettings settings={settings} onChangeToggle={handleToggle} />

        <ExperimentalSettings settings={settings} onChangeToggle={handleToggle} />
      </div>
    </>
  );
}

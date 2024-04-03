import { Card, Input, Switch, Textarea, Typography } from '@material-tailwind/react';
import React from 'react';
import * as PropTypes from 'prop-types';
import { Settings } from './SettingsType';

export function TextgenWebUISettings(props: {
  settings: Settings | null;
  onChangeToggle: any;
  onChangeInput: any;
}) {
  return (
    <Card className="p-6 w-full">
      <Typography className="mb-3" variant="h2">
        Text Generation WebUI
      </Typography>
      <hr className="mb-3" />

      <div className="ml-1 mb-3">
        <Switch
          label="Enable Text Generation WebUI Integration"
          checked={props.settings?.ENABLE_CUSTOM_MODEL || false}
          name="ENABLE_CUSTOM_MODEL"
          onChange={props.onChangeToggle}
        />
      </div>
      <hr className="mb-3" />

      <div className="ml-1 mb-3">
        <Switch
          label="Enable Soft Completion Limit For Custom Model"
          checked={props.settings?.ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL || false}
          name="ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL"
          onChange={props.onChangeToggle}
        />
      </div>
      <hr className="mb-3" />

      <div className="flex">
        <div className="mb-3 w-[100%]">
          <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            Custom Model Command
          </label>
          <div className="min-w-[100%]">
            <Input
              className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
              labelProps={{
                className: 'hidden',
              }}
              containerProps={{ className: 'min-w-[100px]' }}
              value={props.settings ? props.settings.CUSTOM_MODEL_COMMAND : ''}
              name="CUSTOM_MODEL_COMMAND"
              onChange={props.onChangeInput}
            />
          </div>
        </div>

        <div className="mb-3 ml-3 w-[100%]">
          <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            Private Chat Command
          </label>
          <div className="min-w-[100%]">
            <Input
              className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
              labelProps={{
                className: 'hidden',
              }}
              containerProps={{ className: 'min-w-[100px]' }}
              value={props.settings ? props.settings.CUSTOM_MODEL_CHAT_COMMAND : ''}
              name="CUSTOM_MODEL_CHAT_COMMAND"
              onChange={props.onChangeInput}
            />
          </div>
        </div>

        <div className="mb-3 ml-3 w-[100%]">
          <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            Global Chat Command
          </label>
          <div className="min-w-[100%]">
            <Input
              className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
              labelProps={{
                className: 'hidden',
              }}
              containerProps={{ className: 'min-w-[100px]' }}
              value={props.settings ? props.settings.GLOBAL_CUSTOM_CHAT_COMMAND : ''}
              name="GLOBAL_CUSTOM_CHAT_COMMAND"
              onChange={props.onChangeInput}
            />
          </div>
        </div>
      </div>

      <div className="mb-3">
        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
          Custom Model Host
        </label>
        <div className="min-w-[100%]">
          <Input
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            labelProps={{
              className: 'hidden',
            }}
            containerProps={{ className: 'min-w-[100px]' }}
            value={props.settings ? props.settings.CUSTOM_MODEL_HOST : ''}
            name="CUSTOM_MODEL_HOST"
            onChange={props.onChangeInput}
          />
        </div>
      </div>

      <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
        Cutom Model Settings
      </label>
      <Textarea
        className="!border mb-3 !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
        size="lg"
        id="textarea_logs"
        labelProps={{
          className: 'hidden',
        }}
        value={props.settings ? props.settings.CUSTOM_MODEL_SETTINGS : ''}
        name="CUSTOM_MODEL_SETTINGS"
        onChange={props.onChangeInput}
      />
    </Card>
  );
}

TextgenWebUISettings.propTypes = {
  settings: PropTypes.any,
  onChangeToggle: PropTypes.func,
  onChangeInput: PropTypes.func,
};

import { Card, Input, Switch, Typography } from '@material-tailwind/react';
import React from 'react';
import * as PropTypes from 'prop-types';
import { Settings } from './SettingsType';

export function OpenAISettings(props: {
  settings: Settings | null;
  onChangeToggle: React.ChangeEventHandler<HTMLInputElement> | undefined;
  onChangeInput: React.ChangeEventHandler<HTMLInputElement> | undefined;
}) {
  return (
    <Card className="p-6 w-full">
      <Typography className="mb-3" variant="h2">
        OpenAI
      </Typography>
      <hr className="mb-3" />

      <div className="ml-1 mb-3">
        <Switch
          label="Enable OpenAI Commands"
          checked={props.settings?.ENABLE_OPENAI_COMMANDS || false}
          name="ENABLE_OPENAI_COMMANDS"
          onChange={props.onChangeToggle}
        />
      </div>

      <hr className="mb-3" />

      <div className="ml-1 mb-3">
        <Switch
          label="Enable Message Moderation"
          name="TOS_VIOLATION"
          checked={!!props.settings?.TOS_VIOLATION}
          onChange={props.onChangeToggle}
        />
      </div>

      <hr className="mb-3" />

      <div className="mb-3">
        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
          OpenAI API Key
        </label>
        <div className="min-w-[100%]">
          <Input
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            labelProps={{
              className: 'hidden',
            }}
            containerProps={{ className: 'min-w-[100px]' }}
            value={props.settings ? props.settings.OPENAI_API_KEY : ''}
            name="OPENAI_API_KEY"
            onChange={props.onChangeInput}
          />
        </div>
      </div>

      <div className="mb-3">
        <div className="flex">
          <div className="mb-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT3 Model Command
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT_COMMAND : ''}
                name="GPT_COMMAND"
                onChange={props.onChangeInput}
              />
            </div>
          </div>

          <div className="mb-3 ml-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT3 Model
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT3_MODEL : ''}
                name="GPT3_MODEL"
                onChange={props.onChangeInput}
              />
            </div>
          </div>
        </div>

        <div className="flex">
          <div className="mb-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT4 Model Command
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT4_COMMAND : ''}
                name="GPT4_COMMAND"
                onChange={props.onChangeInput}
              />
            </div>
          </div>

          <div className="mb-3 ml-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT4 Model
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT4_MODEL : ''}
                name="GPT4_MODEL"
                onChange={props.onChangeInput}
              />
            </div>
          </div>
        </div>

        <div className="flex">
          <div className="mb-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT4 Legacy Model Command
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT4_LEGACY_COMMAND : ''}
                name="GPT4_LEGACY_COMMAND"
                onChange={props.onChangeInput}
              />
            </div>
          </div>

          <div className="mb-3 ml-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              GPT4 Legacy Model
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT4L_MODEL : ''}
                name="GPT4L_MODEL"
                onChange={props.onChangeInput}
              />
            </div>
          </div>
        </div>

        <div className="flex">
          <div className="mb-3 w-[100%]">
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
                value={props.settings ? props.settings.GLOBAL_CHAT_COMMAND : ''}
                name="GLOBAL_CHAT_COMMAND"
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
                value={props.settings ? props.settings.CHATGPT_COMMAND : ''}
                name="CHATGPT_COMMAND"
                onChange={props.onChangeInput}
              />
            </div>
          </div>

          <div className="mb-3 ml-3 w-[100%]">
            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
              Chat Model
            </label>
            <div className="min-w-[100%]">
              <Input
                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                labelProps={{
                  className: 'hidden',
                }}
                containerProps={{ className: 'min-w-[100px]' }}
                value={props.settings ? props.settings.GPT3_CHAT_MODEL : ''}
                name="GPT3_CHAT_MODEL"
                onChange={props.onChangeInput}
              />
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}

OpenAISettings.propTypes = {
  settings: PropTypes.any,
  onChangeToggle: PropTypes.func,
  onChangeInput: PropTypes.func,
};

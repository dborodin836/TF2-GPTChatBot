import { Card, Input, Typography } from '@material-tailwind/react';
import React from 'react';
import * as PropTypes from 'prop-types';
import { Settings } from './SettingsType';

export function GroqSettings(props: {
  settings: Settings | null;
  onChangeToggle: React.ChangeEventHandler<HTMLInputElement> | undefined;
  onChangeInput: React.ChangeEventHandler<HTMLInputElement> | undefined;
}) {
  return (
    <Card className="p-6 w-full">
      <Typography className="mb-3" variant="h2">
        GroqCloud
      </Typography>
      <hr className="mb-3" />

      <div className="mb-3">
        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
          GroqCloud API Key
        </label>
        <div className="min-w-[100%]">
          <Input
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            labelProps={{
              className: 'hidden',
            }}
            containerProps={{ className: 'min-w-[100px]' }}
            value={props.settings ? props.settings.GROQ_API_KEY : ''}
            name="GROQ_API_KEY"
            onChange={props.onChangeInput}
          />
        </div>
      </div>
    </Card>
  );
}

GroqSettings.propTypes = {
  settings: PropTypes.any,
  onChangeToggle: PropTypes.func,
  onChangeInput: PropTypes.func,
};
